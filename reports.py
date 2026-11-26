"""Participation counts and CSV export."""
import csv
import io
from database import get_connection


def participation_report():
    connection = get_connection()
    alumni_count = connection.execute("SELECT COUNT(*) FROM alumni WHERE consent=1").fetchone()[0]
    student_count = connection.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    total = connection.execute("SELECT COUNT(*) FROM mentoring_requests").fetchone()[0]
    counts = {}
    for status in ("Pending", "Accepted", "Declined", "Completed"):
        counts[status.lower()] = connection.execute("SELECT COUNT(*) FROM mentoring_requests WHERE status=?", (status,)).fetchone()[0]
    received = connection.execute("SELECT COUNT(DISTINCT alumni_id) FROM mentoring_requests").fetchone()[0]
    accepted_total = counts["accepted"] + counts["completed"]
    rate = round(accepted_total * 100 / total, 1) if total else 0
    connection.close()
    return {"consenting_alumni": alumni_count, "students": student_count, "total_requests": total, **counts, "alumni_with_requests": received, "acceptance_rate": rate}


def report_csv(report):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Metric", "Value"])
    for name, value in report.items():
        writer.writerow([name, value])
    return output.getvalue()
