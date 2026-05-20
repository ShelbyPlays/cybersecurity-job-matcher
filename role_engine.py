import re


ROLE_GROUPS = {
    "GENERAL_CYBER": [
        "cybersecurity",
        "cyber security",
        "information security",
        "infosec",
        "information systems security",
        "it cybersecurity",
        "security operations",
        "security specialist",
        "cybersecurity specialist",
        "it cybersecurity specialist",
        "security administrator",
        "security technician",
        "security support",
        "cyber operations",
        "network security",
        "security engineering",
        "cyber defense",
        "security compliance",
        "security advisor",
        "protective security",
        "cybersecurity technology"
    ],
    
    "APP_PRODUCT_SECURITY": [
      "product security",
        "application security",
        "appsec",
        "secure code review",
        "security code review",
        "threat modeling",
        "architecture review",
        "security architecture",
        "owasp",
        "web application security",
        "cloud infrastructure",
        "aws permissions",
        "s3",
        "iam",
        "security testing",
        "secure system design",
        "security assessment"
    ],
    

    "SOC_ANALYST": [
        "soc analyst",
        "security operations analyst",
        "security analyst",
        "cybersecurity analyst",
        "information security analyst",
        "security monitoring",
        "siem analyst",
        "blue team",
        "threat analyst",
        "security operations center",
        "monitoring",
        "log analysis"
    ],

    "DFIR": [
        "digital forensics",
        "dfir",
        "incident response",
        "incident responder",
        "forensic analyst",
        "cyber investigator",
        "cyber investigations",
        "malware analysis",
        "evidence analysis",
        "computer forensics",
        "special agent",
        "investigation",
        "investigative",
        "forensic"
    ],

"CTI": [
    "cyber threat intelligence",
    "threat intelligence",
    "cti",
    "intelligence analyst",
    "threat intel",
    "ioc",
    "indicators of compromise",
    "tactics techniques and procedures",
    "ttps",
    "mitre att&ck",
    "threat actor",
    "osint",
    "malware intelligence",
    "cyber intelligence",
    "intelligence reporting"
],
    "IAM_AUTH": [
        "identity and access management",
        "iam",
        "iam analyst",
        "authentication security",
        "authentication",
        "identity security",
        "access control",
        "single sign-on",
        "sso",
        "mfa",
        "multi-factor authentication",
        "okta",
        "active directory"
    ],

    "CLOUD_SECURITY": [
        "cloud security",
        "aws security",
        "azure security",
        "cloud detection",
        "cloud infrastructure security",
        "security automation",
        "cloud incident response"
    ],

    "AI_SECURITY": [
        "ai security",
        "machine learning security",
        "machine learning",
        "anomaly detection",
        "behavioral analytics",
        "fraud detection",
        "explainable ai",
        "xai",
        "model monitoring"
    ],

    "VULNERABILITY": [
        "vulnerability analyst",
        "vulnerability management",
        "vulnerability assessment",
        "vulnerability",
        "penetration testing",
        "pentest",
        "application security",
        "appsec",
        "burp suite",
        "nmap",
        "metasploit"
    ],

    "GRC": [
        "grc",
        "risk analyst",
        "security compliance",
        "information assurance",
        "security policy",
        "nist",
        "governance risk compliance",
        "risk management"
    ]
}


TECH_KEYWORDS = [
    "splunk",
    "microsoft sentinel",
    "sentinel",
    "siem",
    "crowdstrike",
    "wireshark",
    "autopsy",
    "ftk",
    "ftk imager",
    "nmap",
    "metasploit",
    "burp suite",
    "python",
    "fastapi",
    "powershell",
    "bash",
    "sql",
    "aws",
    "azure",
    "linux",
    "windows",
    "json",
    "pandas",
    "xgboost",
    "random forest",
    "owasp",
    "s3",
    "iam",
    "java",
    "coverity",
    "shap",
    "mitre att&ck",
    "ioc",
    "osint",
    "threat intelligence",
    "malware",
    "yara",
    "virustotal"
]


RELATED_TITLES = [
    "cybersecurity analyst",
    "cyber security analyst",
    "security analyst",
    "information security analyst",
    "soc analyst",
    "security operations analyst",
    "threat analyst",
    "threat hunting analyst",
    "incident response analyst",
    "dfir analyst",
    "digital forensics analyst",
    "cyber investigator",
    "vulnerability analyst",
    "iam analyst",
    "identity analyst",
    "cloud security analyst",
    "security consultant",
    "security engineer",
    "detection engineer",
    "security monitoring analyst",
    "cybersecurity specialist",
    "it cybersecurity specialist",
    "infosec analyst",
    "information systems security officer",
    "isso",
    "cyber operations specialist",
    "security operations specialist",
    "security administrator",
    "special agent",
    "cyber special agent",
    "protective security advisor"
    "federal bureau of investigation",
    "fbi",
    "special agent cybersecurity",
    "cybersecurity special agent",
    "technology background",
    "special agent cybersecurity technology",
    "threat investigations",
    "security investigations",
    "authentication monitoring",
    "product security engineer",
    "application security engineer",
    "appsec engineer",
    "cloud security engineer",
    "security architecture engineer",
    "security engineer"
    "log analysis",
    "cyber threat intelligence intern",
    "cyber threat intelligence analyst",
    "threat intelligence intern",
    "threat intelligence analyst",
    "cti analyst",
    "cyber intelligence analyst",
    "intelligence analyst",
    "osint analyst",
    "security intelligence analyst"
]


