# Team work plan

## Ownership

| Member | Learn and own | Main interfaces |
|---|---|---|
| A | SQLite foundation, validators, student/alumni forms, consent, sample data | initialize_database(), load_sample_data(), validate_*, create_student(), create_alumni(); database.py, profiles.py, validators.py and profile templates |
| B | Directory filters, matching rule, search and matching tests, CI | search_alumni(filters), score_alumni(student, alumni), suggest_mentors(student, alumni_list); search.py, matching.py and workflow |
| C | Requests, allowed statuses, report arithmetic and CSV, deployment notes | create_request(student_id, alumni_id, message), update_request_status(request_id, status), participation_report(), report_csv(report); request/report modules and templates |

All three learn app.py route wiring and Flask forms. Every member contributes implementation, interface and tests to their feature. These are suggested responsibilities, not a record of work completed by named students.

## Order and integration

1. Member A creates tables, validators and fictional samples. Agree on table column names before others build on them.
2. Member B builds search and matching using the agreed row fields; add CI early.
3. Member C builds requests and reports using student/alumni IDs and request statuses.
4. Connect each feature through app.py routes and templates. The reusable function signatures above are integration contracts.
5. Each member writes tests and a small README/doc update with their feature.
6. Work on separate feature branches; use small pull requests and the review cycle A reviews B, B reviews C, C reviews A. Never claim a review happened unless it did.
7. Resolve shared app.py conflicts together: pull current main, compare route changes, retain both routes, then run the complete tests.

Suggested commits: schema and sample data; server validation; profile forms; directory filters; match scoring; request rules; reports and CSV; tests and workflow; documentation and styling. See README for GitHub setup, PR and branch protection steps.
