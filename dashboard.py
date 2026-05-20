import streamlit as st
import pandas as pd
import subprocess
import os

from application_tracker import (
    STATUSES,
    save_application,
    get_status_for_job,
    load_applications
)

from manual_job_input import (
    create_manual_job,
    save_manual_job,
    delete_manual_job
)

from score_explainer import explain_score


# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Cybersecurity Job Matcher",
    page_icon="🔐",
    layout="wide"
)


# ==============================
# CUSTOM CSS
# ==============================

st.markdown("""
<style>
    .stApp {
        background-color: #0f141b;
        color: #f1f5f9;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #243244;
    }

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 15px;
        color: #94a3b8;
        margin-bottom: 24px;
    }

    .metric-card {
        background: linear-gradient(135deg, #111827, #1e293b);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    }

    .metric-label {
        font-size: 13px;
        color: #94a3b8;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 800;
        color: #f8fafc;
    }

    .section-card {
        background-color: #111827;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 22px;
        margin-top: 18px;
        margin-bottom: 18px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.18);
    }

    .small-muted {
        color: #94a3b8;
        font-size: 13px;
    }

    .job-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        background-color: #1d4ed8;
        color: white;
        font-size: 12px;
        font-weight: 600;
        margin-right: 6px;
    }

    .high-pill {
        background-color: #15803d;
    }

    .medium-pill {
        background-color: #ca8a04;
    }

    .low-pill {
        background-color: #b91c1c;
    }

    h1, h2, h3 {
        color: #f8fafc;
    }

    .stDataFrame {
        border-radius: 14px;
        overflow: hidden;
    }

    div[data-testid="stExpander"] {
        background-color: #111827;
        border: 1px solid #334155;
        border-radius: 12px;
    }

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #2563eb;
        background-color: #1d4ed8;
        color: white;
        font-weight: 600;
    }

    .stDownloadButton > button {
        border-radius: 10px;
        border: 1px solid #16a34a;
        background-color: #15803d;
        color: white;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ==============================
# HELPERS
# ==============================

@st.cache_data
def load_data():
    return pd.read_csv("matched_jobs_v3.csv")


def load_manual_jobs():
    if os.path.exists("manual_jobs.csv"):
        return pd.read_csv("manual_jobs.csv")
    return pd.DataFrame()


def merge_manual_jobs(df):
    manual_df = load_manual_jobs()

    if not manual_df.empty:
        df = pd.concat([df, manual_df], ignore_index=True)
        df = df.drop_duplicates(subset=["Title", "Company", "Link"])

    return df


def merge_application_status(df):
    applications_df = load_applications()

    if not applications_df.empty:
        df = df.merge(
            applications_df[["Title", "Company", "Link", "Status", "Notes"]],
            on=["Title", "Company", "Link"],
            how="left",
            suffixes=("", "_tracker")
        )

        if "Application Status" in df.columns:
            df["Application Status"] = df["Status"].fillna(df["Application Status"])
        else:
            df["Application Status"] = df["Status"].fillna("Not Applied")

        if "Notes" in df.columns:
            df["Notes"] = df["Notes_tracker"].fillna(df["Notes"])
        else:
            df["Notes"] = df["Notes_tracker"].fillna("")

        df = df.drop(columns=["Status", "Notes_tracker"])

    return df


def priority_badge(priority):
    if priority == "High Priority":
        return "high-pill"
    elif priority == "Medium Priority":
        return "medium-pill"
    return "low-pill"


def latest_file(folder, extension):
    if not os.path.exists(folder):
        return None

    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(extension)
    ]

    if not files:
        return None

    return max(files, key=os.path.getmtime)


# ==============================
# LOAD DATA
# ==============================

try:
    df = load_data()
except FileNotFoundError:
    st.error("matched_jobs_v3.csv not found. Run python main.py first.")
    st.stop()

df = merge_manual_jobs(df)
df = merge_application_status(df)


# ==============================
# HEADER
# ==============================

st.markdown('<div class="main-title">🔐 Cybersecurity Job Matcher</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Find cyber roles, score matches, generate tailored resumes, cover letters, and interview prep.</div>',
    unsafe_allow_html=True
)


# ==============================
# SIDEBAR
# ==============================

st.sidebar.title("🔐 Cyber Job Matcher")
st.sidebar.caption("Application platform for cybersecurity roles")

st.sidebar.divider()

st.sidebar.header("Generate Materials")

job_options = df["Title"] + " — " + df["Company"]

selected_job = st.sidebar.selectbox(
    "Select job",
    options=job_options
)

selected_index = job_options[job_options == selected_job].index[0]

if st.sidebar.button("Generate Tailored Resume"):
    df.iloc[[selected_index]].to_csv("selected_job.csv", index=False)

    with st.spinner("Generating tailored resume..."):
        subprocess.run(["python", "tailor_resume.py"], check=True)
        subprocess.run(["python", "export_resume.py"], check=True)

        if os.path.exists("convert_resume_to_pdf.py"):
            subprocess.run(["python", "convert_resume_to_pdf.py"], check=True)

    st.sidebar.success("Tailored resume created.")


if st.sidebar.button("Generate Cover Letter"):
    df.iloc[[selected_index]].to_csv("selected_job.csv", index=False)

    with st.spinner("Generating cover letter..."):
        subprocess.run(["python", "cover_letter_ai.py"], check=True)
        subprocess.run(["python", "export_cover_letter.py"], check=True)

        if os.path.exists("convert_cover_letter_to_pdf.py"):
            subprocess.run(["python", "convert_cover_letter_to_pdf.py"], check=True)

    st.sidebar.success("Cover letter created.")


if st.sidebar.button("Generate Interview Prep"):
    df.iloc[[selected_index]].to_csv("selected_job.csv", index=False)

    with st.spinner("Generating interview prep..."):
        subprocess.run(["python", "interview_prep_ai.py"], check=True)

    st.sidebar.success("Interview prep created.")


st.sidebar.divider()

st.sidebar.divider()

if st.sidebar.button("Refresh Job Data"):
    with st.spinner("Refreshing jobs..."):
        subprocess.run(["python", "fetch_jobs.py"], check=True)
        subprocess.run(["python", "main.py"], check=True)

    st.cache_data.clear()
    st.success("Job data refreshed. Reload the dashboard.")


# ==============================
# MANUAL JOB INPUT
# ==============================

st.sidebar.header("Manual Job Input")

with st.sidebar.expander("Add LinkedIn / Indeed / Manual Job"):
    manual_title = st.text_input("Job Title")
    manual_company = st.text_input("Company")
    manual_location = st.text_input("Location")
    manual_link = st.text_input("Job Link")
    manual_description = st.text_area("Job Description", height=220)

    if st.button("Save Manual Job"):
        if manual_title and manual_company and manual_description:
            manual_job = create_manual_job(
                manual_title,
                manual_company,
                manual_location,
                manual_link,
                manual_description
            )

            save_manual_job(manual_job)

            st.success("Manual job saved. Refresh dashboard to view it.")
        else:
            st.error("Please enter at least title, company, and description.")


st.sidebar.divider()


# ==============================
# FILTERS
# ==============================

st.sidebar.header("Filters")

priority_filter = st.sidebar.multiselect(
    "Priority",
    options=df["Priority"].dropna().unique(),
    default=df["Priority"].dropna().unique()
)

source_filter = st.sidebar.multiselect(
    "Source",
    options=df["Source"].dropna().unique(),
    default=df["Source"].dropna().unique()
)

role_filter = st.sidebar.multiselect(
    "Primary Role",
    options=df["Primary Role"].dropna().unique(),
    default=df["Primary Role"].dropna().unique()
)

min_score = st.sidebar.slider(
    "Minimum Match Score",
    min_value=0,
    max_value=100,
    value=0
)

search = st.sidebar.text_input("Search")


filtered_df = df[
    (df["Priority"].isin(priority_filter)) &
    (df["Source"].isin(source_filter)) &
    (df["Primary Role"].isin(role_filter)) &
    (df["Match Score"] >= min_score)
]

if search:
    search_lower = search.lower()
    filtered_df = filtered_df[
        filtered_df.astype(str).apply(
            lambda row: row.str.lower().str.contains(search_lower).any(),
            axis=1
        )
    ]


# ==============================
# KPI CARDS
# ==============================

total_jobs = len(df)
filtered_jobs = len(filtered_df)
high_priority = len(df[df["Priority"] == "High Priority"])
medium_priority = len(df[df["Priority"] == "Medium Priority"])
avg_score = round(df["Match Score"].mean(), 2) if total_jobs else 0

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Jobs</div>
        <div class="metric-value">{total_jobs}</div>
        <div class="small-muted">All tracked roles</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Filtered Jobs</div>
        <div class="metric-value">{filtered_jobs}</div>
        <div class="small-muted">Current view</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">High Priority</div>
        <div class="metric-value">{high_priority}</div>
        <div class="small-muted">Strong matches</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Medium Priority</div>
        <div class="metric-value">{medium_priority}</div>
        <div class="small-muted">Worth reviewing</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Average Score</div>
        <div class="metric-value">{avg_score}</div>
        <div class="small-muted">Across all jobs</div>
    </div>
    """, unsafe_allow_html=True)


