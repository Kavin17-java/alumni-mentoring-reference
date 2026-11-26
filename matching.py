"""Explainable rule-based mentor recommendations."""


def keywords(text):
    words = set()
    for word in text.split(","):
        cleaned = word.strip().lower()
        if cleaned:
            words.add(cleaned)
    return words


def score_alumni(student, alumni):
    shared = keywords(student["interests"]) & keywords(alumni["expertise"])
    industry_match = student["target_industry"].strip().lower() == alumni["industry"].strip().lower()
    score = len(shared) + (3 if industry_match else 0)
    reasons = []
    if industry_match:
        reasons.append("same industry (+3)")
    for word in sorted(shared):
        reasons.append(word + " (+1)")
    return score, reasons


def suggest_mentors(student, alumni_list):
    suggestions = []
    for alumni in alumni_list:
        if alumni["consent"]:
            score, reasons = score_alumni(student, alumni)
            if score > 0:
                suggestions.append({"alumni": alumni, "score": score, "reasons": reasons})
    suggestions.sort(key=lambda item: item["score"], reverse=True)
    return suggestions[:3]
