"""Database functions for creating and finding profiles."""
from datetime import date
from database import get_connection


def create_student(name, department, interests, target_industry):
    connection = get_connection()
    cursor = connection.execute("INSERT INTO students(name, department, interests, target_industry) VALUES (?, ?, ?, ?)", (name.strip(), department.strip(), interests.strip(), target_industry.strip()))
    connection.commit()
    student_id = cursor.lastrowid
    connection.close()
    return student_id


def create_alumni(name, year, industry, role, expertise, consent):
    connection = get_connection()
    cursor = connection.execute("INSERT INTO alumni(name, graduation_year, industry, role, expertise, consent, consent_date) VALUES (?, ?, ?, ?, ?, ?, ?)", (name.strip(), int(year), industry, role.strip(), expertise.strip(), int(consent), date.today().isoformat() if consent else None))
    connection.commit()
    alumni_id = cursor.lastrowid
    connection.close()
    return alumni_id
