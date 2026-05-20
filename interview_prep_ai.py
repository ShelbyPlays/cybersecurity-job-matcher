import os
import pandas as pd
from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=OPENAI_API_KEY)


try:
    jobs = pd.read_csv("selected_job.csv")
    job = jobs.iloc[0]
except FileNotFoundError:
    jobs = pd.read_csv("matched_jobs_v3.csv")
    job = jobs.sort_values(by="Match Score", ascending=False).iloc[0]


job_title = job["Title"]
company = job["Company"]
primary_role = job.get("Primary Role", "GENERAL_CYBER")
matched_role_groups = job.get("Matched Role Groups", "")
matched_keywords = job.get("Matched Tech Keywords", "")


BACKGROUND = """
Shelby Deutsch has a master's degree in Cybersecurity and a B.S. in Cybersecurity with a Digital Forensics Minor.

Experience includes:
- Cybersecurity Graduate Assistant
- Cybersecurity Intern
- Cybersecurity & Digital Forensic Analysis Intern

Skills include:
- Digital forensics
- Threat hunting
- Authentication monitoring
- SIEM monitoring
- Incident response workflows
- Log analysis
- Microsoft Sentinel
- Splunk
- Wireshark
- Autopsy
- FTK Imager
- Python
- FastAPI
- AWS
- Azure

Projects:
- Explainable AI-Driven Anomaly Detection API for Authentication Logs
- Password Security Analysis & Awareness Tool
"""


prompt = f"""
Create interview prep for this role.

JOB TITLE:
{job_title}

COMPANY:
{company}

PRIMARY ROLE:
{primary_role}

MATCHED ROLE GROUPS:
{matched_role_groups}

MATCHED KEYWORDS:
{matched_keywords}

CANDIDATE BACKGROUND:
{BACKGROUND}

Generate:

1. Role Summary
2. 8 Likely Technical Questions
3. 6 Likely Behavioral Questions
4. 5 STAR Story Outlines based only on Shelby's real experience
5. Skills to Review Before Interview
6. 5 Smart Questions to Ask the Interviewer
7. Red Flags or Claims to Avoid Saying

Rules:

- Keep it practical.
- Make it specific to cybersecurity.
- Do not invent fake experience.
- Do not claim Shelby performed work that is not confirmed.
- Do not say Shelby improved detection accuracy, reduced false positives, handled a ransomware incident, or worked a real compromised-device case unless clearly stated.
- For STAR stories, frame them as talking-point outlines, not completed claims.
- Use phrases like “could discuss,” “can frame,” and “example angle” when appropriate.
- Make answers fit early-career cybersecurity roles.
- Include strong talking points based on Shelby's projects.
- Keep language clear and direct.
"""


response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a cybersecurity interview coach."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.5
)


output = response.choices[0].message.content


os.makedirs("interview_prep", exist_ok=True)


def safe_filename(text):
    return "".join(c if c.isalnum() else "_" for c in str(text))[:80]


filename = f"{safe_filename(company)}_{safe_filename(job_title)}_Interview_Prep.txt"
filepath = os.path.join("interview_prep", filename)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(output)

with open("latest_interview_prep.txt", "w", encoding="utf-8") as f:
    f.write(output)

print("Interview prep created.")
print(f"Saved to {filepath}")