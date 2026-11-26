# Syllabus mapping

The requested curriculum PDF (B.Tech IT Curriculum & Syllabus, 27 July 2026) was not included among the supplied files. Therefore this mapping uses the three Semester I subject headings and pages named in the request as a provisional guide; unit names and page-level claims require comparison with that PDF.

| File/function | Concept | Subject area | Unit/page | Beyond syllabus? | Why added |
|---|---|---|---|---|---|
| validators.py validation functions | strings, conditions, integer conversion, try/except | Computational Thinking and Problem Solving with Python | Provisional; exact unit unavailable | No for fundamentals | Check fields before saving |
| search.py search_alumni | loops, string comparison, conditions | Computational Thinking and Problem Solving with Python | Provisional | No for fundamentals | Apply combined filters |
| matching.py keywords/score_alumni | sets, loops, arithmetic, sorting | Computational Thinking and Problem Solving with Python | Provisional | Set/sort syllabus coverage unconfirmed | Explain simple match scores |
| database.py | imports, functions, file path | Python / web project | Provisional | SQLite is beyond core Python syllabus | Create a local persistent database |
| database.py SQL | tables, keys, SELECT, INSERT, UPDATE, JOIN | Open-Source Tools project context | Not listed in provided curriculum pages | Yes | Store linked profile and request data |
| app.py routes | functions, if, imports | Introduction to Web Programming | Provisional; pages unavailable | Flask-specific concepts extend beyond syllabus | Connect URLs to Python behavior |
| app.py request.args/form | GET/POST forms | Introduction to Web Programming | Provisional | Flask details beyond syllabus | Receive filters and form data |
| app.py session | browser session | Introduction to Web Programming | Provisional | Yes | Remember demo role/profile selection |
| templates/*.html | HTML forms, navigation, tables | Introduction to Web Programming | Provisional | Jinja extends beyond plain HTML | Show pages and dynamic database values |
| templates/base.html and style.css | CSS, Bootstrap, responsive grid | Introduction to Web Programming | Provisional | Bootstrap details beyond basics | Provide consistent responsive presentation |
| reports.py | counting, arithmetic, CSV file format | Computational Thinking and Open-Source Tools | Provisional | Python csv library use is an extension | Export report for coordinator |
| tests/test_project.py | assertions, fixtures, temporary DB | Open-Source Tools and Prompt Engineering | Provisional | pytest fixture/database concepts are additional | Repeat checks without changing demo DB |
| tests.yml | YAML and continuous integration | Open-Source Tools and Prompt Engineering | Provisional | Yes | Run tests on pushes and pull requests |
| GitHub workflow documented in README | branches, commits, reviews, protected main | Open-Source Tools and Prompt Engineering | Provisional | Platform workflow details extend basics | Coordinate team work |
| Procfile / README | Gunicorn, environment settings, Render | Introduction to Web Programming / Open-Source Tools | Provisional | Yes | Explain hosted execution |

## Complexity review

The implementation avoids advanced OOP, custom decorators, ORM, AJAX, JavaScript, authentication frameworks and migrations. Flask route decorators are framework syntax required for URL mapping; no custom decorator is created. SQL JOIN supports request names. Set operations are used only for unique shared words. The role selector is intentionally only a demo, not security.
