import requests
import re
import pandas as pd
from datetime import date
from role_engine import score_job, is_relevant_cyber_job

try:
    from company_boards import GREENHOUSE_COMPANIES, LEVER_COMPANIES
except ImportError:
    GREENHOUSE_COMPANIES = ["wizinc", "cloudflare", "okta"]
    LEVER_COMPANIES = []

try:
    from config import USAJOBS_EMAIL, USAJOBS_API_KEY
except ImportError:
    USAJOBS_EMAIL = None
    USAJOBS_API_KEY = None


EXCLUDE_TERMS = [
    "senior", "sr.", "sr ", "lead", "principal", "staff",
    "manager", "director", "head of", "architect", "vp ", "vice president"
]

HARD_EXCLUDE_TITLES = [
    "counsel", "attorney", "lawyer", "legal", "sales", "marketing",
    "recruiter", "talent", "human resources", "finance", "accounting",
    "designer", "product manager", "customer support", "customer success",
    "content", "social media", "communications", "paralegal", "trader", "tax"
]

OUTSIDE_US_TERMS = [
    "europe", "emea", "uk", "united kingdom", "germany", "france",
    "spain", "netherlands", "canada", "australia", "india", "asia", "latin america"
]

LOCAL_TERMS = [
    "philadelphia", "philly", "greater philadelphia", "philadelphia area",
    "philadelphia, pa", "pennsylvania", "pa", "king of prussia", "kop",
    "conshohocken", "malvern", "exton", "west chester", "wayne", "radnor",
    "wilmington", "delaware", "de", "camden", "cherry hill",
    "new jersey", "nj", "south jersey"
]

ALLOWED_LOCATIONS = [
    "united states",
    "usa",
    "remote",
    "washington",
    "maryland",
    "virginia",
    "pennsylvania",
    "new york",
    "new jersey"
]

def clean_text(text):
    return str(text).lower()


