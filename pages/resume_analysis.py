import json
import os
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from database.database import get_user_resume



# ============================================================
# MOBILE RESPONSIVE UI
# ============================================================

st.markdown(
    '''

<style>
@media (max-width: 640px) {
    .block-container {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-top: 1.25rem !important;
        padding-bottom: 2.5rem !important;
    }

    h1 {
        font-size: 1.8rem !important;
        line-height: 1.2 !important;
    }

    h2 {
        font-size: 1.4rem !important;
        line-height: 1.25 !important;
    }

    h3 {
        font-size: 1.15rem !important;
        line-height: 1.3 !important;
    }

    div[data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 0.75rem !important;
    }

    div[data-testid="stHorizontalBlock"] > div {
        flex: 1 1 100% !important;
        min-width: 100% !important;
        width: 100% !important;
    }

    .stButton > button,
    [data-testid="stFormSubmitButton"] button {
        min-height: 48px !important;
    }

    .stTextInput input,
    .stTextArea textarea {
        font-size: 16px !important;
    }

    .stTextArea textarea {
        min-height: 180px;
    }

    pre,
    code,
    [data-testid="stMarkdownContainer"] {
        overflow-wrap: anywhere;
        word-break: break-word;
    }

    [data-testid="stMetric"] {
        width: 100% !important;
        box-sizing: border-box !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
    }
}
</style>
    ''',
    unsafe_allow_html=True,
)

# ============================================================
# CONFIGURATION
# ============================================================

# Use the same .env configuration as the existing interview engine.
# Do NOT use st.secrets here because the project does not require
# a Streamlit secrets.toml file.
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


# ============================================================
# RESUME HELPERS
# ============================================================

def get_resume_text(user_id):
    """
    Load the user's stored PDF and temporarily extract its text.
    The original PDF remains stored in the database.
    """

    try:
        resume = get_user_resume(user_id)

        if not resume:
            return None, "No resume is connected to your profile."

        pdf_data = resume.get("pdf_data")

        if not isinstance(pdf_data, (bytes, bytearray)):
            return None, "The stored resume could not be read."

        if not pdf_data:
            return None, "The stored resume is empty."

        reader = PdfReader(BytesIO(bytes(pdf_data)))

        pages = []

        for page in reader.pages:
            try:
                page_text = page.extract_text() or ""
            except Exception:
                page_text = ""

            if page_text.strip():
                pages.append(page_text.strip())

        resume_text = "\n\n".join(pages).strip()

        if not resume_text:
            return (
                None,
                "I could not extract readable text from this PDF. "
                "Please make sure your resume contains selectable text.",
            )

        # Keep the AI prompt at a reasonable size.
        resume_text = resume_text[:18000]

        return {
            "filename": resume.get("filename", "Resume.pdf"),
            "text": resume_text,
        }, None

    except Exception as error:
        return None, f"Could not read your resume: {error}"


def get_candidate_profile():
    """
    Read candidate information already available in the active
    Streamlit session.
    """

    user = st.session_state.get("user", {})

    if not isinstance(user, dict):
        return {}

    return {
        "name": user.get("full_name", ""),
        "education": user.get("education", ""),
        "target_role": user.get("target_job_role", ""),
        "experience": user.get("experience_level", ""),
        "skills": user.get("technical_skills", ""),
        "career_goal": user.get("career_goal", ""),
    }


# ============================================================
# AI ANALYSIS
# ============================================================

