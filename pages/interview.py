import html
import os
from io import BytesIO
import streamlit as st
import streamlit.components.v1 as components

from database.database import (
    create_interview,
    save_question,
    save_answer,
    save_evaluation,
    complete_interview,
)

# IMPORTANT:
# Your actual engine is located at:
# src/interview/interview_engine.py
from src.interview.interview_engine import (
    select_adaptive_question,
    evaluate_answer,
    calculate_readiness_score,
)


# ============================================================
# VOICE TRANSCRIPTION
# ============================================================

def transcribe_voice_answer(audio_file):
    """Transcribe a microphone recording using Groq Whisper."""

    if audio_file is None:
        return None

    try:
        from dotenv import load_dotenv
        load_dotenv()

        api_key = (
            os.getenv("GROQ_API_KEY")
            or os.getenv("MIRAI_GROQ_API_KEY")
        )

        if not api_key:
            return None

        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        audio_bytes = audio_file.getvalue()

        if not audio_bytes:
            return None

        result = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=(
                getattr(
                    audio_file,
                    "name",
                    "mirai_voice_answer.wav",
                ),
                BytesIO(audio_bytes),
                getattr(
                    audio_file,
                    "type",
                    "audio/wav",
                ),
            ),
        )

        transcript = getattr(result, "text", "")

        return transcript.strip() if transcript else None

    except Exception:
        return None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Mirai AI • Interview",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# GLOBAL LIGHT UI
# ============================================================