def fetch_remoteok_raw_jobs():
    jobs = []
    try:
        response = requests.get(
            "https://remoteok.com/api",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        for item in data:
            if isinstance(item, dict):
                jobs.append({
                    "title": item.get("position", ""),
                    "company": item.get("company", ""),
                    "location": item.get("location", "Remote"),
                    "description": item.get("description", ""),
                    "link": item.get("url", ""),
                    "source": "RemoteOK",
                    "date_found": date.today().isoformat()
                })
    except Exception as e:
        print(f"RemoteOK error: {e}")

    return jobs


def fetch_remotive_raw_jobs():
    jobs = []
    try:
        response = requests.get(
            "https://remotive.com/api/remote-jobs",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        for item in data.get("jobs", []):
            jobs.append({
                "title": item.get("title", ""),
                "company": item.get("company_name", ""),
                "location": item.get("candidate_required_location", "Remote"),
                "description": item.get("description", ""),
                "link": item.get("url", ""),
                "source": "Remotive",
                "date_found": date.today().isoformat()
            })
    except Exception as e:
        print(f"Remotive error: {e}")

    return jobs


def fetch_arbeitnow_raw_jobs():
    jobs = []
    try:
        response = requests.get(
            "https://www.arbeitnow.com/api/job-board-api",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        for item in data.get("data", []):
            jobs.append({
                "title": item.get("title", ""),
                "company": item.get("company_name", ""),
                "location": item.get("location", ""),
                "description": item.get("description", ""),
                "link": item.get("url", ""),
                "source": "Arbeitnow",
                "date_found": date.today().isoformat()
            })
    except Exception as e:
        print(f"Arbeitnow error: {e}")

    return jobs


def fetch_greenhouse_jobs():
    jobs = []

    for company_slug in GREENHOUSE_COMPANIES:
        url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs?content=true"

        try:
            response = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            response.raise_for_status()
            data = response.json()

            for item in data.get("jobs", []):
                location = ""
                if item.get("location"):
                    location = item["location"].get("name", "")

                jobs.append({
                    "title": item.get("title", ""),
                    "company": company_slug,
                    "location": location,
                    "description": item.get("content", ""),
                    "link": item.get("absolute_url", ""),
                    "source": "Greenhouse",
                    "date_found": date.today().isoformat()
                })

        except Exception as e:
            print(f"Greenhouse error for {company_slug}: {e}")

    return jobs


def fetch_lever_jobs():
    jobs = []

    for company_slug in LEVER_COMPANIES:
        url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"

        try:
            response = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            response.raise_for_status()
            data = response.json()

            for item in data:
                jobs.append({
                    "title": item.get("text", ""),
                    "company": company_slug,
                    "location": item.get("categories", {}).get("location", ""),
                    "description": item.get("descriptionPlain", ""),
                    "link": item.get("hostedUrl", ""),
                    "source": "Lever",
                    "date_found": date.today().isoformat()
                })

        except Exception as e:
            print(f"Lever error for {company_slug}: {e}")

    return jobs


def fetch_usajobs_jobs():
    jobs = []

    if not USAJOBS_EMAIL or not USAJOBS_API_KEY:
        print("USAJobs config missing. Skipping USAJobs.")
        return jobs

    url = "https://data.usajobs.gov/api/search"

    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": USAJOBS_EMAIL,
        "Authorization-Key": USAJOBS_API_KEY
    }

    params = {
        "Keyword": "cybersecurity",
        "LocationName": "United States",
        "ResultsPerPage": 50
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        search_results = data.get("SearchResult", {}).get("SearchResultItems", [])

        for item in search_results:
            job_data = item.get("MatchedObjectDescriptor", {})

            jobs.append({
                "title": job_data.get("PositionTitle", ""),
                "company": job_data.get("OrganizationName", "USAJobs"),
                "location": job_data.get("PositionLocationDisplay", ""),
                "description": job_data.get("QualificationSummary", ""),
                "link": job_data.get("PositionURI", ""),
                "source": "USAJobs",
                "date_found": date.today().isoformat()
            })

    except Exception as e:
        print(f"USAJobs error: {e}")

    return jobs


def is_cyber_related(job):
    text = clean_text(f"{job['title']} {job['company']} {job['description']}")

    cyber_terms = [
        "cybersecurity", "cyber security", "information security",
        "security analyst", "soc", "siem", "splunk", "microsoft sentinel",
        "incident response", "threat", "digital forensics", "dfir",
        "vulnerability", "iam", "identity access", "authentication",
        "network security", "cloud security", "blue team", "security operations", 
    ]

    return any(term in text for term in cyber_terms)


def is_not_senior(job):
    text = clean_text(f"{job['title']} {job['description']}")
    return not any(term in text for term in EXCLUDE_TERMS)


def passes_hard_exclude(job):
    text = clean_text(f"{job['title']} {job['description']}")
    return not any(term in text for term in HARD_EXCLUDE_TITLES)


def is_local_area(job):
    text = clean_text(f"{job['location']} {job['description']}")
    return any(term in text for term in LOCAL_TERMS)


def is_remote(job):
    text = clean_text(f"{job['location']} {job['description']}")
    return "remote" in text


def is_clearly_outside_us(job):
    text = clean_text(f"{job['location']} {job['description']}")
    return any(term in text for term in OUTSIDE_US_TERMS)


def passes_location_rules(job):
    if is_local_area(job):
        return True

    if is_remote(job) and not is_clearly_outside_us(job):
        return True

    return False


def filter_jobs(raw_jobs):
    strict_filtered = []
    relaxed_filtered = []

    for job in raw_jobs:

        if not is_relevant_cyber_job(job):
            continue

        role_result = score_job(job)

        job["role_score"] = role_result["score"]
        job["primary_role"] = role_result["primary_role"]

        job["matched_role_groups"] = ", ".join(
            role_result["matched_role_groups"].keys()
        )

        job["matched_tech_keywords"] = ", ".join(
            role_result["matched_tech_keywords"]
        )

        if passes_location_rules(job):
            strict_filtered.append(job)
        else:
            job["location_note"] = "Review location manually"
            relaxed_filtered.append(job)

    strict_filtered.sort(
        key=lambda x: x["role_score"],
        reverse=True
    )

    relaxed_filtered.sort(
        key=lambda x: x["role_score"],
        reverse=True
    )

    if strict_filtered:
        print(f"Strict location matches found: {len(strict_filtered)}")
        return strict_filtered

    print("No strict location matches found.")
    print(
        f"Using relaxed cybersecurity matches for manual review: "
        f"{len(relaxed_filtered)}"
    )

    return relaxed_filtered

    print("No strict location matches found.")
    print(f"Using relaxed cybersecurity matches for manual review: {len(relaxed_filtered)}")
    return relaxed_filtered


def update_saved_jobs(df):
    try:
        old_jobs = pd.read_csv("saved_jobs.csv")

        if old_jobs.empty:
            combined_jobs = df
        else:
            combined_jobs = pd.concat([old_jobs, df], ignore_index=True)

    except (FileNotFoundError, pd.errors.EmptyDataError):
        combined_jobs = df

    combined_jobs = combined_jobs.drop_duplicates(
        subset=["title", "company", "link"]
    )

    combined_jobs.to_csv("saved_jobs.csv", index=False)

    return combined_jobs


def main():
    print("Fetching raw jobs...")

    all_raw_jobs = []

    remoteok_jobs = fetch_remoteok_raw_jobs()
    print(f"RemoteOK raw jobs: {len(remoteok_jobs)}")
    all_raw_jobs.extend(remoteok_jobs)

    remotive_jobs = fetch_remotive_raw_jobs()
    print(f"Remotive raw jobs: {len(remotive_jobs)}")
    all_raw_jobs.extend(remotive_jobs)

    # arbeitnow_jobs = fetch_arbeitnow_raw_jobs()
    # print(f"Arbeitnow raw jobs: {len(arbeitnow_jobs)}")
    # all_raw_jobs.extend(arbeitnow_jobs)

    greenhouse_jobs = fetch_greenhouse_jobs()
    print(f"Greenhouse raw jobs: {len(greenhouse_jobs)}")
    all_raw_jobs.extend(greenhouse_jobs)

    lever_jobs = fetch_lever_jobs()
    print(f"Lever raw jobs: {len(lever_jobs)}")
    all_raw_jobs.extend(lever_jobs)

    usajobs_jobs = fetch_usajobs_jobs()
    print(f"USAJobs raw jobs: {len(usajobs_jobs)}")
    all_raw_jobs.extend(usajobs_jobs)

    if not all_raw_jobs:
        print("No raw jobs returned.")
        return

    raw_df = pd.DataFrame(all_raw_jobs)
    raw_df = raw_df.drop_duplicates(subset=["title", "company", "link"])
    raw_df.to_csv("raw_jobs_debug.csv", index=False)

    filtered_jobs = filter_jobs(all_raw_jobs)

    if not filtered_jobs:
        print("No filtered cybersecurity jobs found.")
        print("Raw jobs saved to raw_jobs_debug.csv for review.")
        return

    df = pd.DataFrame(filtered_jobs)
    df = df.drop_duplicates(subset=["title", "company", "link"])

    df.to_csv("jobs.csv", index=False)

    combined_jobs = update_saved_jobs(df)

    print(f"Filtered jobs found: {len(df)}")
    print(f"Saved total historical jobs: {len(combined_jobs)}")
    print("Created jobs.csv")
    print("Updated saved_jobs.csv")
    print("Raw jobs also saved to raw_jobs_debug.csv")


if __name__ == "__main__":
    main()