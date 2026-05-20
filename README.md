# 🔐 Cybersecurity Job Matcher

An AI-powered cybersecurity job matching platform that aggregates cybersecurity jobs, scores role compatibility, generates tailored resumes and cover letters, tracks applications, and creates interview preparation material for each role.

Built specifically for cybersecurity-focused positions including:

* DFIR
* SOC
* Threat Hunting
* Cloud Security
* IAM
* Threat Intelligence
* AppSec / Product Security
* Security Engineering

---

# 🚀 Features

## 🔎 Cybersecurity Job Aggregation

Pulls jobs from multiple sources and filters for cybersecurity relevance using a custom role engine.

### Current Sources

* RemoteOK
* Remotive
* Greenhouse
* Lever
* USAJobs
* Arbeitnow
* Manual LinkedIn / Indeed / external job imports

---

## 🧠 AI Role Matching Engine

Custom scoring engine that:

* detects cybersecurity role alignment
* scores keyword overlap
* identifies role groups
* prioritizes entry-level cybersecurity roles
* filters unrelated/non-cyber jobs

### Supported Role Categories

* DFIR
* SOC Analyst
* IAM / Authentication Security
* Cloud Security
* AI Security
* AppSec / Product Security
* Vulnerability Management
* Threat Intelligence
* GRC
* General Cybersecurity

---

## 📄 AI Resume Tailoring

Automatically generates:

* tailored cybersecurity resumes
* ATS-optimized technical summaries
* role-specific technical skills
* project emphasis based on job alignment

Exports:

* DOCX
* PDF

---

## ✉️ AI Cover Letter Generation

Generates realistic, role-specific cybersecurity cover letters based on:

* job title
* role category
* matched keywords
* candidate background
* cybersecurity projects

Exports:

* DOCX
* PDF

---

## 🎤 AI Interview Preparation

Generates:

* technical interview questions
* behavioral interview questions
* STAR story outlines
* cybersecurity concepts to review
* role-specific talking points
* smart interviewer questions
* red flags / claims to avoid

---

## 📊 Interactive Dashboard

Built with Streamlit.

### Includes:

* dark-themed UI
* cybersecurity analytics dashboard
* role distribution graphs
* priority breakdowns
* source tracking
* skill analytics
* application tracker
* top match scoring explanations

---

## 📝 Application Tracking

Track:

* Not Applied
* Applied
* Interviewing
* Rejected
* Offer
* Follow Up

Stored locally using CSV persistence.

---

## 🔗 Manual Job Import

Paste jobs from:

* LinkedIn
* Indeed
* ZipRecruiter
* ClearanceJobs
* Dice
* other platforms

Then generate:

* tailored resume
* tailored cover letter
* interview prep

without requiring direct scraping.

---

# 🛠️ Tech Stack

## Frontend

* Streamlit
* Plotly

## Backend

* Python

## AI

* OpenAI API

## Data Processing

* Pandas

## Document Generation

* python-docx
* docx2pdf

---

# 📂 Project Structure

```text
job_matcher/
│
├── dashboard.py
├── fetch_jobs.py
├── main.py
├── role_engine.py
├── tailor_resume.py
├── cover_letter_ai.py
├── interview_prep_ai.py
├── export_resume.py
├── export_cover_letter.py
├── convert_resume_to_pdf.py
├── convert_cover_letter_to_pdf.py
├── application_tracker.py
├── manual_job_input.py
├── score_explainer.py
│
├── resumes/
├── cover_letters/
├── pdf_resumes/
├── pdf_cover_letters/
├── interview_prep/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/job_matcher.git
cd job_matcher
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variable

### Windows PowerShell

```powershell
$env:OPENAI_API_KEY="your_openai_api_key"
```

---

# ▶️ Running the App

## Fetch Jobs

```bash
python fetch_jobs.py
python main.py
```

---

## Launch Dashboard

```bash
streamlit run dashboard.py
```

---

# 📈 Future Improvements

* Additional job source integrations
* Automated URL parsing
* Browser extension integration
* Cloud deployment
* Docker containerization
* AI skill gap analysis
* Resume version management
* Auto-generated networking outreach
* AI application ranking
* Email integration
* Recruiter CRM tools

---

# 📌 Disclaimer

This project is intended for educational and portfolio purposes.

The application avoids:

* bypassing authentication systems
* CAPTCHA circumvention
* unauthorized scraping
* automated spam applications

Manual job import is used for platforms with stricter usage policies.

---

# 👨‍💻 Author

Shelby Deutsch

Cybersecurity | Digital Forensics | Threat Detection | AI Security | Authentication Monitoring
