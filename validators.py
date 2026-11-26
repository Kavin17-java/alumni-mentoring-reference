"""Small server-side validation functions shared by the routes."""
from datetime import date

INDUSTRIES = ["Technology", "Finance", "Healthcare", "Education", "Design", "Other"]


def validate_name(value):
    value = value.strip()
    if len(value) < 2 or len(value) > 60:
        return False, "Name must contain 2 to 60 characters."
    return True, value


def validate_student(name, department, interests, target_industry):
    valid, result = validate_name(name)
    if not valid:
        return False, result
    if not department.strip() or not interests.strip() or not target_industry.strip():
        return False, "Department, interests and target industry are required."
    return True, ""


def validate_alumni(name, year, industry, role, expertise):
    valid, result = validate_name(name)
    if not valid:
        return False, result
    try:
        year_number = int(year)
    except (TypeError, ValueError):
        return False, "Graduation year must be a whole number."
    if year_number < 1990 or year_number > date.today().year:
        return False, "Graduation year must be between 1990 and the current year."
    if industry not in INDUSTRIES:
        return False, "Choose a valid industry."
    if not role.strip() or not expertise.strip():
        return False, "Role and expertise are required."
    keywords = [word.strip() for word in expertise.split(",") if word.strip()]
    if len(keywords) > 5:
        return False, "Enter no more than five expertise keywords."
    return True, ""


def validate_message(message):
    if len(message.strip()) < 10 or len(message.strip()) > 300:
        return False, "Message must contain 10 to 300 characters."
    return True, ""
