import json
import os
import pandas as pd
from openai import OpenAI


# ==========================================
# CONFIG
# ==========================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=OPENAI_API_KEY)


# ==========================================
# LOAD PARSED RESUME
# ==========================================

with open("parsed_resume.json", "r", encoding="utf-8") as f:
    parsed_resume = json.load(f)


# ==========================================
# LOAD SELECTED JOB
# ==========================================

try:
    jobs = pd.read_csv("selected_job.csv")
    top_job = jobs.iloc[0]
except FileNotFoundError:
    jobs = pd.read_csv("matched_jobs_v3.csv")
    top_job = jobs.sort_values(by="Match Score", ascending=False).iloc[0]


job_title = top_job["Title"]
company = top_job["Company"]
job_location = top_job["Location"]

job_keywords = top_job.get("Matched Tech Keywords", "")
primary_role = top_job.get("Primary Role", "GENERAL_CYBER")
matched_role_groups = top_job.get("Matched Role Groups", "")


# ==========================================
# ROLE-SPECIFIC FOCUS
# ==========================================

ROLE_FOCUS = {
    "DFIR": """
Emphasize digital forensics, investigations, evidence analysis, incident response, authentication monitoring, suspicious activity, forensic reporting, Autopsy, FTK Imager, and Wireshark. For FBI, CISA, and investigative cybersecurity roles, avoid making the AI project sound overly academic. Do not include ML performance metrics unless the job specifically asks for machine learning experience.
""",

    "SOC_ANALYST": """
Emphasize SIEM monitoring, Splunk, Microsoft Sentinel, security monitoring, threat hunting, alert triage, log analysis, authentication activity review, and incident response workflows.
""",

    "IAM_AUTH": """
Emphasize authentication monitoring, identity security, access control, MFA, SSO, credential misuse, login behavior, user authentication patterns, and authentication anomaly analysis.
""",

    "AI_SECURITY": """
Emphasize the Explainable AI Authentication Log Detection API, anomaly detection, behavioral analytics, SHAP, FastAPI, Python, machine learning, explainability, and risk scoring.
""",

    "CLOUD_SECURITY": """
Emphasize AWS, Azure, cloud security, cloud monitoring, security automation, identity controls, and cloud-based threat detection.
""",

    "VULNERABILITY": """
Emphasize vulnerability assessment, Nmap, Metasploit, Burp Suite, penetration testing concepts, risk identification, remediation support, and vulnerability analysis.
""",

    "GRC": """
Emphasize security policy, risk management, NIST, compliance, documentation, communication, translating security findings for stakeholders, and security awareness.
""",

    "GENERAL_CYBER": """
Emphasize cybersecurity fundamentals, threat detection, digital forensics, SIEM monitoring, authentication monitoring, incident response, security monitoring, and technical projects.
"""
}


RESUME_PROFILES = {
    "DFIR": {
        "priority_skills": [
            "Digital Forensics",
            "Incident Response",
            "Authentication Monitoring",
            "Log Analysis",
            "Autopsy",
            "FTK Imager",
            "Wireshark",
            "Evidence Analysis",
            "Investigative Workflows"
        ]
    },

    "SOC_ANALYST": {
        "priority_skills": [
            "SIEM Monitoring",
            "Splunk",
            "Microsoft Sentinel",
            "Threat Hunting",
            "Alert Triage",
            "Security Monitoring",
            "Log Analysis",
            "Incident Response"
        ]
    },

    "IAM_AUTH": {
        "priority_skills": [
            "Authentication Monitoring",
            "Identity Security",
            "Credential Misuse Detection",
            "Access Control",
            "Login Behavior Analysis",
            "MFA",
            "SSO",
            "Authentication Anomaly Analysis"
        ]
    },

    "AI_SECURITY": {
        "priority_skills": [
            "FastAPI",
            "SHAP",
            "Behavioral Analytics",
            "Anomaly Detection",
            "Authentication Analytics",
            "XGBoost",
            "Random Forest",
            "Python"
        ]
    },

    "CLOUD_SECURITY": {
        "priority_skills": [
            "AWS",
            "Azure",
            "Cloud Security",
            "Cloud Monitoring",
            "Security Automation",
            "Cloud-Based Threat Detection"
        ]
    },

    "VULNERABILITY": {
        "priority_skills": [
            "Vulnerability Assessment",
            "Nmap",
            "Metasploit",
            "Burp Suite",
            "Risk Identification",
            "Remediation Support"
        ]
    },

    "GRC": {
        "priority_skills": [
            "Risk Management",
            "Security Policy",
            "NIST",
            "Compliance",
            "Documentation",
            "Security Awareness",
            "Stakeholder Communication"
        ]
    },

    "GENERAL_CYBER": {
        "priority_skills": [
            "Threat Detection",
            "Digital Forensics",
            "SIEM Monitoring",
            "Authentication Monitoring",
            "Incident Response",
            "Security Monitoring",
            "Python",
            "AWS",
            "Azure"
        ]
    }
}


