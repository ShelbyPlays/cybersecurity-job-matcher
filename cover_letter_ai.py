import os
import pandas as pd
from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=OPENAI_API_KEY)


YOUR_BACKGROUND = """
Shelby Deutsch is a cybersecurity professional based in Philadelphia, PA with a master's degree in Cybersecurity and a B.S. in Cybersecurity with a Digital Forensics Minor.

Core cybersecurity background:
- Digital forensics
- Threat hunting
- Authentication monitoring
- SIEM monitoring
- Incident response workflows
- Behavioral analytics
- Log analysis
- Security monitoring
- Threat detection

Technical tools:
- Microsoft Sentinel
- Splunk
- Wireshark
- Autopsy
- FTK Imager
- CrowdStrike Falcon
- Nmap
- Metasploit
- Burp Suite
- AWS
- Azure
- Linux
- Windows
- Python
- FastAPI
- SHAP
- XGBoost
- Random Forest
- SQL
- PowerShell
- Bash

Projects:
1. Explainable AI-Driven Anomaly Detection API for Authentication Logs
- Built a cybersecurity API to detect suspicious authentication behavior.
- Focused on failed logins, off-hours access, unique IP activity, credential misuse, and behavioral anomalies.
- Used explainable AI to make technical findings easier for investigators and non-technical stakeholders to understand.

2. Password Security Analysis & Awareness Tool
- Built a password security awareness tool focused on weak password habits, password reuse, predictable patterns, brute-force risk, and user education.
- Designed to show users why secure authentication practices matter.

Experience:
- Cybersecurity Graduate Assistant at Roger Williams University
- Cybersecurity Intern at Roger Williams University
- Cybersecurity & Digital Forensic Analysis Intern at Lincoln Investment

Important writing style:
- Natural and professional.
- Human sounding.
- Confident but not exaggerated.
- Do not sound like a generic AI cover letter.
- Do not simply repeat the job title over and over.
- Do not mention fitness or personal training.
"""


try:
    jobs = pd.read_csv("selected_job.csv")
    job = jobs.iloc[0]
except FileNotFoundError:
    jobs = pd.read_csv("matched_jobs_v3.csv")
    job = jobs.sort_values(by="Match Score", ascending=False).iloc[0]


job_title = job["Title"]
company = job["Company"]
location = job["Location"]
matched_keywords = job.get("Matched Tech Keywords", "")
matched_role_groups = job.get("Matched Role Groups", "")
primary_role = job.get("Primary Role", "")
missing_keywords = ""
link = job["Link"]


prompt = f"""
You are writing a professional cybersecurity cover letter for Shelby Deutsch.

Follow this exact writing style and structure:

STYLE EXAMPLE:
Dear Hiring Manager,

I am interested in the Special Agent position focused on cybersecurity and technology with the FBI. With a background in cybersecurity and digital forensics, I’ve developed hands-on experience in authentication monitoring, threat detection, and security investigations that has strengthened my interest in investigative cybersecurity work.

During my internships and graduate assistant experience, I worked with SIEM platforms such as Splunk and Microsoft Sentinel while supporting threat hunting and security monitoring initiatives. Reviewing authentication activity, investigating suspicious behavior, and assisting with incident response workflows helped me build a practical understanding of how technical findings support larger security investigations.

Outside of my internship experience, I’ve also built cybersecurity-focused projects centered around authentication security and user behavior. One project involved developing an explainable AI-driven API designed to identify suspicious authentication activity such as failed logins, off-hours access attempts, and credential misuse. I also created a password security analysis tool focused on helping users better understand weak password habits and authentication risks. These projects allowed me to strengthen both my technical abilities and my interest in cybersecurity work that combines investigation, analysis, and problem-solving.

I would welcome the opportunity to bring my technical background, analytical mindset, and eagerness to learn to your team. Thank you for your time and consideration, and I look forward to the possibility of speaking further.

Sincerely,

Shelby Deutsch

Now write a new cover letter for the selected job.

RULES:
- Follow the exact structure of the example.
- Keep 4 paragraphs.
- Start with “Dear Hiring Manager,” unless the job/company clearly gives another team name.
- Keep the tone grounded, direct, and early-career professional.
- Do not sound overly corporate.
- Do not sound motivational.
- Do not use em dashes.
- Do not use bullet points.
- Do not mention fitness, coaching, or personal training.
- Do not invent experience, certifications, clearance, or law enforcement employment.
- Mention the job title and company only once in the first paragraph.
- Keep the projects paragraph focused on Shelby’s two cybersecurity projects.
- End with “Sincerely,” and “Shelby Deutsch.”
- Return only the cover letter text.

JOB TITLE:
{job_title}

COMPANY:
{company}

LOCATION:
{location}

MATCHED KEYWORDS:
{matched_keywords}

MISSING KEYWORDS:
{missing_keywords}

PRIMARY ROLE:
{primary_role}

MATCHED ROLE GROUPS:
{matched_role_groups}

CANDIDATE BACKGROUND:
{YOUR_BACKGROUND}
"""


response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "system",
            "content": "You write natural, professional cybersecurity cover letters that do not sound AI-generated."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.65
)


cover_letter = response.choices[0].message.content


os.makedirs("cover_letters", exist_ok=True)


def safe_filename(text):
    return "".join(c if c.isalnum() else "_" for c in str(text))[:80]


filename = f"{safe_filename(company)}_{safe_filename(job_title)}_Cover_Letter.txt"

filepath = os.path.join(
    "cover_letters",
    filename
)


with open(filepath, "w", encoding="utf-8") as f:
    f.write(cover_letter)


with open("latest_cover_letter.txt", "w", encoding="utf-8") as f:
    f.write(cover_letter)


print("Cover letter created.")
print(f"Saved to {filepath}")
print("Also saved as latest_cover_letter.txt")