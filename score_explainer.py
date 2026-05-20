def explain_score(job):
    reasons = []

    score = job.get("Match Score", 0)
    primary_role = job.get("Primary Role", "")
    role_groups = str(job.get("Matched Role Groups", ""))
    tech_keywords = str(job.get("Matched Tech Keywords", ""))
    matched_titles = str(job.get("Matched Titles", ""))

    if primary_role:
        reasons.append(f"Primary role match: {primary_role}")

    if role_groups:
        reasons.append(f"Matched role groups: {role_groups}")

    if tech_keywords:
        reasons.append(f"Matched technical keywords: {tech_keywords}")

    if matched_titles:
        reasons.append(f"Matched job title signals: {matched_titles}")

    if score >= 70:
        reasons.append("This is a strong match based on role alignment and keyword overlap.")
    elif score >= 40:
        reasons.append("This is a moderate match. It may be worth applying if the role responsibilities fit.")
    else:
        reasons.append("This is a weaker match and should be reviewed manually before applying.")

    return reasons