def analyze_resume_with_ai(resume_text, filename, profile):
    """
    Analyze the resume using the existing Groq/OpenAI-compatible
    configuration used by Mirai AI.
    """

    if not GROQ_API_KEY:
        return None, (
            "AI analysis is currently unavailable because "
            "GROQ_API_KEY is not configured in your .env file."
        )

    try:
        from openai import OpenAI
    except ImportError:
        return None, "The OpenAI package is not installed."

    profile_text = f"""
Candidate name: {profile.get("name") or "Not provided"}
Education: {profile.get("education") or "Not provided"}
Target role: {profile.get("target_role") or "Not provided"}
Experience level: {profile.get("experience") or "Not provided"}
Technical skills: {profile.get("skills") or "Not provided"}
Career goal: {profile.get("career_goal") or "Not provided"}
"""

    prompt = f"""
You are Mirai AI, a professional resume reviewer and career coach.

Analyze the candidate's resume carefully.

RESUME FILE:
{filename}

CANDIDATE PROFILE:
{profile_text}

RESUME CONTENT:
{resume_text}

Evaluate the resume for professional quality, clarity, relevance,
skills, projects, experience, education, achievements, and
ATS/readability.

IMPORTANT RULES:

1. Only use information actually present in the resume.
2. Do not invent experience, projects, skills, achievements,
   certifications, companies, or education.
3. If something is missing, clearly say it is missing.
4. Consider the candidate's target role when evaluating relevance.
5. Give practical suggestions that the candidate can actually apply.
6. Scores must be between 0 and 100.
7. Return ONLY valid JSON.
8. Do not use markdown.
9. Do not include additional fields.

Return exactly:

{{
    "overall_score": 0,

    "category_scores": {{
        "ats_readability": 0,
        "skills": 0,
        "projects": 0,
        "experience": 0,
        "education": 0,
        "impact": 0
    }},

    "summary": "Short professional summary of the resume.",

    "strengths": [
        "Strength 1",
        "Strength 2",
        "Strength 3"
    ],

    "weaknesses": [
        "Weakness 1",
        "Weakness 2",
        "Weakness 3"
    ],

    "missing_sections": [
        "Missing section 1",
        "Missing section 2"
    ],

    "improvements": [
        "Specific improvement 1",
        "Specific improvement 2",
        "Specific improvement 3",
        "Specific improvement 4",
        "Specific improvement 5"
    ],

    "role_relevance": "Explain how well the resume matches the target role.",

    "ats_keywords": [
        "keyword 1",
        "keyword 2",
        "keyword 3"
    ],

    "final_recommendation": "One concise recommendation for the candidate."
}}
"""

    try:
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url=GROQ_BASE_URL,
            max_retries=0,
            timeout=45.0,
        )

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            temperature=0.2,
            max_tokens=1800,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Mirai AI's professional resume "
                        "analysis engine. Be accurate, practical, "
                        "and never invent candidate information. "
                        "Return only valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content

        if not content:
            return None, "The AI returned an empty response."

        content = content.strip()

        # Remove accidental markdown code fences.
        if content.startswith("```"):
            if content.startswith("```json"):
                content = content[7:]
            else:
                content = content[3:]

            if content.endswith("```"):
                content = content[:-3]

            content = content.strip()

        data = json.loads(content)

        if not isinstance(data, dict):
            return None, "The AI returned an invalid analysis."

        return data, None

    except json.JSONDecodeError:
        return None, "The AI returned an invalid analysis format."

    except Exception as error:
        return None, f"Resume analysis failed: {error}"


# ============================================================
# UI HELPERS
# ============================================================

def score_label(score):
    if score >= 85:
        return "Excellent"
    if score >= 70:
        return "Good"
    if score >= 55:
        return "Needs Improvement"
    return "Needs Attention"


# ============================================================
# RESUME ANALYSIS PAGE
# ============================================================

