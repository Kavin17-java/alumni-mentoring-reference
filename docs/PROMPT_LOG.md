# Prompt log template

Record real interactions only. Do not invent a response, verification, student contribution, commit or PR. Treat suggestions as drafts and independently check them.

## Entry

- Date:
- Student name:
- Feature:
- Structured prompt (Role, Context, Task, Constraints, Output):
- AI response or short summary:
- Verification performed (test run, manual check, source checked):
- Corrections made:
- Used or rejected, and why:
- Related commit or PR:

## Prompt example: feature planning

Role: Patient Python tutor for beginners.
Context: We are building a Flask and SQLite alumni demo. Only alumni who consent can be listed.
Task: Break search by industry, expertise, role and year into small implementation steps.
Constraints: Use simple Python loops, Flask and sqlite3; no external services.
Output: Numbered steps with function names and one check per step.

## Prompt example: explain an error

Role: Python debugging tutor.
Context: [Paste the exact error and a short relevant code sample.]
Task: Explain the error and suggest one small fix.
Constraints: Do not rewrite the whole project; explain at first-year level.
Output: Meaning, likely cause, fix, and a way to verify.

## Prompt example: test ideas

Role: Software tester using pytest.
Context: [Paste a validation function and exact rules.]
Task: Suggest normal, boundary and invalid-input cases.
Constraints: Each test checks one behavior and uses fictional data.
Output: Table of test name, input and expected result.

## Prompt example: code review

Role: Careful beginner-friendly reviewer.
Context: [Paste a function and its requirement.]
Task: Find correctness, validation and readability problems.
Constraints: Do not claim to have run code; distinguish observed issues from suggestions.
Output: Ordered findings with file/line and a suggested correction.

## Verification notes

For every response, record how it was checked and what changed. Never paste code that you cannot explain. Leave the fields above blank until an actual interaction or contribution occurs.
