import streamlit as st
from datetime import datetime

from database.database import (
    get_interview_history,
    get_interview_answers,
)


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
# HELPERS
# ============================================================

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


def format_score(value):
    if value is None:
        return "—"

    try:
        return f"{float(value):.1f}%"
    except (TypeError, ValueError):
        return "—"


def _safe_text(value, fallback="Not available"):
    if value is None:
        return fallback

    value = str(value).strip()
    return value if value else fallback


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

        if st.button(
            "← Go to Mirai AI",
            type="primary",
            use_container_width=True
        ):
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

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------
    st.title("📜 Interview History")
    st.write("Review your previous interview sessions and detailed feedback.")
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
    # HISTORY SUMMARY
    # --------------------------------------------------------
    total_interviews = len(completed_interviews)

    valid_scores = [
        float(item["overall_score"])
        for item in completed_interviews
        if item.get("overall_score") is not None
    ]

    average_score = (
        sum(valid_scores) / len(valid_scores)
        if valid_scores else 0
    )

    best_score = max(valid_scores) if valid_scores else 0

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:
        st.metric("Completed Interviews", total_interviews)

    with summary_col2:
        st.metric("Average Score", f"{average_score:.1f}%")

    with summary_col3:
        st.metric("Best Score", f"{best_score:.1f}%")

    st.write("")
    st.subheader("Previous Interviews")

    # --------------------------------------------------------
    # DISPLAY COMPLETED INTERVIEWS
    # --------------------------------------------------------
    for index, interview in enumerate(completed_interviews, start=1):

        interview_id = interview.get("id")

        role = interview.get("target_job_role", "Unknown Role")
        interview_type = interview.get("interview_type", "Unknown Type")
        difficulty = interview.get("difficulty", "Unknown")
        focus_area = interview.get("focus_area", "General")

        overall_score = interview.get("overall_score")
        readiness_score = interview.get("readiness_score")

        completed_questions = interview.get("completed_questions", 0)
        total_questions = interview.get("total_questions", 0)

        completed_at = (
            interview.get("completed_at")
            or interview.get("created_at")
        )

        # ----------------------------------------------------
        # INTERVIEW SUMMARY CARD
        # ----------------------------------------------------
        with st.container(border=True):

            st.subheader(f"🎯 Interview #{total_interviews - index + 1} · {role}")
            st.caption(format_date(completed_at))

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Overall Score",
                    format_score(overall_score)
                )

            with col2:
                st.metric(
                    "Readiness",
                    format_score(readiness_score)
                )

            with col3:
                st.metric(
                    "Questions",
                    f"{completed_questions}/{total_questions}"
                    if total_questions
                    else str(completed_questions)
                )

            st.write("")
            st.write(f"**Interview Type:** {interview_type}")
            st.write(f"**Difficulty:** {difficulty}")
            st.write(f"**Focus Area:** {focus_area}")

            st.write("")

            score_col1, score_col2, score_col3, score_col4 = st.columns(4)

            score_items = [
                ("Technical", "technical_score"),
                ("Communication", "communication_score"),
                ("Problem Solving", "problem_solving_score"),
                ("Structure", "answer_structure_score"),
            ]

            for column, (label, field) in zip(
                [score_col1, score_col2, score_col3, score_col4],
                score_items
            ):
                with column:
                    st.caption(label)
                    st.write(format_score(interview.get(field)))

            st.write("")

            # ------------------------------------------------
            # LOAD DETAILED ANSWERS ONLY WHEN REQUESTED
            # ------------------------------------------------
            # Keep the widget key separate from the session-state key.
            # Streamlit does not allow a widget's own session-state key
            # to be modified after that widget has been instantiated.
            details_widget_key = f"history_details_btn_{interview_id}"
            details_state_key = f"history_details_open_{interview_id}"

            if details_state_key not in st.session_state:
                st.session_state[details_state_key] = False

            if st.button(
                "📖 View Interview Details",
                key=details_widget_key,
                use_container_width=True
            ):
                st.session_state[details_state_key] = not st.session_state[
                    details_state_key
                ]

            if st.session_state.get(details_state_key, False):

                st.divider()
                st.subheader("📝 Questions, Answers & Feedback")

                try:
                    answer_rows = get_interview_answers(user["id"], interview_id)
                except Exception as error:
                    st.error(
                        f"Could not load interview details: {error}"
                    )
                    answer_rows = []

                if not answer_rows:
                    st.info(
                        "No question-level answer records were found "
                        "for this interview."
                    )
                else:

                    for question_index, answer in enumerate(
                        answer_rows,
                        start=1
                    ):

                        question_text = _safe_text(
                            answer.get("question_text"),
                            "Question unavailable"
                        )

                        topic = _safe_text(
                            answer.get("topic"),
                            "General"
                        )

                        # The current database query may not expose topic
                        # directly through get_interview_answers, so keep
                        # the UI safe when it is unavailable.
                        if topic == "General" and answer.get("question_topic"):
                            topic = _safe_text(
                                answer.get("question_topic"),
                                "General"
                            )

                        with st.container(border=True):

                            st.markdown(
                                f"### Question {question_index}"
                            )

                            st.caption(f"🎯 Topic: {topic}")

                            st.markdown(
                                f"**Question**\n\n{question_text}"
                            )

                            st.markdown("**Your Answer**")
                            st.write(
                                _safe_text(
                                    answer.get("user_answer"),
                                    "No answer recorded."
                                )
                            )

                            eval_col1, eval_col2, eval_col3 = st.columns(3)

                            with eval_col1:
                                st.metric(
                                    "Answer Score",
                                    format_score(
                                        answer.get("overall_score")
                                    )
                                )

                            with eval_col2:
                                st.metric(
                                    "Technical",
                                    format_score(
                                        answer.get("technical_score")
                                    )
                                )

                            with eval_col3:
                                st.metric(
                                    "Communication",
                                    format_score(
                                        answer.get("communication_score")
                                    )
                                )

                            st.write("")

                            feedback_col1, feedback_col2 = st.columns(2)

                            with feedback_col1:
                                st.markdown("**💪 Strengths**")
                                st.write(
                                    _safe_text(
                                        answer.get("strengths"),
                                        "No strengths recorded."
                                    )
                                )

                                st.markdown("**⚠️ Areas to Improve**")
                                st.write(
                                    _safe_text(
                                        answer.get("weaknesses"),
                                        "No weaknesses recorded."
                                    )
                                )

                            with feedback_col2:
                                st.markdown("**🤖 Mirai Feedback**")
                                st.write(
                                    _safe_text(
                                        answer.get("feedback"),
                                        "No feedback recorded."
                                    )
                                )

                                st.markdown("**🎯 Recommended Action**")
                                st.write(
                                    _safe_text(
                                        answer.get("recommended_action"),
                                        "No recommended action recorded."
                                    )
                                )

                            st.write("")

                # --------------------------------------------
                # FINAL INTERVIEW SUMMARY
                # --------------------------------------------
                st.divider()
                st.subheader("📊 Final Interview Summary")

                final_col1, final_col2, final_col3 = st.columns(3)

                with final_col1:
                    st.metric(
                        "Overall",
                        format_score(interview.get("overall_score"))
                    )
                    st.metric(
                        "Technical",
                        format_score(interview.get("technical_score"))
                    )

                with final_col2:
                    st.metric(
                        "Communication",
                        format_score(
                            interview.get("communication_score")
                        )
                    )
                    st.metric(
                        "Problem Solving",
                        format_score(
                            interview.get("problem_solving_score")
                        )
                    )

                with final_col3:
                    st.metric(
                        "Answer Structure",
                        format_score(
                            interview.get("answer_structure_score")
                        )
                    )
                    st.metric(
                        "Readiness",
                        format_score(
                            interview.get("readiness_score")
                        )
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