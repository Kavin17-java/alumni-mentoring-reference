"""SQLite setup and fictional classroom demonstration data."""
import csv
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "data" / "alumni.db"


def get_connection(database_path=None):
    """Open a database connection and enable foreign-key checks."""
    if database_path is None:
        database_path = DATABASE_PATH
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(database_path=None):
    """Create project tables if they do not already exist."""
    if database_path is None:
        database_path = DATABASE_PATH
    Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    connection = get_connection(database_path)
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            department TEXT NOT NULL, interests TEXT NOT NULL, target_industry TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS alumni (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            graduation_year INTEGER NOT NULL, industry TEXT NOT NULL, role TEXT NOT NULL,
            expertise TEXT NOT NULL, consent INTEGER NOT NULL DEFAULT 0, consent_date TEXT
        );
        CREATE TABLE IF NOT EXISTS mentoring_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL REFERENCES students(id),
            alumni_id INTEGER NOT NULL REFERENCES alumni(id), message TEXT NOT NULL,
            status TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
    """)
    connection.commit()
    connection.close()


def load_sample_data(database_path=None):
    """Insert fictional sample rows once."""
    if database_path is None:
        database_path = DATABASE_PATH
    connection = get_connection(database_path)
    found = connection.execute("SELECT id FROM alumni WHERE name = ?", ("Aarav Demo",)).fetchone()
    if found:
        connection.close()
        return
    students = [
        ("Riya Student", "Information Technology", "python, data, cloud", "Technology"),
        ("Dev Student", "Information Technology", "design, analytics", "Finance"),
    ]
    connection.executemany("INSERT INTO students(name, department, interests, target_industry) VALUES (?, ?, ?, ?)", students)
    sample_file = Path(__file__).parent / "data" / "alumni.csv"
    try:
        with open(sample_file, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                consent = int(row["consent"])
                connection.execute(
                    "INSERT INTO alumni(name, graduation_year, industry, role, expertise, consent, consent_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (row["name"], int(row["graduation_year"]), row["industry"], row["role"], row["expertise"], consent, "2026-11-01" if consent else None),
                )
    except (OSError, csv.Error, KeyError, ValueError) as error:
        connection.close()
        raise ValueError("Sample alumni CSV could not be loaded: " + str(error)) from error
    connection.execute("INSERT INTO mentoring_requests(student_id, alumni_id, message, status, created_at, updated_at) VALUES (1, 1, ?, 'Pending', '2026-11-01', '2026-11-01')", ("Could you share advice about starting in technology?",))
    connection.execute("INSERT INTO mentoring_requests(student_id, alumni_id, message, status, created_at, updated_at) VALUES (2, 2, ?, 'Accepted', '2026-11-02', '2026-11-03')", ("Could you share your career journey in finance?",))
    connection.execute("INSERT INTO mentoring_requests(student_id, alumni_id, message, status, created_at, updated_at) VALUES (1, 3, ?, 'Declined', '2026-11-04', '2026-11-05')", ("Could you explain your product career path?",))
    connection.execute("INSERT INTO mentoring_requests(student_id, alumni_id, message, status, created_at, updated_at) VALUES (2, 4, ?, 'Completed', '2026-11-06', '2026-11-10')", ("Could you share advice about cloud engineering?",))
    connection.commit()
    connection.close()