def resume_analysis_page():

    user = st.session_state.get("user")

    # --------------------------------------------------------
    # AUTHENTICATION
    # --------------------------------------------------------

    if not user:
        st.title("📄 Resume Analysis")

        st.info(
            "Please sign in to your Mirai AI account "
            "to analyze your resume."
        )

        if st.button(
            "← Go to Mirai AI",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.page = "welcome"
            st.switch_page("app.py")

        return

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.title("📄 Resume Analysis")

    st.caption(
        "Get an AI-powered review of your resume, "
        "including strengths, weaknesses, ATS readiness, "
        "and practical improvements."
    )

    st.write("")

    # --------------------------------------------------------
    # LOAD RESUME
    # --------------------------------------------------------

    resume, error = get_resume_text(user["id"])

    if error:
        with st.container(border=True):
            st.subheader("📄 No Resume Available")
            st.write(error)

            if st.button(
                "👤 Go to Profile",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.page = "profile"
                st.switch_page("app.py")

        return

    filename = resume["filename"]

    # --------------------------------------------------------
    # RESUME CONNECTED CARD
    # --------------------------------------------------------

    with st.container(border=True):

        col1, col2 = st.columns([3, 1])

        with col1:
            st.caption("CONNECTED RESUME")
            st.markdown(f"### 📄 {filename}")

        with col2:
            st.success("✓ Connected")

    st.write("")

    # --------------------------------------------------------
    # ANALYSIS BUTTON
    # --------------------------------------------------------

    if st.button(
        "🤖 Analyze My Resume",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner(
            "Mirai AI is analyzing your resume..."
        ):

            profile = get_candidate_profile()

            analysis, analysis_error = analyze_resume_with_ai(
                resume_text=resume["text"],
                filename=filename,
                profile=profile,
            )

        if analysis_error:
            st.error(analysis_error)
            return

        st.session_state.resume_analysis = analysis

    # --------------------------------------------------------
    # CURRENT ANALYSIS
    # --------------------------------------------------------

    analysis = st.session_state.get("resume_analysis")

    if not analysis:
        st.write("")

        with st.container(border=True):
            st.subheader("Ready when you are.")
            st.write(
                "Click **Analyze My Resume** to get your "
                "personalized resume review."
            )

        return

    st.write("")

    # --------------------------------------------------------
    # OVERALL SCORE
    # --------------------------------------------------------

    try:
        overall_score = float(
            analysis.get("overall_score", 0)
        )
    except (TypeError, ValueError):
        overall_score = 0

    overall_score = max(
        0,
        min(100, overall_score),
    )

    with st.container(border=True):

        st.caption("OVERALL RESUME SCORE")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric(
                "Resume Score",
                f"{overall_score:.0f}/100",
            )

        with col2:
            st.progress(
                overall_score / 100,
            )

            st.write(
                f"**{score_label(overall_score)}**"
            )

    st.write("")

    # --------------------------------------------------------
    # CATEGORY SCORES
    # --------------------------------------------------------

    st.subheader("📊 Resume Breakdown")

    category_scores = analysis.get(
        "category_scores",
        {},
    )

    categories = [
        ("ATS Readability", "ats_readability"),
        ("Skills", "skills"),
        ("Projects", "projects"),
        ("Experience", "experience"),
        ("Education", "education"),
        ("Impact", "impact"),
    ]

    for row_start in range(0, len(categories), 3):

        row_categories = categories[
            row_start:row_start + 3
        ]

        score_cols = st.columns(3)

        for column, (label, key) in zip(
            score_cols,
            row_categories,
        ):

            with column:

                try:
                    value = float(
                        category_scores.get(key, 0)
                    )
                except (TypeError, ValueError):
                    value = 0

                value = max(
                    0,
                    min(100, value),
                )

                with st.container(border=True):

                    st.caption(label.upper())

                    st.markdown(
                        f"### {value:.0f}/100"
                    )

                    st.progress(
                        value / 100,
                    )

    st.write("")

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    summary = analysis.get(
        "summary",
        "",
    )

    if summary:

        st.subheader("🧠 AI Summary")

        with st.container(border=True):
            st.write(summary)

    st.write("")

    # --------------------------------------------------------
    # STRENGTHS / WEAKNESSES
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Strengths")

        strengths = analysis.get(
            "strengths",
            [],
        )

        with st.container(border=True):

            if strengths:
                for item in strengths:
                    st.write(f"• {item}")
            else:
                st.write(
                    "No specific strengths identified."
                )

    with col2:

        st.subheader("⚠️ Areas to Improve")

        weaknesses = analysis.get(
            "weaknesses",
            [],
        )

        with st.container(border=True):

            if weaknesses:
                for item in weaknesses:
                    st.write(f"• {item}")
            else:
                st.write(
                    "No major weaknesses identified."
                )

    st.write("")

    # --------------------------------------------------------
    # MISSING SECTIONS
    # --------------------------------------------------------

    missing_sections = analysis.get(
        "missing_sections",
        [],
    )

    if missing_sections:

        st.subheader("📌 Missing or Weak Sections")

        with st.container(border=True):

            for item in missing_sections:
                st.write(f"• {item}")

    st.write("")

    # --------------------------------------------------------
    # ROLE RELEVANCE
    # --------------------------------------------------------

    role_relevance = analysis.get(
        "role_relevance",
        "",
    )

    if role_relevance:

        st.subheader("🎯 Target Role Relevance")

        with st.container(border=True):
            st.write(role_relevance)

    st.write("")

    # --------------------------------------------------------
    # ATS KEYWORDS
    # --------------------------------------------------------

    keywords = analysis.get(
        "ats_keywords",
        [],
    )

    if keywords:

        st.subheader("🔎 Recommended ATS Keywords")

        with st.container(border=True):

            st.write(
                "Consider naturally including relevant "
                "keywords that genuinely match your experience:"
            )

            st.write(
                " • ".join(
                    str(keyword)
                    for keyword in keywords
                )
            )

    st.write("")

    # --------------------------------------------------------
    # IMPROVEMENTS
    # --------------------------------------------------------

    improvements = analysis.get(
        "improvements",
        [],
    )

    st.subheader("🚀 Recommended Improvements")

    with st.container(border=True):

        if improvements:

            for index, item in enumerate(
                improvements,
                start=1,
            ):
                st.write(
                    f"**{index}.** {item}"
                )

        else:
            st.write(
                "No specific improvements were identified."
            )

    st.write("")

    # --------------------------------------------------------
    # FINAL RECOMMENDATION
    # --------------------------------------------------------

    recommendation = analysis.get(
        "final_recommendation",
        "",
    )

    if recommendation:

        st.subheader("💡 Mirai's Recommendation")

        with st.container(border=True):
            st.write(recommendation)

    st.write("")

    # --------------------------------------------------------
    # RE-ANALYZE
    # --------------------------------------------------------

    if st.button(
        "🔄 Analyze Again",
        use_container_width=True,
    ):

        st.session_state.pop(
            "resume_analysis",
            None,
        )

        st.rerun()


# ============================================================
# DIRECT STREAMLIT PAGE ENTRY
# ============================================================

if __name__ == "__main__":
    resume_analysis_page()