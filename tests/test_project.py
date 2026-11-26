from datetime import date
from flask import Flask
import database
from database import get_connection, load_sample_data
from validators import validate_name, validate_alumni, validate_message
from search import search_alumni
from matching import score_alumni, suggest_mentors, keywords
from mentoring_requests import create_request, update_request_status
from reports import participation_report, report_csv


def sample_rows():
    student = {"interests": " Python, data, python ", "target_industry": "Technology"}
    alumnus = {"interests": "", "expertise": "python, cloud", "industry": "technology", "consent": 1}
    return student, alumnus


def test_validators_and_year_boundaries():
    assert validate_name("Ava")[0]
    assert not validate_name("A")[0]
    assert validate_alumni("Ava", "1990", "Technology", "Engineer", "python")[0]
    assert validate_alumni("Ava", str(date.today().year), "Technology", "Engineer", "python")[0]
    assert not validate_alumni("Ava", "1989", "Technology", "Engineer", "python")[0]
    assert not validate_alumni("Ava", str(date.today().year + 1), "Technology", "Engineer", "python")[0]
    assert not validate_alumni("Ava", "nope", "Technology", "Engineer", "python")[0]
    assert not validate_alumni("Ava", "2020", "Unknown", "Engineer", "python")[0]
    assert not validate_alumni("Ava", "2020", "Technology", "Engineer", "a,b,c,d,e,f")[0]


def test_search_filters_consent_and_empty(temporary_database):
    load_sample_data(temporary_database)
    assert len(search_alumni()) == 14
    connection = get_connection(temporary_database)
    assert connection.execute("SELECT COUNT(*) FROM alumni").fetchone()[0] == 16
    connection.close()
    assert search_alumni({"industry": "TECHNOLOGY"})
    assert search_alumni({"role": "engineer", "industry": "technology"})
    assert search_alumni({"graduation_year": "2005"})
    assert search_alumni({"expertise": "cloud"})
    assert search_alumni({"role": "no such role"}) == []
    assert all(row["consent"] for row in search_alumni())


def test_matching_scores_deduplicates_keywords_and_top_three():
    student, alumnus = sample_rows()
    score, reasons = score_alumni(student, alumnus)
    assert score == 4
    assert len(keywords("python, Python , data")) == 2
    assert reasons == ["same industry (+3)", "python (+1)"]
    alumnus["expertise"] = "design"
    assert score_alumni(student, alumnus)[0] == 3
    people = [dict(alumnus, name=str(i)) for i in range(5)]
    assert len(suggest_mentors(student, people)) == 3


def test_requests_validate_duplicate_consent_and_transitions(temporary_database):
    load_sample_data(temporary_database)
    assert create_request(999, 1, "A useful mentoring question")[0] is False
    assert create_request(1, 6, "A useful mentoring question")[0] is False
    assert not create_request(1, 1, "short")[0]
    assert create_request(1, 1, "A useful mentoring question")[0] is False  # seeded pending
    assert create_request(1, 3, "I would like to learn about your career.")[0]
    assert update_request_status(1, "Accepted")[0]
    assert update_request_status(1, "Completed")[0]
    assert not update_request_status(1, "Declined")[0]
    assert not update_request_status(999, "Accepted")[0]


def test_report_csv_and_zero_division(temporary_database):
    connection = get_connection(temporary_database)
    connection.execute("INSERT INTO students(name,department,interests,target_industry) VALUES ('Test Student','IT','python','Technology')")
    connection.commit()
    connection.close()
    report = participation_report()
    assert report["total_requests"] == 0
    assert report["acceptance_rate"] == 0
    assert "Metric,Value" in report_csv(report)
    load_sample_data(temporary_database)
    report = participation_report()
    assert report["acceptance_rate"] == 50.0
    assert report["completed"] == 1
    assert report["declined"] == 1


def test_flask_routes_and_form(temporary_database, monkeypatch):
    import app as web_app
    monkeypatch.setattr(web_app.database, "DATABASE_PATH", temporary_database)
    web_app.initialize_database(temporary_database)
    load_sample_data(temporary_database)
    web_app.app.config["TESTING"] = True
    client = web_app.app.test_client()
    assert client.get("/").status_code == 200
    assert client.get("/directory").status_code == 200
    assert client.get("/alumni/6").status_code == 302
    assert client.get("/reports.csv").mimetype == "text/csv"
    response = client.post("/student", data={"name": "New Student", "department": "IT", "interests": "python", "target_industry": "Technology"})
    assert response.status_code == 302
    assert client.get("/matches").status_code == 200
