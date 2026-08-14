import streamlit as st
import pandas as pd

from database.database import (
    get_user_progress,
    get_interview_history,
    get_weak_topics,
)


# ============================================================
# HELPERS
# ============================================================

def _safe_float(value, default=0.0):
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _score_label(score):
    score = _safe_float(score)

    if score >= 85:
        return "Excellent"
    if score >= 70:
        return "Strong"
    if score >= 55:
        return "Developing"
    if score > 0:
        return "Needs Focus"
    return "Not evaluated"


def _score_class(score):
    score = _safe_float(score)

    if score >= 85:
        return "excellent"
    if score >= 70:
        return "strong"
    if score >= 55:
        return "developing"
    return "focus"


def _valid_score(value):
    try:
        return value is not None and float(value) >= 0
    except (TypeError, ValueError):
        return False


def _average_for(interviews, field):
    values = [
        float(item.get(field))
        for item in interviews
        if _valid_score(item.get(field))
    ]
    return sum(values) / len(values) if values else 0.0


def _change(current, previous):
    if previous is None:
        return 0.0
    return round(float(current) - float(previous), 1)


def _direction(change):
    if change > 2:
        return "Improving"
    if change < -2:
        return "Declining"
    return "Stable"


def _trend_class(change):
    if change > 2:
        return "trend-positive"
    if change < -2:
        return "trend-negative"
    return "trend-neutral"


def _trend_symbol(change):
    if change > 2:
        return "↑"
    if change < -2:
        return "↓"
    return "→"


def _skill_analytics(interviews):
    fields = [
        ("Technical Knowledge", "technical_score"),
        ("Communication", "communication_score"),
        ("Problem Solving", "problem_solving_score"),
        ("Answer Structure", "answer_structure_score"),
    ]

    recent = interviews[-3:]
    previous = interviews[-6:-3] if len(interviews) > 3 else []
    result = []

    for name, field in fields:
        recent_avg = _average_for(recent, field)
        previous_avg = (
            _average_for(previous, field) if previous else None
        )
        result.append({
            "name": name,
            "recent": recent_avg,
            "change": _change(recent_avg, previous_avg),
        })

    return result


