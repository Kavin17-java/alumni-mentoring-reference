"""Consenting alumni search using easy-to-follow Python comparisons."""
from database import get_connection


def search_alumni(filters=None):
    filters = filters or {}
    connection = get_connection()
    rows = connection.execute("SELECT * FROM alumni WHERE consent = 1 ORDER BY name").fetchall()
    connection.close()
    results = []
    for alumni in rows:
        matched = True
        for field in ("industry", "expertise", "role", "graduation_year"):
            wanted = str(filters.get(field, "")).strip().lower()
            if wanted:
                actual = str(alumni[field]).lower()
                if (field == "graduation_year" and wanted != actual) or (field != "graduation_year" and wanted not in actual):
                    matched = False
        if matched:
            results.append(alumni)
    return results
