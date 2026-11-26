"""Create requests and enforce the allowed status flow."""
from datetime import datetime
from database import get_connection
from validators import validate_message

ALLOWED_NEXT = {"Pending": ["Accepted", "Declined"], "Accepted": ["Completed"], "Declined": [], "Completed": []}


def create_request(student_id, alumni_id, message):
    valid, error = validate_message(message)
    if not valid:
        return False, error
    connection = get_connection()
    student = connection.execute("SELECT id FROM students WHERE id = ?", (student_id,)).fetchone()
    alumni = connection.execute("SELECT id, consent FROM alumni WHERE id = ?", (alumni_id,)).fetchone()
    if not student or not alumni:
        connection.close()
        return False, "Student or alumnus was not found."
    if not alumni["consent"]:
        connection.close()
        return False, "This alumnus is not accepting mentoring requests."
    duplicate = connection.execute("SELECT id FROM mentoring_requests WHERE student_id = ? AND alumni_id = ? AND status = 'Pending'", (student_id, alumni_id)).fetchone()
    if duplicate:
        connection.close()
        return False, "A pending request already exists for this pair."
    now = datetime.now().isoformat(timespec="seconds")
    connection.execute("INSERT INTO mentoring_requests(student_id, alumni_id, message, status, created_at, updated_at) VALUES (?, ?, ?, 'Pending', ?, ?)", (student_id, alumni_id, message.strip(), now, now))
    connection.commit()
    connection.close()
    return True, "Request sent."


def update_request_status(request_id, new_status):
    connection = get_connection()
    request = connection.execute("SELECT status FROM mentoring_requests WHERE id = ?", (request_id,)).fetchone()
    if not request:
        connection.close()
        return False, "Request was not found."
    if new_status not in ALLOWED_NEXT.get(request["status"], []):
        connection.close()
        return False, "That status change is not allowed."
    now = datetime.now().isoformat(timespec="seconds")
    connection.execute("UPDATE mentoring_requests SET status = ?, updated_at = ? WHERE id = ?", (new_status, now, request_id))
    connection.commit()
    connection.close()
    return True, "Request status updated."


def list_requests():
    connection = get_connection()
    rows = connection.execute("SELECT r.*, s.name AS student_name, a.name AS alumni_name FROM mentoring_requests r JOIN students s ON r.student_id=s.id JOIN alumni a ON r.alumni_id=a.id ORDER BY r.id DESC").fetchall()
    connection.close()
    return rows
