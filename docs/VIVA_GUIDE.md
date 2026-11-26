# Viva guide

**What is Flask?** A small Python web framework. This app uses it to connect URLs with Python functions.

**What does a route do?** A route decorator associates a URL and HTTP method with a view function, such as /directory with directory().

**How do forms work?** HTML names each input. A GET form places values in the URL and Flask reads request.args. POST sends values in the request body and Flask reads request.form.

**Why use GET for search and POST for changes?** Filters can be bookmarked and shared as a URL. Profile and request changes should be submitted as form actions.

**What is a template?** Jinja combines an HTML template with values from Flask. Loops display lists and conditions display empty states.

**What is SQLite?** A database stored in a local file and accessed here through Python's built-in sqlite3 module.

**Why primary and foreign keys?** A primary key identifies a row. Request foreign keys link a student and alumnus and help prevent orphan references.

**Why parameterized SQL?** The question-mark placeholders keep values separate from SQL commands and avoid unsafe query construction.

**How does matching work?** Matching industry gives three points; each unique shared keyword gives one. Only positive consenting matches are displayed, with reasons.

**How is input checked?** Server-side functions check required values, name length, year range, industry, expertise count and message length before database insertion.

**What do tests check?** pytest asserts known expected results for validation, consent filters, scores, request transitions, reports and Flask routes. A temporary database keeps tests away from sample data.

**What does GitHub Actions do?** It runs the test command on a push or pull request so errors can be found before merging.

**How should the team use GitHub?** Each person works on a feature branch, makes commits, opens a PR and reviews another person's change. Protect main with a required review and passing test status.

**How is the app deployed?** Render installs requirements and starts Gunicorn with app:app. Environment variables hold settings such as SECRET_KEY.

**What is a deployment limitation?** SQLite is a local file. Hosted instance replacements can erase it unless persistent storage is configured; this demo is designed for class learning, not production.