# ==============================
# ANALYTICS
# ==============================

import plotly.express as px

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("📊 Job Analytics")

chart_col1, chart_col2, chart_col3, chart_col4 = st.columns(4)

if not filtered_df.empty:

    with chart_col1:
        role_counts = filtered_df["Primary Role"].value_counts().reset_index()
        role_counts.columns = ["Role", "Count"]

        fig = px.bar(
            role_counts,
            x="Role",
            y="Count",
            title="Jobs by Primary Role",
            color="Count",
            color_continuous_scale="Blues",
            height=320
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            margin=dict(l=20, r=20, t=45, b=70),
            showlegend=False,
            font=dict(size=11)
        )

        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        priority_counts = filtered_df["Priority"].value_counts().reset_index()
        priority_counts.columns = ["Priority", "Count"]

        fig = px.pie(
            priority_counts,
            names="Priority",
            values="Count",
            title="Jobs by Priority",
            hole=0.55,
            color="Priority",
            color_discrete_map={
                "High Priority": "#22c55e",
                "Medium Priority": "#f59e0b",
                "Low Priority": "#ef4444"
            },
            height=320
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            margin=dict(l=20, r=20, t=45, b=20),
            font=dict(size=11)
        )

        st.plotly_chart(fig, use_container_width=True)

    with chart_col3:
        source_counts = filtered_df["Source"].value_counts().reset_index()
        source_counts.columns = ["Source", "Count"]

        fig = px.pie(
            source_counts,
            names="Source",
            values="Count",
            title="Jobs by Source",
            hole=0.55,
            color_discrete_sequence=["#3b82f6", "#8b5cf6", "#22c55e", "#f97316"],
            height=320
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            margin=dict(l=20, r=20, t=45, b=20),
            font=dict(size=11)
        )

        st.plotly_chart(fig, use_container_width=True)

    with chart_col4:
        avg_score_by_role = (
            filtered_df.groupby("Primary Role")["Match Score"]
            .mean()
            .sort_values(ascending=True)
            .reset_index()
        )

        fig = px.bar(
            avg_score_by_role,
            x="Match Score",
            y="Primary Role",
            orientation="h",
            title="Average Score by Role",
            color="Match Score",
            color_continuous_scale="Blues",
            height=320
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            margin=dict(l=20, r=20, t=45, b=30),
            showlegend=False,
            font=dict(size=11)
        )

        st.plotly_chart(fig, use_container_width=True)

