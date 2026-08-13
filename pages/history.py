import streamlit as st
from datetime import datetime

from database.database import get_interview_history


# ============================================================
# INTERVIEW HISTORY PAGE
# ============================================================

def history_page():

    # The page shares the same Streamlit session as app.py.
    user = st.session_state.get("user")

    if not user:
        st.title("📜 Interview History")
        st.info(
            "Please sign in to your Mirai AI account to view your interview history."
        )

        if st.button("← Go to Mirai AI", type="primary", use_container_width=True):
            st.session_state.page = "welcome"
            st.switch_page("app.py")
        return

    # --------------------------------------------------------
    # LOAD USER'S INTERVIEW HISTORY
    # --------------------------------------------------------
    try:
        interviews = get_interview_history(user["id"])
    except Exception as error:
        st.error(f"Could not load interview history: {error}")
        return

    completed_interviews = [
        interview
        for interview in interviews
        if interview.get("status") == "completed"
    ]

    st.title("📜 Interview History")
    st.write("Review your previous interview sessions.")
    st.write("")

    # --------------------------------------------------------
    # NO HISTORY YET
    # --------------------------------------------------------
    if not completed_interviews:
        with st.container(border=True):
            st.subheader("No interviews completed yet.")
            st.write(
                "Once you complete an interview, your results "
                "and feedback will appear here."
            )

        st.write("")

        if st.button(
            "🚀 Start Your First Interview",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page = "interview_setup"
            st.switch_page("app.py")

        return

    # --------------------------------------------------------
    # DATE FORMATTER
    # --------------------------------------------------------
    def format_date(value):
        if not value:
            return "Date unavailable"

        try:
            parsed = datetime.fromisoformat(
                str(value).replace("Z", "+00:00")
            )
            return parsed.strftime("%d %b %Y, %I:%M %p")
        except (TypeError, ValueError):
            return str(value)

    # --------------------------------------------------------
    # DISPLAY COMPLETED INTERVIEWS
    # --------------------------------------------------------
    for interview in completed_interviews:

        role = interview.get("target_job_role", "Unknown Role")
        interview_type = interview.get("interview_type", "Unknown Type")
        difficulty = interview.get("difficulty", "Unknown")

        overall_score = interview.get("overall_score")
        readiness_score = interview.get("readiness_score")

        completed_questions = interview.get("completed_questions", 0)
        total_questions = interview.get("total_questions", 0)

        completed_at = (
            interview.get("completed_at")
            or interview.get("created_at")
        )

        with st.container(border=True):

            st.subheader(f"🎯 {role}")
            st.caption(format_date(completed_at))

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Overall Score",
                    f"{float(overall_score):.1f}%"
                    if overall_score is not None else "—"
                )

            with col2:
                st.metric(
                    "Readiness",
                    f"{float(readiness_score):.1f}%"
                    if readiness_score is not None else "—"
                )

            with col3:
                st.metric(
                    "Questions",
                    f"{completed_questions}/{total_questions}"
                    if total_questions else str(completed_questions)
                )

            st.write("")
            st.write(f"**Interview Type:** {interview_type}")
            st.write(f"**Difficulty:** {difficulty}")
            st.write("")

            score_col1, score_col2, score_col3, score_col4 = st.columns(4)

            with score_col1:
                value = interview.get("technical_score")
                st.caption("Technical")
                st.write(
                    f"{float(value):.1f}%"
                    if value is not None else "—"
                )

            with score_col2:
                value = interview.get("communication_score")
                st.caption("Communication")
                st.write(
                    f"{float(value):.1f}%"
                    if value is not None else "—"
                )

            with score_col3:
                value = interview.get("problem_solving_score")
                st.caption("Problem Solving")
                st.write(
                    f"{float(value):.1f}%"
                    if value is not None else "—"
                )

            with score_col4:
                value = interview.get("answer_structure_score")
                st.caption("Structure")
                st.write(
                    f"{float(value):.1f}%"
                    if value is not None else "—"
                )

        st.write("")

    # --------------------------------------------------------
    # START ANOTHER INTERVIEW
    # --------------------------------------------------------
    if st.button(
        "🚀 Start New Interview",
        type="primary",
        use_container_width=True
    ):
        st.session_state.page = "interview_setup"
        st.switch_page("app.py")


# ============================================================
# DIRECT STREAMLIT PAGE ENTRY
# ============================================================

if __name__ == "__main__":
    history_page()