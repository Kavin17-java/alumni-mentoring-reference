# Code walkthrough

## File map
- app.py: Flask app, URL routes, request handling and template rendering.
- database.py: SQLite connection, table creation and fictional sample loading.
- validators.py: server-side checks and allowed industries.
- profiles.py: insert student and alumni profiles.
- search.py: consenting alumni filter logic.
- matching.py: normalized keywords, score and top three recommendations.
- mentoring_requests.py: request creation, status transitions and joined listing.
- reports.py: report counts and CSV text.
- templates/: page HTML, shared layout and Jinja expressions.
- static/style.css: visual adjustments.
- tests/: pytest checks using a temporary SQLite file.
- .github/workflows/tests.yml: run tests on push and pull request.
- Procfile and requirements.txt: Render process and dependencies.
- docs/: learning and team references.

## Application flow and imports
app.py imports Flask helpers (Flask, render_template, request, session, flash, redirect, url_for, Response), feature modules, and standard os/csv. Flask(__name__) creates the application. secret_key allows Flask sessions; its default is explicitly demo-only.

shared_template_data() queries selectable profiles and supplies them to templates. home() saves a demonstration role and profile IDs in session. It is not authentication or access control.

## Routes

| URL | Function | Behavior |
|---|---|---|
| / | home | Select demo role/profile or show landing page |
| /student | student_profile | Validate and save student |
| /alumni/register | alumni_register | Validate and save profile and consent |
| /alumni/<id>/consent | withdraw_consent | Set consent false and clear consent date |
| /directory | directory | Pass four optional filters into search |
| /alumni/<id> | alumni_detail | Show only a consenting profile |
| /matches | matches | Score consenting mentors for selected student |
| /requests/new/<id> | new_request | Validate and create a request |
| /requests | requests_page | List requests with profile names |
| /requests/<id>/status | request_status | Check and update status |
| /reports | report_page | Show participation counts |
| /reports.csv | export_report | Send CSV download |
| unknown URL | not_found | Render friendly 404 |

render_template() combines a template and values. redirect(url_for(...)) returns the browser to a named route after a change. request.args reads URL filters; request.form reads submitted fields.

## Functions and SQL
- get_connection(path=None) sets named-column row results and enables SQLite foreign keys.
- initialize_database(path) creates three tables if absent.
- load_sample_data(path) adds fictional sample data only if sentinel alumni is absent.
- validate_name/student/alumni/message return (valid, message).
- create_student and create_alumni insert a row and return its generated ID.
- search_alumni(filters) returns rows matching all non-empty filters among consenting profiles.
- keywords(text) returns distinct lowercase, trimmed comma-separated words.
- score_alumni(student, alumni) returns (score, reasons).
- suggest_mentors(student, alumni_list) returns up to three consenting positive results.
- create_request and update_request_status return (success, message).
- participation_report() returns a dictionary of counts and acceptance percentage.
- report_csv(report) returns CSV text.

CREATE TABLE defines primary keys and request foreign keys. SELECT ... WHERE consent = 1 protects directory results. INSERT ... VALUES (?,...) uses placeholders so input is data, not SQL syntax. UPDATE ... WHERE id = ? changes one row. Request listings use JOIN to attach names. COUNT computes totals; COUNT(DISTINCT alumni_id) counts alumni who received requests.

## Jinja and forms
{% raw %}{% extends "base.html" %}{% endraw %} shares the navigation layout. A Jinja value expression prints data with HTML escaping. A for block repeats cards or table rows; an if block selects the empty-state message. url_for() builds route links. GET forms produce query parameters; POST forms send form values.

## End-to-end examples

### Searching
1. Browser submits four optional fields with GET to /directory.
2. directory() reads request.args.
3. search_alumni() selects only consenting rows and compares non-empty filters case-insensitively.
4. Route supplies matching rows and filter values to directory.html.
5. Jinja displays results or a no-results message.

### Recommendations
1. /matches loads selected student and consenting alumni from SQLite.
2. suggest_mentors() calls score_alumni() for each person.
3. keywords() trims, lowercases and deduplicates comma-separated values.
4. Shared words add one point each; matching industry adds three.
5. Positive scores are sorted and up to three appear with reasons.

### Submitting a request
1. Alumni detail opens /requests/new/<id>.
2. POST form sends student ID and message.
3. Route validates message length; create_request() checks student, alumnus consent and duplicate pending request.
4. Parameterized INSERT stores Pending and timestamps.
5. Browser is redirected to requests list.

### Updating status
1. Request table sends a new status with POST.
2. update_request_status() reads current status and checks ALLOWED_NEXT.
3. A valid UPDATE stores status and last-updated time; invalid transitions return a friendly message.
4. Route flashes the outcome and returns to the list.
