import os
import pandas as pd


TRACKER_FILE = "applications.csv"


STATUSES = [
    "Not Applied",
    "Applied",
    "Interviewing",
    "Rejected",
    "Offer",
    "Follow Up"
]


def load_applications():
    if os.path.exists(TRACKER_FILE):
        return pd.read_csv(TRACKER_FILE)

    return pd.DataFrame(columns=[
        "Title",
        "Company",
        "Location",
        "Source",
        "Status",
        "Notes",
        "Link"
    ])


def save_application(job, status, notes):
    apps = load_applications()

    title = job["Title"]
    company = job["Company"]
    link = job["Link"]

    existing = (
        (apps["Title"] == title) &
        (apps["Company"] == company) &
        (apps["Link"] == link)
    )

    new_row = {
        "Title": title,
        "Company": company,
        "Location": job.get("Location", ""),
        "Source": job.get("Source", ""),
        "Status": status,
        "Notes": notes,
        "Link": link
    }

    if existing.any():
        apps.loc[existing, :] = pd.DataFrame([new_row]).values
    else:
        apps = pd.concat([apps, pd.DataFrame([new_row])], ignore_index=True)

    apps.to_csv(TRACKER_FILE, index=False)


def get_status_for_job(job):
    apps = load_applications()

    if apps.empty:
        return "Not Applied", ""

    match = apps[
        (apps["Title"] == job["Title"]) &
        (apps["Company"] == job["Company"]) &
        (apps["Link"] == job["Link"])
    ]

    if match.empty:
        return "Not Applied", ""

    return match.iloc[0]["Status"], match.iloc[0]["Notes"]