role_focus = ROLE_FOCUS.get(primary_role, ROLE_FOCUS["GENERAL_CYBER"])
profile = RESUME_PROFILES.get(primary_role, RESUME_PROFILES["GENERAL_CYBER"])
profile_skills = ", ".join(profile["priority_skills"])


# ==========================================
# AI PROMPT
# ==========================================

prompt = f"""
You are an elite cybersecurity resume optimization system.

Your job is to tailor the resume strategically WITHOUT rewriting the candidate's identity.

IMPORTANT RULES:
- Preserve the original structure.
- Preserve the original formatting style.
- Preserve the same sections.
- Preserve most bullet points.
- Keep the writing realistic and believable.
- Do NOT invent fake experience.
- Do NOT dramatically rewrite the resume.
- Only improve wording strategically.
- Only inject ATS keywords naturally.
- Reorder bullets if beneficial.
- Keep the tone technical and professional.
- Maintain cybersecurity focus.
- Keep Additional Experience unchanged.
- Keep Education unchanged.
- Keep Certifications unchanged.
- Avoid buzzword stacking in the summary.
- Keep the summary clear, direct, and believable for an early-career cybersecurity professional.
- Do not overuse phrases like "machine learning-based threat detection."
- Prefer "authentication anomaly analysis" when discussing the AI project.
- Do not include exact model performance metrics unless the job is specifically AI/ML focused.
- For DFIR, FBI, CISA, SOC, or government cyber roles, replace exact metrics like "91% accuracy, 89% precision, 93% recall, and 0.94 ROC-AUC" with a more practical impact statement.
- Use practical language such as "support real-time risk scoring workflows," "identify suspicious authentication behavior," and "support investigative reporting."
- Reorder Technical Skills so role priority skills appear earlier when possible.
- Reorder project and experience bullets so the most relevant bullets appear first.
- Keep every bullet believable and consistent with the original resume.
- Keep the summary to 3 sentences maximum.

JOB TITLE:
{job_title}

COMPANY:
{company}

LOCATION:
{job_location}

MATCHED JOB KEYWORDS:
{job_keywords}

PRIMARY ROLE TYPE:
{primary_role}

MATCHED ROLE GROUPS:
{matched_role_groups}

ROLE-SPECIFIC RESUME FOCUS:
{role_focus}

ROLE PRIORITY SKILLS:
{profile_skills}

CURRENT RESUME JSON:
{json.dumps(parsed_resume, indent=2)}

Generate:
1. Improved Professional Summary
2. Improved Technical Skills section
3. Improved Project bullets
4. Improved Experience bullets

Return ONLY valid JSON.

JSON FORMAT:
{{
    "SUMMARY": [],
    "TECHNICAL_SKILLS": [],
    "TECHNICAL_PROJECTS": [],
    "RELATED_EXPERIENCE": []
}}
"""


# ==========================================
# OPENAI REQUEST
# ==========================================

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "system",
            "content": "You are an elite ATS cybersecurity resume optimizer."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.4
)


output = response.choices[0].message.content


# ==========================================
# SAVE OUTPUT
# ==========================================

with open("tailored_resume.json", "w", encoding="utf-8") as f:
    f.write(output)

print("Tailored resume generation complete.")
print("Created tailored_resume.json")