ENTRY_LEVEL_TERMS = [
    "entry level",
    "entry-level",
    "junior",
    "associate",
    "new graduate",
    "recent graduate",
    "early career",
    "0-2 years",
    "0 to 2 years",
    "1-2 years",
    "1 to 2 years",
    "intern",
    "trainee"
]


SENIOR_TERMS = [
    "senior",
    "sr.",
    "sr ",
    "lead",
    "principal",
    "staff",
    "manager",
    "director",
    "head of",
    "architect",
    "vp ",
    "vice president"
]


HARD_EXCLUDE_TERMS = [
    "counsel",
    "attorney",
    "lawyer",
    "legal",
    "sales",
    "marketing",
    "recruiter",
    "talent",
    "human resources",
    "finance",
    "accounting",
    "designer",
    "product manager",
    "customer support",
    "customer success",
    "content",
    "social media",
    "communications",
    "paralegal",
    "trader",
    "tax",
    "hospitality",
    "coordinator"
    "editor",
    "consulting",
    "financial",
    "finance",
    "berater",
    "praktikum",
    "trainee",
    "hospitality",
    "internship",
    "customer",
    "hr",
    "account manager",
    "salesforce",
    "tax",
    "journalist",
    "media",
    "copywriter"
]


def normalize_text(text):
    return str(text).lower()


def contains_phrase(text, phrase):
    pattern = r"\b" + re.escape(phrase.lower()) + r"\b"
    return re.search(pattern, text) is not None


def get_job_text(job):
    return normalize_text(
        f"{job.get('title', '')} "
        f"{job.get('company', '')} "
        f"{job.get('location', '')} "
        f"{job.get('description', '')}"
    )


def detect_role_groups(job):
    text = get_job_text(job)
    matched_groups = {}

    for group_name, keywords in ROLE_GROUPS.items():
        matches = []

        for keyword in keywords:
            if contains_phrase(text, keyword):
                matches.append(keyword)

        if matches:
            matched_groups[group_name] = matches

    return matched_groups


def detect_tech_keywords(job):
    text = get_job_text(job)
    matches = []

    for keyword in TECH_KEYWORDS:
        if contains_phrase(text, keyword):
            matches.append(keyword)

    return matches


def detect_related_titles(job):
    title = normalize_text(job.get("title", ""))
    matches = []

    for related_title in RELATED_TITLES:
        if contains_phrase(title, related_title):
            matches.append(related_title)

    return matches


def is_entry_level(job):
    text = get_job_text(job)

    return any(
        contains_phrase(text, term)
        for term in ENTRY_LEVEL_TERMS
    )


def is_senior_level(job):
    text = normalize_text(
        f"{job.get('title', '')} {job.get('description', '')}"
    )

    return any(
        term in text
        for term in SENIOR_TERMS
    )


def is_hard_excluded(job):
    text = normalize_text(
        f"{job.get('title', '')} {job.get('description', '')}"
    )

    return any(
        term in text
        for term in HARD_EXCLUDE_TERMS
    )


def get_primary_role_group(job):
    matched_groups = detect_role_groups(job)

    if not matched_groups:
        return "GENERAL_CYBER"

    return max(
        matched_groups,
        key=lambda group: len(matched_groups[group])
    )


def score_job(job):
    matched_groups = detect_role_groups(job)
    tech_matches = detect_tech_keywords(job)
    title_matches = detect_related_titles(job)

    score = 0

    for group_name, matches in matched_groups.items():
        if group_name == "GENERAL_CYBER":
            score += len(matches) * 5
        else:
            score += len(matches) * 10

    score += len(tech_matches) * 4
    score += len(title_matches) * 12

    if is_entry_level(job):
        score += 15

    if is_senior_level(job):
        score -= 15

    if is_hard_excluded(job):
        score -= 50

    score = max(score, 0)
    score = min(score, 100)

    primary_role = get_primary_role_group(job)

    return {
        "score": score,
        "primary_role": primary_role,
        "matched_role_groups": matched_groups,
        "matched_tech_keywords": tech_matches,
        "matched_titles": title_matches,
        "entry_level": is_entry_level(job),
        "senior_level": is_senior_level(job),
        "hard_excluded": is_hard_excluded(job)
    }


def is_relevant_cyber_job(job, minimum_score=25):
    result = score_job(job)

    if result["hard_excluded"]:
        return False

    if result["senior_level"]:
        return False

    matched_groups = result["matched_role_groups"]

    # Allow cybersecurity internships if they match a real cyber role group
    if result["entry_level"] and matched_groups:
        return result["score"] >= 15

    return result["score"] >= minimum_score