st.html(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    :root {
        --mirai-bg: #F7F8FF;
        --mirai-white: #FFFFFF;
        --mirai-text: #20243A;
        --mirai-muted: #737D96;
        --mirai-light-muted: #9AA3B8;
        --mirai-purple: #6B57E8;
        --mirai-purple-light: #F0EDFF;
        --mirai-border: #E2E4F0;
        --mirai-green: #2E9B68;
        --mirai-red: #D9536F;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(122, 102, 235, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(164, 145, 255, 0.08),
                transparent 25%
            ),
            #F7F8FF;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Remove Streamlit's occasional visible element spacing */
    div[data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }

    /* ======================================================
       TEXT
       ====================================================== */

    h1,
    h2,
    h3,
    h4 {
        color: #20243A !important;
    }

    p,
    label,
    .stCaption {
        color: #56617A !important;
    }

    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        min-height: 50px;

        border-radius: 15px;

        border: 1px solid #DCD7FF;

        background:
            linear-gradient(
                135deg,
                #6754E8,
                #8271EF
            );

        color: #FFFFFF !important;

        font-size: 16px;
        font-weight: 700;

        box-shadow:
            0 10px 25px
            rgba(103, 84, 232, 0.15);

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        color: #FFFFFF !important;

        transform: translateY(-1px);

        box-shadow:
            0 13px 30px
            rgba(103, 84, 232, 0.22);

        border-color: #6B57E8;
    }

    /* ======================================================
       TEXT AREA
       ====================================================== */

    .stTextArea textarea {
        background: #FFFFFF !important;

        color: #20243A !important;

        border: 1px solid #D8DCEA !important;

        border-radius: 16px !important;

        font-size: 16px !important;

        line-height: 1.65 !important;

        padding: 15px !important;
    }

    .stTextArea textarea:focus {
        border-color: #8170EC !important;

        box-shadow:
            0 0 0 2px
            rgba(107, 87, 232, 0.10) !important;
    }

    .stTextArea textarea::placeholder {
        color: #A1A8BA !important;
    }

    /* ======================================================
       PROGRESS
       ====================================================== */

    div[data-testid="stProgressBar"] > div {
        background: #E6E7EF;
        border-radius: 999px;
        height: 9px;
    }

    div[data-testid="stProgressBar"] > div > div {
        background:
            linear-gradient(
                90deg,
                #6B57E8,
                #8C79F2
            );
        border-radius: 999px;
    }

    /* ======================================================
       NATIVE ALERTS
       ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 15px;
    }

    /* ======================================================
       EXPANDERS
       ====================================================== */

    div[data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid #E3E5F0;
        border-radius: 16px;
    }

    /* ======================================================
       METRICS
       ====================================================== */

    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E4F0;
        border-radius: 18px;
        padding: 18px;
    }

    div[data-testid="stMetricLabel"] {
        color: #69738A !important;
    }

    div[data-testid="stMetricValue"] {
        color: #6B57E8 !important;
    }


        /* ======================================================
           MOBILE POLISH — NARROW SCREEN
           ====================================================== */

        @media (max-width: 640px) {

            .block-container {
                padding-left: 0.75rem !important;
                padding-right: 0.75rem !important;
                padding-top: 1.25rem !important;
                padding-bottom: 2.5rem !important;
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

            h1 {
                font-size: 1.8rem !important;
                line-height: 1.2 !important;
            }

            h2 {
                font-size: 1.4rem !important;
            }

            h3 {
                font-size: 1.15rem !important;
            }

            .question-text {
                font-size: 17px !important;
                line-height: 1.55 !important;
            }

            .stTextArea textarea {
                font-size: 16px !important;
                min-height: 170px !important;
            }

            .stButton > button {
                min-height: 48px !important;
            }

            div[data-testid="stMetric"] {
                width: 100% !important;
                box-sizing: border-box !important;
            }

            pre,
            code {
                overflow-wrap: anywhere !important;
                word-break: break-word !important;
            }
        }

    </style>
    """
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "interview_running": False,
    "interview_finished": False,
    "interview_id": None,

    "current_question": None,
    "question_number": 1,
    "total_questions": 10,

    "used_questions": [],
    "question_ids": [],

    "scores": [],
    "evaluations": [],

    "last_evaluation": None,
    "final_result": None,
}


for key, default_value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = default_value


# ============================================================
# USER VALIDATION
# ============================================================

if "user" not in st.session_state:

    st.warning(
        "Please log in before starting an interview."
    )

    st.stop()


user = st.session_state.user


if not isinstance(user, dict):

    st.error(
        "Your login session is invalid. "
        "Please log in again."
    )

    st.stop()


if "id" not in user:

    st.error(
        "User information is incomplete. "
        "Please log in again."
    )

    st.stop()


# ============================================================
# HELPER: NORMALIZE QUESTION
# ============================================================

def normalize_question(question):

    if not isinstance(question, dict):

        return None


    question_text = str(
        question.get(
            "question",
            ""
        )
    ).strip()


    if not question_text:

        return None


    topic = str(
        question.get(
            "topic",
            "General"
        )
    ).strip()


    keywords = question.get(
        "keywords",
        []
    )


    if not isinstance(
        keywords,
        list
    ):

        keywords = []


    return {
        "question": question_text,
        "topic": topic or "General",
        "keywords": keywords,
    }


# ============================================================
# HELPER: DUPLICATE KEY
# ============================================================

def question_key(question):

    if isinstance(
        question,
        dict
    ):

        text = question.get(
            "question",
            ""
        )

    else:

        text = question


    return (
        str(text)
        .strip()
        .casefold()
    )


# ============================================================
# HELPER: UNIQUE ADAPTIVE QUESTION
# ============================================================

def generate_unique_question(
    interview_type,
    scores,
    used_questions,
    question_number,
):

    used_keys = {
        question_key(item)

        for item in used_questions

        if item
    }


    # Ask the engine multiple times if it
    # accidentally returns a previous question.
    for _ in range(20):

        candidate = select_adaptive_question(

            interview_type,

            scores,

            used_questions,

            question_number,
        )


        candidate = normalize_question(
            candidate
        )


        if candidate is None:

            continue


        candidate_key = question_key(
            candidate
        )


        if candidate_key not in used_keys:

            return candidate


    return None


# ============================================================
# HELPER: HTML ESCAPE
# ============================================================

def safe_html(value):

    return html.escape(
        str(value),
        quote=True
    )


# ============================================================
# HELPER: QUESTION CARD
# ============================================================

def render_question_card(
    question,
    question_number,
):

    question_text = safe_html(
        question.get(
            "question",
            ""
        )
    )


    topic = safe_html(
        question.get(
            "topic",
            "General"
        )
    )


    # st.html() is deliberately used here.
    # We DO NOT use st.markdown() for HTML UI.
    st.html(
        f"""
        <div style="
            background:
                linear-gradient(
                    135deg,
                    #FFFFFF 0%,
                    #FBFAFF 100%
                );

            border:
                1px solid #E2DFFF;

            border-radius:
                24px;

            padding:
                34px 38px;

            margin:
                24px 0 24px 0;

            box-shadow:
                0 15px 40px
                rgba(72, 63, 145, 0.08);
        ">

            <div style="
                color:#6B57E8;
                font-size:14px;
                font-weight:800;
                letter-spacing:1px;
                text-transform:uppercase;
                margin-bottom:16px;
            ">
                Question {question_number}
            </div>


            <div style="
                color:#20243A;
                font-size:26px;
                font-weight:700;
                line-height:1.55;
                margin-bottom:24px;
            ">
                {question_text}
            </div>


            <div style="
                display:inline-block;
                background:#F0EDFF;
                color:#5F4BD6;
                border:1px solid #DDD7FF;
                border-radius:999px;
                padding:8px 15px;
                font-size:13px;
                font-weight:700;
            ">
                🧠 {topic}
            </div>

        </div>
        """
    )


# ============================================================
# HELPER: PREVIOUS FEEDBACK CARD
# ============================================================

def render_previous_feedback(evaluation):

    if not isinstance(
        evaluation,
        dict
    ):

        return


    score = evaluation.get(
        "overall_score",
        0
    )


    feedback = safe_html(
        evaluation.get(
            "feedback",
            "No feedback available."
        )
    )


    strengths = safe_html(
        evaluation.get(
            "strengths",
            ""
        )
    )


    weaknesses = safe_html(
        evaluation.get(
            "weaknesses",
            ""
        )
    )


    st.html(
        f"""
        <div style="
            background:
                linear-gradient(
                    135deg,
                    #FFFFFF,
                    #FAF9FF
                );

            border:
                1px solid #E2DFFF;

            border-radius:
                20px;

            padding:
                22px 26px;

            margin:
                20px 0 24px 0;

            box-shadow:
                0 8px 25px
                rgba(72, 63, 145, 0.06);
        ">

            <div style="
                color:#20243A;
                font-size:15px;
                font-weight:750;
                margin-bottom:7px;
            ">
                ✨ Previous Answer
            </div>


            <div style="
                color:#6B57E8;
                font-size:28px;
                font-weight:800;
                margin-bottom:10px;
            ">
                {float(score):.1f}%
            </div>


            <div style="
                color:#56617A;
                font-size:15px;
                line-height:1.6;
                margin-bottom:10px;
            ">
                {feedback}
            </div>


            <div style="
                color:#56617A;
                font-size:14px;
                line-height:1.6;
            ">
                <strong>Strength:</strong>
                {strengths}
            </div>


            <div style="
                color:#56617A;
                font-size:14px;
                line-height:1.6;
                margin-top:6px;
            ">
                <strong>Improve:</strong>
                {weaknesses}
            </div>

        </div>
        """
    )


# ============================================================
# HELPER: AVERAGE SCORE
# ============================================================

def average_score(
    evaluations,
    field,
):

    values = []


    for evaluation in evaluations:

        if not isinstance(
            evaluation,
            dict
        ):

            continue


        value = evaluation.get(
            field
        )


        try:

            if value is not None:

                values.append(
                    float(value)
                )

        except (
            TypeError,
            ValueError,
        ):

            pass


    if not values:

        return 0.0


    return round(
        sum(values) / len(values),
        1
    )


# ============================================================
# HELPER: RESET
# ============================================================

def reset_interview():

    st.session_state.interview_running = False

    st.session_state.interview_finished = False

    st.session_state.interview_id = None

    st.session_state.current_question = None

    st.session_state.question_number = 1

    st.session_state.total_questions = 10

    st.session_state.used_questions = []

    st.session_state.question_ids = []

    st.session_state.scores = []

    st.session_state.evaluations = []

    st.session_state.last_evaluation = None

    st.session_state.final_result = None

# ============================================================
# PAGE HEADER
# ============================================================

st.html(
    """
    <div style="
        margin-bottom:28px;
    ">

        <div style="
            color:#6B57E8;
            font-size:14px;
            font-weight:800;
            letter-spacing:1.5px;
            text-transform:uppercase;
            margin-bottom:8px;
        ">
            MIRAI AI • INTERVIEW
        </div>


        <div style="
            color:#20243A;
            font-size:48px;
            font-weight:800;
            line-height:1.15;
            margin-bottom:10px;
        ">
            🎤 Interview Session
        </div>


        <div style="
            color:#737D96;
            font-size:17px;
            line-height:1.6;
        ">
            Mirai is evaluating your responses and
            adapting the interview as you progress.
        </div>

    </div>
    """
)


# ============================================================
# START SCREEN
# ============================================================

if (
    not st.session_state.interview_running
    and not st.session_state.interview_finished
):


    st.html(
        """
        <div style="
            background:#FFFFFF;

            border:
                1px solid #E2E4F0;

            border-radius:18px;

            padding:18px 22px;

            margin-bottom:22px;

            color:#56617A;

            font-size:15px;
        ">
            ✨ Your interview session is ready.
            Mirai will evaluate every answer and
            adapt upcoming questions.
        </div>
        """
    )


    # Use the same question count selected in Interview Setup.
    selected_question_count = st.session_state.get(
        "selected_question_count",
        st.session_state.get(
            "interview_config",
            {}
        ).get("number_of_questions", 10)
    )

    try:
        selected_question_count = int(selected_question_count)
    except (TypeError, ValueError):
        selected_question_count = 10

    selected_question_count = max(5, min(selected_question_count, 20))

    selected_difficulty = st.session_state.get(
        "selected_difficulty",
        st.session_state.get(
            "interview_config",
            {}
        ).get("difficulty", "Adaptive")
    )

    col1, col2, col3 = st.columns(
        3
    )


    with col1:

        st.html(
            f"""
            <div style="
                background:#FFFFFF;
                border:1px solid #E2E4F0;
                border-radius:20px;
                padding:25px;
                text-align:center;
                box-shadow:
                    0 8px 25px
                    rgba(60,70,120,0.06);
            ">

                <div style="
                    color:#6B57E8;
                    font-size:32px;
                    font-weight:800;
                ">
                    {selected_question_count}
                </div>

                <div style="
                    color:#737D96;
                    font-size:14px;
                    margin-top:5px;
                ">
                    Questions
                </div>

            </div>
            """
        )


    with col2:

        st.html(
            f"""
            <div style="
                background:#FFFFFF;
                border:1px solid #E2E4F0;
                border-radius:20px;
                padding:25px;
                text-align:center;
                box-shadow:
                    0 8px 25px
                    rgba(60,70,120,0.06);
            ">

                <div style="
                    color:#6B57E8;
                    font-size:32px;
                    font-weight:800;
                ">
                    {html.escape(str(selected_difficulty))}
                </div>

                <div style="
                    color:#737D96;
                    font-size:14px;
                    margin-top:5px;
                ">
                    Difficulty
                </div>

            </div>
            """
        )


    with col3:

        st.html(
            f"""
            <div style="
                background:#FFFFFF;
                border:1px solid #E2E4F0;
                border-radius:20px;
                padding:25px;
                text-align:center;
                box-shadow:
                    0 8px 25px
                    rgba(60,70,120,0.06);
            ">

                <div style="
                    color:#6B57E8;
                    font-size:32px;
                    font-weight:800;
                ">
                    AI
                </div>

                <div style="
                    color:#737D96;
                    font-size:14px;
                    margin-top:5px;
                ">
                    Evaluation
                </div>

            </div>
            """
        )


    st.write("")
    st.write("")


    # --------------------------------------------------------
    # Begin interview
    # --------------------------------------------------------

    if st.button(
        "🚀 Begin Interview",
        use_container_width=True,
        key="begin_interview_button",
    ):


        # ----------------------------------------------------
        # Read interview settings
        # ----------------------------------------------------

        interview_type = (
            st.session_state.get(
                "selected_interview_type",
                "Technical"
            )
        )


        difficulty = (
            st.session_state.get(
                "selected_difficulty",
                "Adaptive"
            )
        )


        interview_mode = (
            st.session_state.get(
                "selected_interview_mode",
                "Practice"
            )
        )


        focus_area = (
            st.session_state.get(
                "selected_focus_area",
                "Overall Performance"
            )
        )


        target_role = (
            st.session_state.get(
                "selected_job_role"
            )
        )


        if not target_role:

            if isinstance(
                user,
                dict
            ):

                target_role = user.get(
                    "target_job_role",
                    "AI/ML Engineer"
                )


        if not target_role:

            target_role = (
                "AI/ML Engineer"
            )


        total_questions = (
            st.session_state.get(
                "selected_question_count",
                10
            )
        )


        try:

            total_questions = int(
                total_questions
            )

        except (
            TypeError,
            ValueError,
        ):

            total_questions = 10


        total_questions = max(
            5,
            min(
                total_questions,
                20
            )
        )


        # ----------------------------------------------------
        # Create interview in database
        # ----------------------------------------------------

        try:

            interview_id = create_interview(

                user_id=user["id"],

                target_job_role=target_role,

                interview_type=interview_type,

                difficulty=difficulty,

                interview_mode=interview_mode,

                focus_area=focus_area,

                total_questions=total_questions,
            )

        except Exception as error:

            st.error(
                f"Could not create interview: {error}"
            )

            st.stop()


        if interview_id is None:

            st.error(
                "Unable to create the interview session."
            )

            st.stop()


        # ----------------------------------------------------
        # Reset interview data
        # ----------------------------------------------------

        st.session_state.interview_id = (
            interview_id
        )

        st.session_state.interview_running = True

        st.session_state.interview_finished = False

        st.session_state.question_number = 1

        st.session_state.total_questions = (
            total_questions
        )

        st.session_state.used_questions = []

        st.session_state.question_ids = []

        st.session_state.scores = []

        st.session_state.evaluations = []

        st.session_state.last_evaluation = None

        st.session_state.final_result = None


        # ----------------------------------------------------
        # Generate first question
        # ----------------------------------------------------

        first_question = (
            generate_unique_question(

                interview_type,

                [],

                [],

                1,
            )
        )


        if first_question is None:

            st.session_state.interview_running = False

            st.error(
                "Mirai could not generate the first "
                "interview question."
            )

            st.stop()


        # ----------------------------------------------------
        # Save first question
        # ----------------------------------------------------

        try:

            question_id = save_question(

                user["id"],

                interview_id,

                1,

                first_question[
                    "question"
                ],

                interview_type,

                difficulty,

                first_question[
                    "topic"
                ],

                ", ".join(
                    map(
                        str,
                        first_question[
                            "keywords"
                        ]
                    )
                ),
            )

        except Exception as error:

            st.session_state.interview_running = False

            st.error(
                f"Could not save the first question: {error}"
            )

            st.stop()


        if question_id is None:

            st.session_state.interview_running = False

            st.error(
                "The first question could not be saved."
            )

            st.stop()


        st.session_state.current_question = (
            first_question
        )


        st.session_state.question_ids = [
            question_id
        ]


        st.session_state.used_questions = [
            first_question[
                "question"
            ]
        ]


        st.rerun()


# ============================================================
# ACTIVE INTERVIEW
# ============================================================

elif (
    st.session_state.interview_running
    and not st.session_state.interview_finished
):


    question = (
        st.session_state.current_question
    )


    question_number = (
        st.session_state.question_number
    )


    total_questions = (
        st.session_state.total_questions
    )


    if not question:

        st.error(
            "The current interview question "
            "could not be loaded."
        )

        st.stop()


    # --------------------------------------------------------
    # Progress
    # --------------------------------------------------------

    progress = (
        (question_number - 1)
        / max(
            total_questions,
            1
        )
    )


    progress = max(
        0.0,
        min(
            progress,
            1.0
        )
    )


    st.progress(
        progress
    )


    st.caption(
        f"Question {question_number} "
        f"of {total_questions}"
    )


    # --------------------------------------------------------
    # Previous answer feedback
    # --------------------------------------------------------

    if st.session_state.last_evaluation:

        render_previous_feedback(
            st.session_state.last_evaluation
        )


    # --------------------------------------------------------
    # Question
    # --------------------------------------------------------

    render_question_card(
        question,
        question_number
    )


    # --------------------------------------------------------
    # MIRAI VOICE QUESTION
    # --------------------------------------------------------

    # Use the browser's native Speech Synthesis API.
    # This avoids an extra API call, API-key dependency, and
    # audio-generation latency while keeping the interview flow
    # completely unchanged.
    question_text_for_audio = str(
        question.get("question", "")
    ).strip()

    voice_col1, voice_col2 = st.columns([1, 4])

    with voice_col1:
        components.html(
            f'''
            <button
                onclick="speakQuestion()"
                style="
                    width:100%;
                    min-height:50px;
                    border:1px solid #DCD7FF;
                    border-radius:15px;
                    background:linear-gradient(135deg,#6754E8,#8271EF);
                    color:white;
                    font-size:16px;
                    font-weight:700;
                    cursor:pointer;
                    box-shadow:0 10px 25px rgba(103,84,232,0.15);
                "
            >
                🔊 Hear Question
            </button>

            <script>
            function speakQuestion() {{
                const text = {question_text_for_audio!r};

                if (!("speechSynthesis" in window)) {{
                    alert("Voice playback is not supported by this browser.");
                    return;
                }}

                window.speechSynthesis.cancel();

                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.95;
                utterance.pitch = 1.0;
                utterance.volume = 1.0;

                const voices = window.speechSynthesis.getVoices();
                const englishVoice = voices.find(
                    voice => voice.lang && voice.lang.toLowerCase().startsWith("en")
                );

                if (englishVoice) {{
                    utterance.voice = englishVoice;
                }}

                window.speechSynthesis.speak(utterance);
            }}
            </script>
            ''',
            height=65,
            scrolling=False,
        )

    with voice_col2:
        st.caption(
            "Listen to Mirai read the question aloud. "
            "The text question remains available above."
        )


    # --------------------------------------------------------
    # Answer
    # --------------------------------------------------------

    # --------------------------------------------------------
    # ANSWER METHOD
    # --------------------------------------------------------

    answer_mode = st.radio(
        "Answer method",
        ["⌨️ Type Answer", "🎙️ Voice Answer"],
        horizontal=True,
        key=f"answer_mode_{question_number}",
    )

    answer = ""

    if answer_mode == "⌨️ Type Answer":

        answer = st.text_area(
            "Your Answer",
            height=220,
            placeholder=(
                "Explain your answer clearly. "
                "Use examples where possible..."
            ),
            key=f"answer_box_{question_number}",
        )

    else:

        st.caption(
            "🎙️ Record your answer. Mirai will convert your speech "
            "to text so you can review it before submitting."
        )

        audio_file = st.audio_input(
            "Record your answer",
            sample_rate=16000,
            key=f"voice_answer_{question_number}",
        )

        if audio_file is not None:

            signature = (
                f"{question_number}:"
                f"{len(audio_file.getvalue())}"
            )

            if st.session_state.get(
                "voice_transcript_signature"
            ) != signature:

                with st.spinner(
                    "🎧 Converting your answer to text..."
                ):

                    transcript = transcribe_voice_answer(
                        audio_file
                    )

                st.session_state.voice_transcript = (
                    transcript or ""
                )

                st.session_state.voice_transcript_signature = (
                    signature
                )

            transcript = st.session_state.get(
                "voice_transcript",
                ""
            )

            if transcript:

                st.success(
                    "Voice answer transcribed. "
                    "Review the text before submitting."
                )

                answer = st.text_area(
                    "Review your transcription",
                    value=transcript,
                    height=220,
                    key=f"voice_review_{question_number}",
                )

            else:

                st.warning(
                    "I couldn't transcribe that recording. "
                    "Please record again or switch to Type Answer."
                )

    st.caption(
        "💡 Tip: A strong answer usually includes "
        "your reasoning, an example, and the result."
    )

    st.write("")


    # --------------------------------------------------------
    # Submit
    # --------------------------------------------------------

    if st.button(
        "Submit Answer →",
        use_container_width=True,
        key=(
            f"submit_answer_"
            f"{question_number}"
        ),
    ):


        if not answer.strip():

            st.warning(
                "Please write an answer before continuing."
            )

            st.stop()


        # ----------------------------------------------------
        # Get question ID
        # ----------------------------------------------------

        if not st.session_state.question_ids:

            st.error(
                "Question ID is missing."
            )

            st.stop()


        question_id = (
            st.session_state.question_ids[-1]
        )


        # ----------------------------------------------------
        # Save answer
        # ----------------------------------------------------

        try:

            answer_id = save_answer(

                user["id"],

                st.session_state.interview_id,

                question_id,

                answer.strip()
            )

        except Exception as error:

            st.error(
                f"Could not save your answer: {error}"
            )

            st.stop()


        if answer_id is None:

            st.error(
                "Your answer could not be saved."
            )

            st.stop()


        # ----------------------------------------------------
        # Evaluate answer
        # ----------------------------------------------------

        try:

            evaluation = evaluate_answer(

                answer.strip(),

                question
            )

        except Exception as error:

            st.error(
                f"Mirai could not evaluate your answer: {error}"
            )

            st.stop()


        if not isinstance(
            evaluation,
            dict
        ):

            st.error(
                "Mirai returned an invalid evaluation."
            )

            st.stop()


        # ----------------------------------------------------
        # Normalize evaluation values
        # ----------------------------------------------------

        score_fields = [

            "overall_score",

            "technical_score",

            "communication_score",

            "problem_solving_score",

            "answer_structure_score",

            "relevance_score",

            "confidence_score",
        ]


        for field in score_fields:

            try:

                evaluation[field] = float(
                    evaluation.get(
                        field,
                        0
                    )
                )

            except (
                TypeError,
                ValueError,
            ):

                evaluation[field] = 0.0


        # ----------------------------------------------------
        # Normalize text feedback
        # ----------------------------------------------------

        text_fields = [

            "strengths",

            "weaknesses",

            "feedback",

            "recommended_action",
        ]


        for field in text_fields:

            value = evaluation.get(
                field,
                ""
            )


            if value is None:

                value = ""


            evaluation[field] = str(
                value
            )


        # ----------------------------------------------------
        # Save evaluation
        # ----------------------------------------------------

        try:

            save_evaluation(

                user["id"],

                answer_id,

                evaluation[
                    "overall_score"
                ],

                evaluation[
                    "technical_score"
                ],

                evaluation[
                    "communication_score"
                ],

                evaluation[
                    "problem_solving_score"
                ],

                evaluation[
                    "answer_structure_score"
                ],

                evaluation[
                    "relevance_score"
                ],

                evaluation[
                    "confidence_score"
                ],

                evaluation[
                    "strengths"
                ],

                evaluation[
                    "weaknesses"
                ],

                evaluation[
                    "feedback"
                ],

                evaluation[
                    "recommended_action"
                ],
            )

        except Exception as error:

            st.error(
                f"Could not save evaluation: {error}"
            )

            st.stop()


        # ----------------------------------------------------
        # Store evaluation
        # ----------------------------------------------------

        st.session_state.scores.append(

            evaluation[
                "overall_score"
            ]
        )


        st.session_state.evaluations.append(
            evaluation
        )


        st.session_state.last_evaluation = (
            evaluation
        )


        # ----------------------------------------------------
        # LAST QUESTION
        # ----------------------------------------------------

        if (
            question_number
            >= total_questions
        ):


            # -----------------------------------------------
            # Calculate final scores
            # -----------------------------------------------

            evaluations = (
                st.session_state.evaluations
            )


            overall = average_score(
                evaluations,
                "overall_score"
            )


            technical = average_score(
                evaluations,
                "technical_score"
            )


            communication = average_score(
                evaluations,
                "communication_score"
            )


            problem_solving = average_score(
                evaluations,
                "problem_solving_score"
            )


            structure = average_score(
                evaluations,
                "answer_structure_score"
            )


            try:

                readiness = float(
                    calculate_readiness_score(
                        st.session_state.scores
                    )
                )

            except Exception:

                readiness = overall


            readiness = round(
                readiness,
                1
            )


            # -----------------------------------------------
            # Save completed interview
            # -----------------------------------------------

            try:

                complete_interview(

                    user["id"],

                    st.session_state.interview_id,

                    overall,

                    technical,

                    communication,

                    problem_solving,

                    structure,

                    readiness
                )

            except Exception as error:

                st.error(
                    f"Could not complete interview: {error}"
                )

                st.stop()


            # -----------------------------------------------
            # Final result
            # -----------------------------------------------

            st.session_state.final_result = {

                "overall": overall,

                "technical": technical,

                "communication": communication,

                "problem_solving": problem_solving,

                "structure": structure,

                "readiness": readiness,
            }


            st.session_state.interview_running = False

            st.session_state.interview_finished = True


            st.rerun()


        # ----------------------------------------------------
        # GENERATE NEXT QUESTION
        # ----------------------------------------------------

        interview_type = (
            st.session_state.get(
                "selected_interview_type",
                "Technical"
            )
        )


        difficulty = (
            st.session_state.get(
                "selected_difficulty",
                "Adaptive"
            )
        )


        next_number = (
            question_number + 1
        )


        next_question = (
            generate_unique_question(

                interview_type,

                st.session_state.scores,

                st.session_state.used_questions,

                next_number,
            )
        )


        if next_question is None:

            st.error(
                "Mirai could not find a new question "
                "for this interview. No duplicate question "
                "has been inserted."
            )

            st.stop()


        # ----------------------------------------------------
        # Save next question
        # ----------------------------------------------------

        try:

            next_question_id = save_question(

                user["id"],

                st.session_state.interview_id,

                next_number,

                next_question[
                    "question"
                ],

                interview_type,

                difficulty,

                next_question[
                    "topic"
                ],

                ", ".join(
                    map(
                        str,
                        next_question[
                            "keywords"
                        ]
                    )
                ),
            )

        except Exception as error:

            st.error(
                f"Could not save the next question: {error}"
            )

            st.stop()


        if next_question_id is None:

            st.error(
                "The next question could not be saved."
            )

            st.stop()


        # ----------------------------------------------------
        # Update session
        # ----------------------------------------------------

        st.session_state.question_number = (
            next_number
        )


        st.session_state.current_question = (
            next_question
        )

        st.session_state.question_ids.append(
            next_question_id
        )


        st.session_state.used_questions.append(
            next_question[
                "question"
            ]
        )


        st.rerun()


# ============================================================
# RESULTS
# ============================================================

elif st.session_state.interview_finished:


    result = (
        st.session_state.final_result
    )


    if not isinstance(
        result,
        dict
    ):

        st.error(
            "Interview completed, but the result "
            "could not be loaded."
        )

        st.stop()


    # --------------------------------------------------------
    # Result header
    # --------------------------------------------------------

    st.html(
        """
        <div style="
            text-align:center;
            margin-top:20px;
            margin-bottom:30px;
        ">

            <div style="
                font-size:46px;
                margin-bottom:8px;
            ">
                🎉
            </div>

            <div style="
                color:#20243A;
                font-size:38px;
                font-weight:800;
                margin-bottom:8px;
            ">
                Interview Complete
            </div>

            <div style="
                color:#737D96;
                font-size:16px;
            ">
                Here's how you performed in your Mirai AI interview.
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # Main results
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(
        3
    )


    with col1:

        st.metric(
            "Overall Score",
            f'{result["overall"]:.1f}%'
        )


    with col2:

        st.metric(
            "Readiness",
            f'{result["readiness"]:.1f}%'
        )


    with col3:

        st.metric(
            "Questions",
            str(
                len(
                    st.session_state.scores
                )
            )
        )


    st.write("")


    # --------------------------------------------------------
    # Performance breakdown
    # --------------------------------------------------------

    st.subheader(
        "📊 Performance Breakdown"
    )


    col1, col2, col3, col4 = st.columns(
        4
    )


    with col1:

        st.metric(
            "Technical",
            f'{result["technical"]:.1f}%'
        )


    with col2:

        st.metric(
            "Communication",
            f'{result["communication"]:.1f}%'
        )


    with col3:

        st.metric(
            "Problem Solving",
            f'{result["problem_solving"]:.1f}%'
        )


    with col4:

        st.metric(
            "Answer Structure",
            f'{result["structure"]:.1f}%'
        )


    st.write("")


    # --------------------------------------------------------
    # Question feedback
    # --------------------------------------------------------

    st.subheader(
        "🧠 Question-by-Question Feedback"
    )


    for index, evaluation in enumerate(

        st.session_state.evaluations,

        start=1,
    ):


        score = evaluation.get(
            "overall_score",
            0
        )


        with st.expander(
            f"Question {index} • {float(score):.1f}%"
        ):


            st.markdown(
                "#### 💪 Strengths"
            )


            st.success(
                evaluation.get(
                    "strengths",
                    "No strengths recorded."
                )
            )


            st.markdown(
                "#### 🎯 Areas to Improve"
            )


            st.warning(
                evaluation.get(
                    "weaknesses",
                    "No improvement areas recorded."
                )
            )


            st.markdown(
                "#### 💬 Mirai's Feedback"
            )


            st.info(
                evaluation.get(
                    "feedback",
                    "No feedback recorded."
                )
            )


            st.markdown(
                "#### 🚀 Recommended Next Step"
            )


            st.write(
                evaluation.get(
                    "recommended_action",
                    "Keep practicing."
                )
            )


    st.write("")


    # --------------------------------------------------------
    # Navigation after completed interview

    nav_col1, nav_col2 = st.columns(2)

    with nav_col1:
        if st.button(
            "← Back to Dashboard",
            use_container_width=True,
            key="back_to_dashboard",
            type="primary",
        ):
            reset_interview()
            st.switch_page("app.py")

    with nav_col2:
        if st.button(
            "🔄 Start Another Interview",
            use_container_width=True,
            key="start_another_interview",
        ):
            reset_interview()
            st.rerun()