import json

import streamlit as st
from openai import OpenAI

from pages.resume_analysis import (
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_BASE_URL,
    get_resume_text,
    get_candidate_profile,
)


# ============================================================
# AI JOB-DESCRIPTION MATCHING
# ============================================================

def match_resume_to_job(resume_text, job_description, profile):
    """Compare the stored resume against a supplied job description."""

    if not GROQ_API_KEY:
        return None, (
            "AI matching is unavailable because GROQ_API_KEY "
            "is not configured in your .env file."
        )

    profile_text = f"""
Candidate name: {profile.get('name') or 'Not provided'}
Education: {profile.get('education') or 'Not provided'}
Target role: {profile.get('target_role') or 'Not provided'}
Experience level: {profile.get('experience') or 'Not provided'}
Technical skills: {profile.get('skills') or 'Not provided'}
Career goal: {profile.get('career_goal') or 'Not provided'}
"""

    prompt = f"""
You are Mirai AI, a professional ATS and career-matching assistant.

Compare the candidate's resume against the job description below.

CANDIDATE PROFILE:
{profile_text}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

IMPORTANT RULES:
1. Only use information actually present in the resume and job description.
2. Never invent skills, experience, projects, certifications, or achievements.
3. Distinguish clearly between skills the candidate has and skills the job requires.
4. Calculate an overall match score from 0 to 100.
5. Identify matched skills, missing skills, matching keywords, and relevant experience.
6. Give practical next steps for improving the candidate's fit.
7. Do not penalize the candidate for information that the job description does not require.
8. Return ONLY valid JSON. No markdown and no extra text.
9. All scores must be between 0 and 100.

Return exactly this structure:

{{
    "match_score": 0,
    "match_level": "Excellent / Strong / Moderate / Low",
    "summary": "Short explanation of the overall match.",
    "category_scores": {{
        "skills_match": 0,
        "experience_match": 0,
        "education_match": 0,
        "keyword_match": 0,
        "role_alignment": 0
    }},
    "matched_skills": [
        "Skill 1",
        "Skill 2",
        "Skill 3"
    ],
    "missing_skills": [
        "Skill 1",
        "Skill 2",
        "Skill 3"
    ],
    "matched_keywords": [
        "Keyword 1",
        "Keyword 2",
        "Keyword 3"
    ],
    "relevant_experience": [
        "Relevant resume evidence 1",
        "Relevant resume evidence 2"
    ],
    "improvements": [
        "Practical improvement 1",
        "Practical improvement 2",
        "Practical improvement 3",
        "Practical improvement 4"
    ],
    "interview_focus": [
        "Area to prepare for interview 1",
        "Area to prepare for interview 2",
        "Area to prepare for interview 3"
    ],
    "final_recommendation": "Concise recommendation for the candidate."
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
                        "You are Mirai AI's job-description matching engine. "
                        "Be accurate, evidence-based, and never invent candidate data. "
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
            return None, "The AI returned an invalid matching result."

        return data, None

    except json.JSONDecodeError:
        return None, "The AI returned an invalid JSON response."
    except Exception as error:
        return None, f"Job-description matching failed: {error}"


def clamp_score(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = 0
    return max(0, min(100, value))


def job_matching_page():
    user = st.session_state.get("user")

    if not user:
        st.title("🎯 Job-Description Matching")
        st.info("Please sign in to use job-description matching.")
        return

    st.title("🎯 Job-Description Matching")
    st.caption(
        "Compare your connected resume with a real job description "
        "and see how closely your profile matches the role."
    )

    # --------------------------------------------------------
    # LOAD STORED RESUME
    # --------------------------------------------------------
    resume, resume_error = get_resume_text(user["id"])

    if resume_error:
        with st.container(border=True):
            st.subheader("📄 Resume Required")
            st.write(resume_error)
            st.info("Upload a PDF resume from **My Profile → Edit Profile**.")

        return

    with st.container(border=True):
        col1, col2 = st.columns([3, 1])

        with col1:
            st.caption("CONNECTED RESUME")
            st.markdown(f"### 📄 {resume['filename']}")

        with col2:
            st.success("✓ Connected")

    st.write("")

    # --------------------------------------------------------
    # JOB DESCRIPTION
    # --------------------------------------------------------
    st.subheader("📋 Job Description")

    job_description = st.text_area(
        "Paste the complete job description below",
        placeholder=(
            "Example:\n\n"
            "We are looking for an AI/ML Engineer...\n"
            "Requirements:\n"
            "• Python\n"
            "• Machine Learning\n"
            "• SQL\n"
            "• TensorFlow / PyTorch\n"
            "..."
        ),
        height=300,
        key="job_description_input",
        label_visibility="collapsed",
    )

    st.caption(
        "For the most accurate result, paste the full job description, "
        "including responsibilities and requirements."
    )

    st.write("")

    # --------------------------------------------------------
    # ANALYZE
    # --------------------------------------------------------
    if st.button(
        "🎯 Analyze Job Match",
        type="primary",
        use_container_width=True,
    ):
        cleaned_job_description = job_description.strip()

        if not cleaned_job_description:
            st.error("Please paste a job description first.")
            return

        if len(cleaned_job_description) < 80:
            st.error(
                "The job description is too short. Please paste more of the "
                "job posting so Mirai can give you a meaningful match score."
            )
            return

        # Prevent unnecessarily large prompts while keeping the useful JD.
        cleaned_job_description = cleaned_job_description[:18000]

        with st.spinner("Mirai AI is comparing your resume with the job..."):
            profile = get_candidate_profile()

            result, error = match_resume_to_job(
                resume_text=resume["text"],
                job_description=cleaned_job_description,
                profile=profile,
            )

        if error:
            st.error(error)
            return

        st.session_state.job_match_result = result
        st.session_state.job_match_filename = resume["filename"]

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------
    result = st.session_state.get("job_match_result")

    if not result:
        with st.container(border=True):
            st.subheader("Ready when you are.")
            st.write(
                "Paste a job description above and click **Analyze Job Match** "
                "to get your personalized compatibility report."
            )
        return

    st.write("")

    match_score = clamp_score(result.get("match_score", 0))
    match_level = result.get("match_level", "Needs Review")

    # --------------------------------------------------------
    # OVERALL MATCH
    # --------------------------------------------------------
    with st.container(border=True):
        st.caption("OVERALL JOB MATCH")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric("Match Score", f"{match_score:.0f}/100")

        with col2:
            st.progress(match_score / 100)
            st.write(f"**{match_level} Match**")

    st.write("")

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------
    summary = result.get("summary", "")

    if summary:
        st.subheader("🧠 Match Summary")
        with st.container(border=True):
            st.write(summary)

    st.write("")

    # --------------------------------------------------------
    # CATEGORY SCORES
    # --------------------------------------------------------
    st.subheader("📊 Match Breakdown")

    category_scores = result.get("category_scores", {})
    categories = [
        ("Skills Match", "skills_match"),
        ("Experience Match", "experience_match"),
        ("Education Match", "education_match"),
        ("Keyword Match", "keyword_match"),
        ("Role Alignment", "role_alignment"),
    ]

    score_cols = st.columns(3)

    for index, (label, key) in enumerate(categories):
        with score_cols[index % 3]:
            value = clamp_score(category_scores.get(key, 0))

            with st.container(border=True):
                st.caption(label.upper())
                st.markdown(f"### {value:.0f}/100")
                st.progress(value / 100)

    st.write("")

    # --------------------------------------------------------
    # MATCHED / MISSING SKILLS
    # --------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matching Skills")
        matched_skills = result.get("matched_skills", [])

        with st.container(border=True):
            if matched_skills:
                for item in matched_skills:
                    st.write(f"• {item}")
            else:
                st.write("No clear matching skills were identified.")

    with col2:
        st.subheader("⚠️ Missing Skills")
        missing_skills = result.get("missing_skills", [])

        with st.container(border=True):
            if missing_skills:
                for item in missing_skills:
                    st.write(f"• {item}")
            else:
                st.success("No major missing skills identified.")

    st.write("")

    # --------------------------------------------------------
    # KEYWORDS
    # --------------------------------------------------------
    keywords = result.get("matched_keywords", [])

    if keywords:
        st.subheader("🔎 Matching Job Keywords")
        with st.container(border=True):
            st.write(" • ".join(str(item) for item in keywords))

        st.write("")

    # --------------------------------------------------------
    # RELEVANT EXPERIENCE
    # --------------------------------------------------------
    relevant_experience = result.get("relevant_experience", [])

    if relevant_experience:
        st.subheader("💼 Relevant Resume Evidence")
        with st.container(border=True):
            for item in relevant_experience:
                st.write(f"• {item}")

        st.write("")

    # --------------------------------------------------------
    # IMPROVEMENTS
    # --------------------------------------------------------
    improvements = result.get("improvements", [])

    st.subheader("🚀 How to Improve Your Match")

    with st.container(border=True):
        if improvements:
            for index, item in enumerate(improvements, start=1):
                st.write(f"**{index}.** {item}")
        else:
            st.write("No additional improvements were identified.")

    st.write("")

    # --------------------------------------------------------
    # INTERVIEW PREPARATION
    # --------------------------------------------------------
    interview_focus = result.get("interview_focus", [])

    if interview_focus:
        st.subheader("🎤 Interview Preparation Focus")
        with st.container(border=True):
            for item in interview_focus:
                st.write(f"• {item}")

        st.write("")

    # --------------------------------------------------------
    # FINAL RECOMMENDATION
    # --------------------------------------------------------
    recommendation = result.get("final_recommendation", "")

    if recommendation:
        st.subheader("💡 Mirai's Recommendation")
        with st.container(border=True):
            st.write(recommendation)

    st.write("")

    if st.button("🔄 Analyze Another Job", use_container_width=True):
        st.session_state.pop("job_match_result", None)
        st.session_state.pop("job_match_filename", None)
        st.rerun()


# ============================================================
# DIRECT STREAMLIT PAGE ENTRY
# ============================================================

if __name__ == "__main__":
    job_matching_page()