def _render_trend_badge(change):
    st.markdown(
        f"""
        <div class="trend-badge {_trend_class(change)}">
            {_trend_symbol(change)} {abs(change):.1f} pts
            <span>{_direction(change)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_score_bar(label, score):
    score = max(0.0, min(100.0, _safe_float(score)))
    state = _score_class(score)

    st.markdown(
        f"""
        <div class="skill-row">
            <div class="skill-row-top">
                <span class="skill-name">{label}</span>
                <span class="skill-score {state}">{score:.1f}%</span>
            </div>
            <div class="skill-track">
                <div class="skill-fill {state}" style="width:{score:.1f}%"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_topic_card(topic):
    name = topic.get("topic") or "General"
    average = _safe_float(topic.get("average_score"))
    last = _safe_float(topic.get("last_score"))
    attempts = int(topic.get("attempts") or 0)
    improvement = _safe_float(topic.get("improvement_rate"))

    if improvement > 0:
        trend = f"↑ {improvement:.1f}%"
        trend_class = "positive"
    elif improvement < 0:
        trend = f"↓ {abs(improvement):.1f}%"
        trend_class = "negative"
    else:
        trend = "— 0.0%"
        trend_class = "neutral"

    st.markdown(
        f"""
        <div class="topic-card">
            <div class="topic-header">
                <div>
                    <div class="topic-name">{name}</div>
                    <div class="topic-attempts">
                        {attempts} attempt{"s" if attempts != 1 else ""}
                    </div>
                </div>
                <div class="topic-average">{average:.1f}%</div>
            </div>
            <div class="topic-meta">
                <span>Latest {last:.1f}%</span>
                <span class="topic-trend {trend_class}">{trend}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_insight(score, readiness, weakest_topics, interviews_completed):
    score = _safe_float(score)
    readiness = _safe_float(readiness)

    if interviews_completed == 0:
        title = "Your journey starts here"
        body = (
            "Complete your first mock interview and Mirai will begin "
            "building a performance profile from your actual results."
        )
    elif weakest_topics:
        weak = weakest_topics[0]
        topic_name = weak.get("topic") or "your weakest topic"
        weak_score = _safe_float(weak.get("average_score"))
        title = f"Focus next on {topic_name}"
        body = (
            f"Your current average in {topic_name} is {weak_score:.1f}%. "
            "Practice this area in your next interview and use the "
            "feedback after each attempt to track improvement."
        )
    elif readiness >= 85:
        title = "You're looking interview-ready"
        body = (
            "Your readiness is strong. Keep practicing under realistic "
            "conditions and focus on consistency rather than only chasing "
            "a higher score."
        )
    elif score >= 70:
        title = "You're building a strong foundation"
        body = (
            "Your overall performance is moving in the right direction. "
            "Keep alternating between full mock interviews and focused "
            "practice on weaker skills."
        )
    else:
        title = "Consistency is the next goal"
        body = (
            "Use your next interview to identify where marks are being "
            "lost. Small improvements across several attempts will raise "
            "your overall readiness."
        )

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-icon">🤖</div>
            <div>
                <div class="insight-title">{title}</div>
                <div class="insight-body">{body}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PERFORMANCE DASHBOARD
# ============================================================

def progress_page():
    user = st.session_state.get("user")

    if not user:
        st.warning("Please sign in to view your performance.")
        return

    user_id = user["id"]
    first_name = user.get("full_name", "there").split()[0]

    # --------------------------------------------------------
    # Load stored performance data.
    # --------------------------------------------------------
    try:
        progress = get_user_progress(user_id) or {}
    except Exception:
        progress = {}

    try:
        interviews = get_interview_history(user_id) or []
    except Exception:
        interviews = []

    completed = [
        item for item in interviews
        if item.get("status") == "completed"
    ]

    # History is returned newest-first. Reverse for a natural
    # left-to-right progress timeline.
    completed_for_chart = list(reversed(completed))

    try:
        weak_topics = get_weak_topics(user_id, limit=5) or []
    except Exception:
        weak_topics = []

    # --------------------------------------------------------
    # Calculate dashboard values.
    # Prefer the persisted progress record, with interview
    # history as a safe fallback.
    # --------------------------------------------------------
    average_score = _safe_float(progress.get("average_score"))

    if not average_score and completed:
        scores = [
            _safe_float(item.get("overall_score"))
            for item in completed
            if item.get("overall_score") is not None
        ]
        if scores:
            average_score = sum(scores) / len(scores)

    interviews_completed = int(
        progress.get("interviews_completed")
        or len(completed)
        or 0
    )

    questions_answered = int(
        progress.get("questions_answered")
        or sum(
            int(item.get("completed_questions") or 0)
            for item in completed
        )
        or 0
    )

    readiness = _safe_float(progress.get("readiness_score"))

    if not readiness and completed:
        readiness = _safe_float(
            completed[0].get("readiness_score")
        )

    technical = _safe_float(
        progress.get("technical_average")
    )
    communication = _safe_float(
        progress.get("communication_average")
    )
    problem_solving = _safe_float(
        progress.get("problem_solving_average")
    )
    answer_structure = _safe_float(
        progress.get("answer_structure_average")
    )

    # Fallback to interview history if the progress record has
    # not yet been populated.
    if completed:
        if not technical:
            technical = sum(
                _safe_float(i.get("technical_score"))
                for i in completed
            ) / len(completed)

        if not communication:
            communication = sum(
                _safe_float(i.get("communication_score"))
                for i in completed
            ) / len(completed)

        if not problem_solving:
            problem_solving = sum(
                _safe_float(i.get("problem_solving_score"))
                for i in completed
            ) / len(completed)

        if not answer_structure:
            answer_structure = sum(
                _safe_float(i.get("answer_structure_score"))
                for i in completed
            ) / len(completed)

    # --------------------------------------------------------
    # PAGE CSS
    # --------------------------------------------------------
    st.markdown(
        """
        <style>
        .progress-hero {
            background:
                linear-gradient(135deg, #FFFFFF 0%, #F7F5FF 100%);
            border: 1px solid #E4E2F2;
            border-radius: 24px;
            padding: 30px 34px;
            margin-bottom: 24px;
            box-shadow: 0 12px 35px rgba(60, 55, 120, 0.055);
        }

        .progress-eyebrow {
            color: #7567DE;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1.4px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .progress-title {
            color: #20243A;
            font-size: 34px;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 8px;
        }

        .progress-subtitle {
            color: #747A91;
            font-size: 15px;
            line-height: 1.6;
        }

        .metric-card {
            background: #FFFFFF;
            border: 1px solid #E4E5F0;
            border-radius: 18px;
            padding: 20px;
            min-height: 108px;
            box-shadow: 0 8px 26px rgba(50, 45, 100, 0.045);
        }

        .metric-label {
            color: #7A8096;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: .6px;
        }

        .metric-value {
            color: #292D47;
            font-size: 28px;
            font-weight: 800;
            margin-top: 8px;
        }

        .metric-note {
            color: #8C91A5;
            font-size: 12px;
            margin-top: 4px;
        }

        .section-card {
            background: #FFFFFF;
            border: 1px solid #E4E5F0;
            border-radius: 20px;
            padding: 22px;
            box-shadow: 0 8px 26px rgba(50, 45, 100, 0.045);
        }

        .skill-row {
            margin: 17px 0;
        }

        .skill-row-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }

        .skill-name {
            color: #454B66;
            font-size: 14px;
            font-weight: 650;
        }

        .skill-score {
            font-size: 13px;
            font-weight: 800;
        }

        .skill-score.excellent,
        .skill-score.strong {
            color: #6255C8;
        }

        .skill-score.developing {
            color: #8A72D6;
        }

        .skill-score.focus {
            color: #B06A7A;
        }

        .skill-track {
            width: 100%;
            height: 9px;
            background: #ECECF5;
            border-radius: 20px;
            overflow: hidden;
        }

        .skill-fill {
            height: 100%;
            border-radius: 20px;
            background: linear-gradient(90deg, #7567DE, #9A8EF2);
        }

        .skill-fill.focus {
            background: linear-gradient(90deg, #B58A96, #D1A7B1);
        }

        .topic-card {
            background: #FBFAFF;
            border: 1px solid #E8E6F4;
            border-radius: 15px;
            padding: 15px 16px;
            margin-bottom: 10px;
        }

        .topic-header,
        .topic-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .topic-name {
            color: #30354D;
            font-weight: 750;
            font-size: 14px;
        }

        .topic-attempts {
            color: #9095A8;
            font-size: 11px;
            margin-top: 3px;
        }

        .topic-average {
            color: #5F54C7;
            font-weight: 800;
            font-size: 18px;
        }

        .topic-meta {
            margin-top: 10px;
            color: #8A8FA2;
            font-size: 11px;
        }

        .topic-trend.positive {
            color: #4C8B73;
            font-weight: 700;
        }

        .topic-trend.negative {
            color: #B56D7B;
            font-weight: 700;
        }

        .topic-trend.neutral {
            color: #9095A8;
        }

        .insight-card {
            display: flex;
            gap: 16px;
            align-items: flex-start;
            background:
                linear-gradient(135deg, #F5F2FF 0%, #FFFFFF 100%);
            border: 1px solid #DDD8F4;
            border-radius: 20px;
            padding: 22px;
            margin-top: 6px;
        }

        .insight-icon {
            width: 44px;
            height: 44px;
            min-width: 44px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #E9E5FF;
            font-size: 21px;
        }

        .insight-title {
            color: #30354D;
            font-size: 16px;
            font-weight: 800;
            margin-bottom: 5px;
        }

        .insight-body {
            color: #747A91;
            font-size: 13px;
            line-height: 1.6;
        }

        .empty-state {
            text-align: center;
            padding: 32px 20px;
            color: #747A91;
        }

        .trend-badge {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            border-radius: 999px;
            padding: 7px 12px;
            font-size: 12px;
            font-weight: 800;
        }

        .trend-positive { color: #3F836A; }
        .trend-negative { color: #B05E73; }
        .trend-neutral { color: #7D8397; }

        .analytics-row {
            padding: 13px 0;
            border-bottom: 1px solid #EEEFF5;
        }

        .analytics-row:last-child {
            border-bottom: none;
        }

        .analytics-main,
        .analytics-sub {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .analytics-name {
            color: #454B66;
            font-size: 14px;
            font-weight: 700;
        }

        .analytics-score {
            color: #5F54C7;
            font-size: 15px;
            font-weight: 800;
        }

        .analytics-sub {
            margin-top: 5px;
            color: #9196A8;
            font-size: 11px;
        }

        .analytics-insight {
            background: linear-gradient(135deg, #F6F3FF, #FFFFFF);
            border: 1px solid #DDD8F4;
            border-radius: 18px;
            padding: 20px;
        }

        .analytics-insight-title {
            color: #30354D;
            font-size: 16px;
            font-weight: 800;
            margin-bottom: 7px;
        }

        .analytics-insight-body {
            color: #70768C;
            font-size: 13px;
            line-height: 1.65;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------
    st.markdown(
        f"""
        <div class="progress-hero">
            <div class="progress-eyebrow">
                MIRAI PERFORMANCE INTELLIGENCE
            </div>
            <div class="progress-title">
                Your progress, {first_name}.
            </div>
            <div class="progress-subtitle">
                See how your interview performance is evolving,
                where you're strongest, and what Mirai thinks you
                should focus on next.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # KPI ROW
    # --------------------------------------------------------
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Interviews</div>
                <div class="metric-value">{interviews_completed}</div>
                <div class="metric-note">Completed sessions</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Average Score</div>
                <div class="metric-value">{average_score:.1f}%</div>
                <div class="metric-note">{_score_label(average_score)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Questions</div>
                <div class="metric-value">{questions_answered}</div>
                <div class="metric-note">Questions answered</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with k4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Readiness</div>
                <div class="metric-value">{readiness:.1f}%</div>
                <div class="metric-note">{_score_label(readiness)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # --------------------------------------------------------
    # PERFORMANCE TREND
    # --------------------------------------------------------
    st.subheader("📈 Performance Trend")

    if len(completed_for_chart) >= 1:
        chart_rows = []

        for index, interview in enumerate(completed_for_chart, start=1):
            chart_rows.append(
                {
                    "Interview": index,
                    "Overall Score": _safe_float(
                        interview.get("overall_score")
                    ),
                    "Readiness": _safe_float(
                        interview.get("readiness_score")
                    ),
                }
            )

        chart_df = pd.DataFrame(chart_rows).set_index("Interview")

        with st.container(border=True):
            st.line_chart(
                chart_df,
                use_container_width=True,
                height=300,
            )

        if len(completed_for_chart) == 1:
            st.caption(
                "Complete more interviews to see your performance "
                "trend develop over time."
            )
    else:
        with st.container(border=True):
            st.markdown(
                """
                <div class="empty-state">
                    Complete your first interview to start building
                    your performance timeline.
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    # --------------------------------------------------------
    # SKILLS + READINESS
    # --------------------------------------------------------
    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.subheader("🧠 Skill Performance")

        with st.container(border=True):
            _render_score_bar("Technical Knowledge", technical)
            _render_score_bar("Communication", communication)
            _render_score_bar("Problem Solving", problem_solving)
            _render_score_bar("Answer Structure", answer_structure)

    with right:
        st.subheader("🎯 Readiness")

        with st.container(border=True):
            st.metric(
                "Interview Readiness",
                f"{readiness:.1f}%"
            )

            st.progress(
                min(max(readiness / 100, 0), 1)
            )

            if readiness >= 85:
                st.success(
                    "You're showing strong interview readiness."
                )
            elif readiness >= 70:
                st.info(
                    "You're building a solid interview foundation."
                )
            elif interviews_completed:
                st.warning(
                    "More focused practice will help improve readiness."
                )
            else:
                st.caption(
                    "Your readiness score will appear after "
                    "your first completed interview."
                )

    st.write("")

    # --------------------------------------------------------
    # TOPIC PERFORMANCE
    # --------------------------------------------------------
    st.subheader("🎯 Topic Performance")

    if weak_topics:
        topic_columns = st.columns(2)

        # Weakest topics first, with the best available data.
        for index, topic in enumerate(weak_topics):
            with topic_columns[index % 2]:
                _render_topic_card(topic)
    else:
        with st.container(border=True):
            st.markdown(
                """
                <div class="empty-state">
                    Topic-level performance will appear as you
                    practice more interviews.
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    # --------------------------------------------------------
    # --------------------------------------------------------
    # INTELLIGENT ANALYTICS
    # --------------------------------------------------------
    st.subheader("🧠 Intelligent Performance Analytics")

    chronological = list(reversed(completed))
    recent = chronological[-3:]
    previous = chronological[-6:-3] if len(chronological) > 3 else []

    recent_average = _average_for(recent, "overall_score")
    previous_average = (
        _average_for(previous, "overall_score")
        if previous else None
    )
    overall_change = _change(recent_average, previous_average)

    best_score = 0.0
    best_number = None
    for number, interview in enumerate(chronological, start=1):
        score = interview.get("overall_score")
        if _valid_score(score) and float(score) > best_score:
            best_score = float(score)
            best_number = number

    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            st.caption("RECENT PERFORMANCE")
            st.metric("Last 3 Interviews", f"{recent_average:.1f}%")
            _render_trend_badge(overall_change)

    with c2:
        with st.container(border=True):
            st.caption("BEST INTERVIEW")
            st.metric(
                f"Interview #{best_number}" if best_number else "Best Score",
                f"{best_score:.1f}%" if best_number else "—",
            )

    with c3:
        with st.container(border=True):
            st.caption("CURRENT DIRECTION")
            st.metric("Performance", _direction(overall_change))
            st.caption(
                "Compared with the previous interview group."
                if previous else
                "Complete more interviews for a comparison."
            )

    st.write("")

    skills = _skill_analytics(chronological)

    left, right = st.columns([1.1, 0.9], gap="large")

    with left:
        st.subheader("📊 Skill Movement")
        with st.container(border=True):
            if len(chronological) < 2:
                st.info(
                    "Complete one more interview to compare how each "
                    "skill is changing."
                )
            else:
                for skill in skills:
                    change = skill["change"]
                    st.markdown(
                        f"""
                        <div class="analytics-row">
                            <div class="analytics-main">
                                <span class="analytics-name">
                                    {skill["name"]}
                                </span>
                                <span class="analytics-score">
                                    {skill["recent"]:.1f}%
                                </span>
                            </div>
                            <div class="analytics-sub">
                                <span>Recent 3 interviews</span>
                                <span class="{_trend_class(change)}">
                                    {_trend_symbol(change)}
                                    {abs(change):.1f} pts
                                </span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    with right:
        st.subheader("🎯 Performance Signal")
        with st.container(border=True):
            evaluated = [s for s in skills if s["recent"] > 0]

            if evaluated:
                strongest = max(evaluated, key=lambda s: s["recent"])
                priority = min(evaluated, key=lambda s: s["recent"])

                st.markdown(
                    f"""
                    <div class="analytics-insight">
                        <div class="analytics-insight-title">
                            💪 Strongest: {strongest["name"]}
                        </div>
                        <div class="analytics-insight-body">
                            Recent average:
                            <strong>{strongest["recent"]:.1f}%</strong>
                            <br><br>
                            <strong>⚠️ Priority:</strong>
                            {priority["name"]}
                            ({priority["recent"]:.1f}%)
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.info("Skill signals will appear after scored interviews.")

    st.write("")

    st.subheader("🤖 Mirai Recommendation")

    evaluated = [s for s in skills if s["recent"] > 0]
    declining = [s for s in evaluated if s["change"] < -2]
    improving = [s for s in evaluated if s["change"] > 2]

    if not chronological:
        title = "Your journey starts here"
        body = (
            "Complete your first interview so Mirai can learn from "
            "your actual performance."
        )
    elif len(chronological) < 2:
        title = "Build your performance baseline"
        body = (
            "Complete another interview so Mirai can compare your "
            "scores and identify your improvement pattern."
        )
    elif declining:
        names = ", ".join(s["name"] for s in declining[:2])
        title = f"Watch your {names} performance"
        body = (
            f"Your recent results show a downward movement in {names}. "
            "Focus your next practice session on structured answers "
            "and deliberate practice in these areas."
        )
    elif evaluated:
        weakest = min(evaluated, key=lambda s: s["recent"])
        title = f"Focus next on {weakest['name']}"
        body = (
            f"{weakest['name']} is currently your lowest-scoring skill "
            f"at {weakest['recent']:.1f}% across your recent interviews. "
            "Improving this area should give you the best opportunity "
            "to raise your overall performance."
        )
        if improving:
            body += " Your improving skills show that your practice is working."
    elif overall_change > 2:
        title = "You're moving in the right direction"
        body = (
            f"Your recent average is up {overall_change:.1f} points. "
            "Keep the same practice consistency and maintain that improvement."
        )
    else:
        title = "Your next goal is consistency"
        body = (
            "Your recent performance is relatively stable. Pick one "
            "skill to improve in the next interview instead of trying "
            "to change everything at once."
        )

    st.markdown(
        f"""
        <div class="analytics-insight">
            <div class="analytics-insight-title">{title}</div>
            <div class="analytics-insight-body">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button(
        "🚀 Start Another Interview",
        type="primary",
        use_container_width=True,
    ):
        # progress.py is also a native Streamlit page. Switch back to
        # app.py so its custom router can render interview_setup.
        st.session_state.page = "interview_setup"
        st.switch_page("app.py")

# Streamlit also discovers files inside the pages/ directory as native
# multipage entries. Render this page when it is opened directly from that
# native route, while keeping the function importable by app.py.
if __name__ == "__main__":
    progress_page()