else:
    st.write("No jobs match the current filters.")

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# TOP SKILLS + RECENT MATCHES
# ==============================

from collections import Counter

st.markdown('<div class="section-card">', unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1.6])

with left_col:
    st.subheader("Top Matching Skills")

    all_keywords = []

    if "Matched Tech Keywords" in filtered_df.columns:
        for keywords in filtered_df["Matched Tech Keywords"].dropna():
            for keyword in str(keywords).split(","):
                cleaned = keyword.strip()
                if cleaned:
                    all_keywords.append(cleaned)

    skill_counts = Counter(all_keywords).most_common(5)

    if skill_counts:
        skills_df = pd.DataFrame(skill_counts, columns=["Skill", "Count"])

        fig = px.bar(
            skills_df.sort_values("Count"),
            x="Count",
            y="Skill",
            orientation="h",
            color="Count",
            color_continuous_scale="Greens",
            height=320,
            title="Top 5 Skills Across Jobs"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            margin=dict(l=20, r=20, t=45, b=30),
            showlegend=False,
            font=dict(size=11)
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No matched skills available yet.")

with right_col:
    st.subheader("Recent Top Matches")

    recent_cols = [
        "Title",
        "Company",
        "Match Score",
        "Primary Role",
        "Priority",
        "Source"
    ]

    recent_df = (
        filtered_df
        .sort_values(by="Match Score", ascending=False)
        .head(5)[recent_cols]
    )

    st.dataframe(
        recent_df,
        use_container_width=True,
        hide_index=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# DOWNLOADS
# ==============================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("📄 Generated Materials")

download_col1, download_col2, download_col3 = st.columns(3)

with download_col1:
    if os.path.exists("pdf_resumes/tailored_resume.pdf"):
        with open("pdf_resumes/tailored_resume.pdf", "rb") as file:
            st.download_button(
                label="Download Resume PDF",
                data=file,
                file_name="tailored_resume.pdf",
                mime="application/pdf"
            )
    elif os.path.exists("tailored_resume.docx"):
        with open("tailored_resume.docx", "rb") as file:
            st.download_button(
                label="Download Resume DOCX",
                data=file,
                file_name="tailored_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    else:
        st.write("No resume generated yet.")

with download_col2:
    latest_cover_pdf = latest_file("pdf_cover_letters", ".pdf")

    if latest_cover_pdf:
        with open(latest_cover_pdf, "rb") as file:
            st.download_button(
                label="Download Cover Letter PDF",
                data=file,
                file_name=os.path.basename(latest_cover_pdf),
                mime="application/pdf"
            )
    else:
        st.write("No cover letter PDF generated yet.")

with download_col3:
    if os.path.exists("latest_interview_prep.txt"):
        with open("latest_interview_prep.txt", "r", encoding="utf-8") as file:
            interview_text = file.read()

        st.download_button(
            label="Download Interview Prep",
            data=interview_text,
            file_name="interview_prep.txt",
            mime="text/plain"
        )
    else:
        st.write("No interview prep generated yet.")

st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# TOP MATCHES
# ==============================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🔥 Top Matches")

top_jobs = filtered_df.sort_values(by="Match Score", ascending=False).head(5)

for _, job in top_jobs.iterrows():
    priority_class = priority_badge(job["Priority"])

    with st.expander(f"{job['Title']} — {job['Company']} | Score: {job['Match Score']}"):
        st.markdown(
            f"""
            <span class="job-pill">{job.get('Primary Role', '')}</span>
            <span class="job-pill {priority_class}">{job.get('Priority', '')}</span>
            <span class="job-pill">{job.get('Source', '')}</span>
            """,
            unsafe_allow_html=True
        )

        st.write(f"**Location:** {job.get('Location', '')}")
        st.write(f"**Matched Role Groups:** {job.get('Matched Role Groups', '')}")
        st.write(f"**Matched Tech Keywords:** {job.get('Matched Tech Keywords', '')}")
        st.write(f"**Matched Titles:** {job.get('Matched Titles', '')}")

        st.write("**Why this score?**")
        for reason in explain_score(job):
            st.write(f"- {reason}")

        st.write(f"[Apply Here]({job['Link']})")

        current_status, current_notes = get_status_for_job(job)

        new_status = st.selectbox(
            "Application Status",
            STATUSES,
            index=STATUSES.index(current_status),
            key=f"status_{job['Title']}_{job['Company']}_{job['Link']}"
        )

        new_notes = st.text_area(
            "Notes",
            current_notes,
            key=f"notes_{job['Title']}_{job['Company']}_{job['Link']}"
        )

        if st.button(
            "Save Application Status",
            key=f"save_{job['Title']}_{job['Company']}_{job['Link']}"
        ):
            save_application(job, new_status, new_notes)
            st.success("Application status saved.")

st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# JOB TABLE
# ==============================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("📋 All Job Matches")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# COVER LETTER PREVIEW
# ==============================

if os.path.exists("latest_cover_letter.txt"):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("✉️ Latest Cover Letter Preview")

    with open("latest_cover_letter.txt", "r", encoding="utf-8") as file:
        cover_letter_text = file.read()

    st.text_area(
        "Cover Letter",
        cover_letter_text,
        height=300
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# INTERVIEW PREP PREVIEW
# ==============================

if os.path.exists("latest_interview_prep.txt"):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🎤 Latest Interview Prep Preview")

    with open("latest_interview_prep.txt", "r", encoding="utf-8") as file:
        interview_prep_text = file.read()

    st.text_area(
        "Interview Prep",
        interview_prep_text,
        height=400
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# MANUAL JOB MANAGEMENT
# ==============================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("📝 Manual Jobs")

manual_jobs_df = load_manual_jobs()

if manual_jobs_df.empty:
    st.write("No manual jobs saved.")
else:
    for _, manual_job in manual_jobs_df.iterrows():
        with st.expander(f"{manual_job['Title']} — {manual_job['Company']}"):
            st.write(f"**Score:** {manual_job['Match Score']}")
            st.write(f"**Primary Role:** {manual_job['Primary Role']}")
            st.write(f"**Source:** {manual_job['Source']}")
            st.write(f"[Open Job Link]({manual_job['Link']})")

            if st.button(
                "Delete Manual Job",
                key=f"delete_{manual_job['Title']}_{manual_job['Company']}_{manual_job['Link']}"
            ):
                deleted = delete_manual_job(
                    manual_job["Title"],
                    manual_job["Company"],
                    manual_job["Link"]
                )

                if deleted:
                    st.success("Manual job deleted. Refresh the page.")
                else:
                    st.error("Could not delete manual job.")

st.markdown('</div>', unsafe_allow_html=True)


# ==============================
# APPLICATION TRACKER
# ==============================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("✅ Application Tracker")

applications_df = load_applications()

if applications_df.empty:
    st.write("No applications tracked yet.")
else:
    st.dataframe(
        applications_df,
        use_container_width=True,
        hide_index=True
    )

st.markdown('</div>', unsafe_allow_html=True)