import pandas as pd
from datetime import date
from role_engine import score_job


MANUAL_JOB_FILE = "manual_jobs.csv"
SELECTED_JOB_FILE = "selected_job.csv"


def create_manual_job(title, company, location, link, description):
    job_dict = {
        "title": title,
        "company": company,
        "location": location,
        "description": description,
        "link": link,
        "source": "Manual",
        "date_found": date.today().isoformat()
    }

    role_result = score_job(job_dict)

    job_row = {
        "Title": title,
        "Company": company,
        "Location": location,
        "Source": "Manual",
        "Date Found": date.today().isoformat(),
        "Match Score": role_result["score"],
        "Priority": get_priority(role_result["score"]),
        "Primary Role": role_result["primary_role"],
        "Entry Level": role_result["entry_level"],
        "Senior Level": role_result["senior_level"],
        "Matched Role Groups": ", ".join(role_result["matched_role_groups"].keys()),
        "Matched Tech Keywords": ", ".join(role_result["matched_tech_keywords"]),
        "Matched Titles": ", ".join(role_result["matched_titles"]),
        "Application Status": "Not Applied",
        "Notes": "",
        "Link": link,
        "Description": description
    }

    return job_row


def get_priority(score):
    if score >= 70:
        return "High Priority"
    elif score >= 40:
        return "Medium Priority"
    else:
        return "Low Priority"


def save_manual_job(job_row):
    try:
        df = pd.read_csv(MANUAL_JOB_FILE)
        df = pd.concat([df, pd.DataFrame([job_row])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([job_row])

    df = df.drop_duplicates(subset=["Title", "Company", "Link"])
    df.to_csv(MANUAL_JOB_FILE, index=False)

    pd.DataFrame([job_row]).to_csv(SELECTED_JOB_FILE, index=False)

    return job_row

def delete_manual_job(title, company, link):
    try:
        df = pd.read_csv(MANUAL_JOB_FILE)
    except FileNotFoundError:
        return False

    before_count = len(df)

    df = df[
        ~(
            (df["Title"] == title) &
            (df["Company"] == company) &
            (df["Link"] == link)
        )
    ]

    df.to_csv(MANUAL_JOB_FILE, index=False)

    return len(df) < before_count