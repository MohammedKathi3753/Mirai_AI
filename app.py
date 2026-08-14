import streamlit as st
import streamlit.components.v1 as components

from datetime import datetime

from database.database import (
    initialize_database,
    create_user,
    authenticate_user,
    get_login_security_status,
    get_interview_history,
    get_interview_answers
)

from pages.profile import profile_page
from pages.progress import progress_page


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Mirai AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE
# ============================================================

initialize_database()


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "welcome"

# Open the public Home page first when the main app is launched.
# The Home page sets this flag before sending the user back to app.py.
if "main_app_active" not in st.session_state:
    st.session_state.main_app_active = False

if not st.session_state.main_app_active:
    st.switch_page("pages/home.py")

if "user" not in st.session_state:
    st.session_state.user = None

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "interview_config" not in st.session_state:
    st.session_state.interview_config = {}

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #F7F8FF 0%,
                #F3F1FF 45%,
                #FFFFFF 100%
            );
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3, h4 {
        color: #20243A !important;
    }

    p {
        color: #68708A;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E6E7F1;
    }

    [data-testid="stSidebar"] * {
        color: #454B66;
    }


    /* ======================================================
       TEXT INPUT
       ====================================================== */

    .stTextInput input,
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #252943 !important;
        -webkit-text-fill-color: #252943 !important;

        border: 1px solid #D8DAE7 !important;
        border-radius: 12px !important;

        font-size: 15px !important;
    }

    .stTextInput input {
        min-height: 46px !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #A2A7B8 !important;
        -webkit-text-fill-color: #A2A7B8 !important;
        opacity: 1 !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        background-color: #FFFFFF !important;
        color: #252943 !important;
        -webkit-text-fill-color: #252943 !important;

        border: 2px solid #7567DE !important;

        box-shadow:
            0 0 0 3px
            rgba(117, 103, 222, 0.10) !important;
    }


    /* ======================================================
       LABELS
       ====================================================== */

    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stSlider label,
    .stRadio label {
        color: #4D5571 !important;
        font-weight: 600 !important;
    }


    /* ======================================================
       SELECTBOX
       ====================================================== */

    [data-baseweb="select"] > div {
        background: #FFFFFF !important;
        color: #30354D !important;

        border: 1px solid #D8DAE7 !important;
        border-radius: 12px !important;
    }

    [data-baseweb="select"] span {
        color: #30354D !important;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        background: #FFFFFF !important;

        color: #57519F !important;
        -webkit-text-fill-color: #57519F !important;

        border: 1px solid #DCDCEF !important;
        border-radius: 12px !important;

        min-height: 46px !important;

        font-weight: 600 !important;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: #F6F4FF !important;

        color: #4C4592 !important;
        -webkit-text-fill-color: #4C4592 !important;

        border-color: #AAA1EF !important;
    }


    /* ======================================================
       PRIMARY BUTTONS
       ====================================================== */

    .stButton > button[kind="primary"] {
        background:
            linear-gradient(
                135deg,
                #6959E6,
                #8978F0
            ) !important;

        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;

        border: none !important;
        border-radius: 12px !important;

        min-height: 50px !important;

        font-size: 15px !important;
        font-weight: 700 !important;

        box-shadow:
            0 8px 24px
            rgba(105, 89, 230, 0.18) !important;
    }

    .stButton > button[kind="primary"]:hover {
        background:
            linear-gradient(
                135deg,
                #5E4FD2,
                #7867E4
            ) !important;

        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }


    /* ======================================================
       FORM BUTTON
       ====================================================== */

    [data-testid="stFormSubmitButton"] button {
        background:
            linear-gradient(
                135deg,
                #6959E6,
                #8978F0
            ) !important;

        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;

        border: none !important;
        border-radius: 12px !important;

        min-height: 50px !important;

        font-size: 15px !important;
        font-weight: 700 !important;

        box-shadow:
            0 8px 24px
            rgba(105, 89, 230, 0.18) !important;
    }

    [data-testid="stFormSubmitButton"] button * {
        color: #FFFFFF !important;
    }


    /* ======================================================
       CARDS
       ====================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;

        border: 1px solid #E4E5F0 !important;
        border-radius: 18px !important;

        box-shadow:
            0 8px 28px
            rgba(50, 45, 100, 0.045) !important;
    }


    /* ======================================================
       METRICS
       ====================================================== */

    [data-testid="stMetric"] {
        background: #FFFFFF !important;

        border: 1px solid #E4E5F0 !important;
        border-radius: 16px !important;

        padding: 18px !important;

        box-shadow:
            0 7px 22px
            rgba(50, 45, 100, 0.045);
    }

    [data-testid="stMetricLabel"] {
        color: #747A91 !important;
    }

    [data-testid="stMetricValue"] {
        color: #292D47 !important;
    }


    /* ======================================================
       PROGRESS
       ====================================================== */

    .stProgress > div > div > div {
        background: #7464DE !important;
        border-radius: 10px;
    }


    /* ======================================================
       RADIO
       ====================================================== */

    [data-testid="stRadio"] label {
        color: #4D5571 !important;
    }


    /* ======================================================
       DIVIDER
       ====================================================== */

    hr {
        border-color: #E6E7F1 !important;
    }


    /* ======================================================
       AUTHENTICATION ICON
       ====================================================== */

    .auth-icon {
        text-align: center;
        font-size: 55px;
        margin-bottom: 5px;
    }


    /* ======================================================
       AUTHENTICATION HEADING
       ====================================================== */

    .auth-heading {
        text-align: center;
        color: #20243A !important;

        font-size: 40px;
        font-weight: 750;

        margin-bottom: 8px;
    }

    .auth-description {
        text-align: center;
        color: #747B92 !important;

        font-size: 16px;
        line-height: 1.6;

        margin-bottom: 28px;
    }


    /* ======================================================
       QUESTION AREA
       ====================================================== */

    .question-box {
        background: #FFFFFF;

        border: 1px solid #E3E0F2;
        border-left: 5px solid #7567DE;

        border-radius: 18px;

        padding: 28px;

        margin-top: 18px;
        margin-bottom: 20px;

        box-shadow:
            0 10px 28px
            rgba(70, 60, 140, 0.06);
    }

    .question-label {
        color: #7567DE;

        font-size: 12px;
        font-weight: 800;

        letter-spacing: 1px;
        text-transform: uppercase;

        margin-bottom: 12px;
    }

    .question-text {
        color: #252943;

        font-size: 20px;
        font-weight: 650;

        line-height: 1.6;
    }


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .auth-heading {
            font-size: 32px;
        }

        .question-text {
            font-size: 18px;
        }
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
    """,
    unsafe_allow_html=True
)


# ============================================================
# NAVIGATION
# ============================================================

def go_to(page):
    st.session_state.page = page
    st.rerun()


# ============================================================
# LOGOUT
# ============================================================

def logout():

    st.session_state.user = None
    st.session_state.profile = {}
    st.session_state.interview_config = {}
    st.session_state.current_question = 0
    st.session_state.answers = []
    st.session_state.interview_started = False
    st.session_state.page = "welcome"

    st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

def show_sidebar():

    if st.session_state.user is None:
        return

    user = st.session_state.user

    with st.sidebar:

        st.title("🤖 Mirai AI")

        st.caption(
            "Your Personal AI Interview Coach"
        )

        st.divider()

        if st.button(
            "🏠 Dashboard",
            use_container_width=True
        ):
            go_to("dashboard")

        if st.button(
            "🎯 New Interview",
            use_container_width=True
        ):
            go_to("interview_setup")

        if st.button(
            "📊 Interview Feedback",
            use_container_width=True
        ):
            go_to("feedback")

        if st.button(
            "📄 Resume Analysis",
            use_container_width=True
        ):
            st.switch_page("pages/resume_analysis.py")

        if st.button(
            "🎯 Job Matching",
            use_container_width=True
        ):
            st.switch_page("pages/job_matching.py")

        st.divider()

        st.caption("SIGNED IN AS")

        st.write(
            f"**{user['full_name']}**"
        )

        st.caption(
            user["email"]
        )

        st.write("")

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):
            logout()


# ============================================================
# WELCOME PAGE
# ============================================================

def welcome_page():

    st.write("")
    st.write("")

    left, right = st.columns(
        [1.35, 0.85],
        gap="large"
    )

    with left:

        st.caption(
            "AI INTERVIEW PREPARATION"
        )

        st.title(
            "Prepare smarter.\nInterview better."
        )

        st.write(
            "Mirai AI helps candidates prepare for interviews "
            "through personalized practice, performance analysis "
            "and adaptive coaching."
        )

        st.write("")

        if st.button(
            "🚀 Start Your Preparation",
            type="primary"
        ):
            go_to("login")

    with right:

        with st.container(border=True):

            st.markdown(
                "<div class='auth-icon'>🤖</div>",
                unsafe_allow_html=True
            )

            st.subheader(
                "Meet Mirai"
            )

            st.write(
                "A personal AI coach designed to help you "
                "understand not only what you answered, "
                "but how you can improve."
            )

            st.info(
                "Personalized preparation • Adaptive practice • "
                "Performance insights"
            )

    st.write("")
    st.write("")

    st.subheader(
        "Why Mirai?"
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.subheader(
                "🧠 Adaptive Coaching"
            )

            st.write(
                "Preparation can adapt to your performance "
                "instead of giving every candidate the same "
                "questions."
            )

    with col2:

        with st.container(border=True):

            st.subheader(
                "🎤 Realistic Practice"
            )

            st.write(
                "Practice technical, behavioral, project-based "
                "and mixed interview scenarios."
            )

    with col3:

        with st.container(border=True):

            st.subheader(
                "📊 Performance Intelligence"
            )

            st.write(
                "Understand your strengths, weaknesses and "
                "progress over multiple sessions."
            )

    st.write("")

    st.info(
        "💡 Mirai is built around one idea: "
        "interview preparation should be personalized."
    )


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.write("")
    st.write("")

    left, center, right = st.columns(
        [0.65, 1.7, 0.65]
    )

    with center:

        st.markdown(
            "<div class='auth-icon'>🔐</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='auth-heading'>Welcome Back</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='auth-description'>"
            "Login to continue your personalized "
            "Mirai AI interview journey."
            "</div>",
            unsafe_allow_html=True
        )

        with st.container(border=True):

            st.subheader(
                "Sign in to your account"
            )

            st.caption(
                "Enter your account details to continue."
            )

            # ------------------------------------------------
            # LIVE LOGIN SECURITY STATUS
            # ------------------------------------------------

            status_email = st.session_state.get(
                "login_status_email",
                ""
            )

            if status_email:

                try:
                    security_status = get_login_security_status(
                        status_email
                    )
                except Exception:
                    security_status = {
                        "attempts_left": 5,
                        "locked": False,
                        "seconds_remaining": 0
                    }

                if security_status["locked"]:

                    seconds = int(
                        security_status["seconds_remaining"]
                    )

                    st.error(
                        "🔒 Too many unsuccessful login attempts."
                    )

                    components.html(
                        f"""
                        <div style="
                            text-align:center;
                            padding:14px 10px;
                            border-radius:12px;
                            background:#FFF4F4;
                            border:1px solid #F2C7C7;
                            font-family:Arial,sans-serif;
                        ">
                            <div style="
                                font-size:14px;
                                color:#7A3030;
                                margin-bottom:6px;
                            ">
                                You can try again in
                            </div>

                            <div id="countdown" style="
                                font-size:28px;
                                font-weight:700;
                                color:#B33A3A;
                            ">
                                Calculating...
                            </div>
                        </div>

                        <script>
                            let remaining = {seconds};

                            function updateCountdown() {{
                                if (remaining <= 0) {{
                                    document.getElementById(
                                        "countdown"
                                    ).innerText = "You can try again now";
                                    setTimeout(
                                        () => window.parent.location.reload(),
                                        1000
                                    );
                                    return;
                                }}

                                const minutes = Math.floor(
                                    remaining / 60
                                );
                                const secs = remaining % 60;

                                document.getElementById(
                                    "countdown"
                                ).innerText =
                                    String(minutes).padStart(2, "0")
                                    + ":"
                                    + String(secs).padStart(2, "0");

                                remaining--;
                            }}

                            updateCountdown();
                            setInterval(updateCountdown, 1000);
                        </script>
                        """,
                        height=105,
                        scrolling=False
                    )

                else:

                    attempts_left = int(
                        security_status["attempts_left"]
                    )

                    if attempts_left < 5:

                        st.warning(
                            f"⚠️ {attempts_left} login "
                            f"attempt"
                            f"{'s' if attempts_left != 1 else ''} "
                            "remaining before temporary lock."
                        )

            with st.form("login_form"):

                email = st.text_input(
                    "Email Address",
                    placeholder="you@example.com"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                st.write("")

                login_button = st.form_submit_button(
                    "Sign In →",
                    use_container_width=True
                )

            if login_button:

                email = email.strip()

                st.session_state.login_status_email = email

                if not email or not password:

                    st.error(
                        "Please enter your email and password."
                    )

                else:

                    try:

                        security_status = get_login_security_status(
                            email
                        )

                        if security_status["locked"]:

                            st.error(
                                "🔒 Too many unsuccessful login "
                                "attempts. Please wait for the "
                                "lockout timer to finish."
                            )

                        else:

                            user = authenticate_user(
                                email,
                                password
                            )

                            if user is None:

                                new_status = (
                                    get_login_security_status(
                                        email
                                    )
                                )

                                if new_status["locked"]:

                                    st.error(
                                        "🔒 Too many unsuccessful "
                                        "login attempts. Your account "
                                        "is temporarily locked."
                                    )

                                else:

                                    attempts_left = int(
                                        new_status["attempts_left"]
                                    )

                                    st.error(
                                        "❌ Incorrect email or password."
                                    )

                                    st.warning(
                                        f"⚠️ {attempts_left} login "
                                        f"attempt"
                                        f"{'s' if attempts_left != 1 else ''} "
                                        "remaining before temporary lock."
                                    )

                            else:

                                st.session_state.user = user
                                st.session_state.login_status_email = ""
                                go_to("dashboard")

                    except Exception:

                        st.error(
                            "❌ Unable to sign in right now. "
                            "Please try again later."
                        )

            st.write("")

            st.caption(
                "Don't have a Mirai AI account?"
            )

            if st.button(
                "Create New Account",
                use_container_width=True
            ):
                go_to("signup")

        st.write("")

        if st.button(
            "← Back to Welcome",
            use_container_width=True
        ):
            st.session_state.login_status_email = ""
            go_to("welcome")



# ============================================================
# SIGNUP PAGE
# ============================================================

def signup_page():

    st.write("")
    st.write("")

    left, center, right = st.columns(
        [0.45, 2.1, 0.45]
    )

    with center:

        st.markdown(
            "<div class='auth-icon'>📝</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='auth-heading'>"
            "Create Your Account"
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='auth-description'>"
            "Build your personalized Mirai AI "
            "interview preparation profile."
            "</div>",
            unsafe_allow_html=True
        )

        with st.container(border=True):

            st.subheader(
                "Tell us about yourself"
            )

            st.caption(
                "This information helps Mirai personalize "
                "your preparation experience."
            )

            full_name = st.text_input(
                "Full Name",
                placeholder="Enter your full name"
            )

            email = st.text_input(
                "Email Address",
                placeholder="you@example.com"
            )

            col1, col2 = st.columns(2)

            with col1:

                education = st.text_input(
                    "Education",
                    placeholder="BCA / B.Tech / MCA"
                )

            with col2:

                job_role = st.text_input(
                    "Target Job Role",
                    placeholder="AI/ML Engineer"
                )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password"
            )

            st.caption(
                "🔒 Password must contain at least 8 characters."
            )

            st.write("")

            if st.button(
                "Create Account →",
                type="primary",
                use_container_width=True
            ):

                full_name = full_name.strip()
                email = email.strip()
                education = education.strip()
                job_role = job_role.strip()

                if not all([
                    full_name,
                    email,
                    education,
                    job_role,
                    password,
                    confirm_password
                ]):

                    st.error(
                        "Please fill in all fields."
                    )

                elif (
                    "@" not in email
                    or "." not in email
                ):

                    st.error(
                        "Please enter a valid email address."
                    )

                elif len(password) < 8:

                    st.error(
                        "Password must contain at least 8 characters."
                    )

                elif password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

                else:

                    try:

                        result = create_user(
                            full_name,
                            email,
                            password
                        )

                        if isinstance(result, tuple):

                            success = result[0]

                            message = (
                                result[1]
                                if len(result) > 1
                                else ""
                            )

                        else:

                            success = bool(result)
                            message = ""

                        if success:

                            st.session_state.profile = {
                                "full_name": full_name,
                                "email": email,
                                "education": education,
                                "job_role": job_role
                            }

                            st.success(
                                "✅ Account created successfully!"
                            )

                            st.info(
                                "Your account is ready. "
                                "Please sign in."
                            )

                            st.session_state.page = "login"

                            st.rerun()

                        else:

                            if message:

                                st.error(
                                    f"❌ {message}"
                                )

                            else:

                                st.error(
                                    "❌ Unable to create account. "
                                    "The email may already exist."
                                )

                    except Exception as error:

                        error_text = str(error).lower()

                        if (
                            "unique" in error_text
                            or
                            "already exists" in error_text
                            or
                            "integrity" in error_text
                        ):

                            st.error(
                                "❌ An account with this "
                                "email already exists."
                            )

                        else:

                            st.error(
                                "❌ Unable to create your account "
                                "right now. Please try again later."
                            )

        st.write("")

        if st.button(
            "← Back to Login",
            use_container_width=True
        ):
            go_to("login")


# ============================================================
# DASHBOARD
# ============================================================

def dashboard_page():

    user = st.session_state.user
    first_name = user["full_name"].split()[0]

    # ========================================================
    # LOAD REAL INTERVIEW DATA
    # ========================================================

    try:
        interviews = get_interview_history(user["id"])
    except Exception:
        interviews = []

    completed_interviews = [
        interview
        for interview in interviews
        if interview.get("status") == "completed"
    ]

    # ========================================================
    # CALCULATE DASHBOARD STATISTICS
    # ========================================================

    interviews_completed = len(completed_interviews)

    scores = [
        float(interview["overall_score"])
        for interview in completed_interviews
        if interview.get("overall_score") is not None
    ]

    average_score = (
        round(sum(scores) / len(scores), 1)
        if scores else 0
    )

    questions_practiced = sum(
        int(interview.get("completed_questions", 0) or 0)
        for interview in completed_interviews
    )

    if completed_interviews:
        latest_interview = completed_interviews[0]
        latest_readiness = latest_interview.get("readiness_score")
        latest_readiness = (
            float(latest_readiness)
            if latest_readiness is not None
            else 0
        )
    else:
        latest_readiness = 0

    # ========================================================
    # DASHBOARD HEADER
    # ========================================================

    st.title(
        f"Welcome back, {first_name} 👋"
    )

    st.write(
        "Let's make your next interview better than your last."
    )

    st.write("")

    left, right = st.columns(
        [1.5, 1],
        gap="large"
    )

    with left:
        with st.container(border=True):
            st.subheader(
                "🎯 Ready for your next interview?"
            )

            st.write(
                "Start a personalized mock interview based "
                "on your target role, interview type and "
                "preparation level."
            )

            st.write("")

            if st.button(
                "🚀 Start New Interview",
                type="primary",
                use_container_width=True
            ):
                go_to("interview_setup")

    with right:
        with st.container(border=True):
            st.subheader(
                "🤖 Mirai Coach"
            )

            st.write(
                "Your personal AI interview preparation partner."
            )

            if interviews_completed > 0:
                st.success(
                    "Interview progress updated"
                )
            else:
                st.success(
                    "Ready to practice"
                )

    st.write("")

    # ========================================================
    # YOUR PROGRESS
    # ========================================================

    st.subheader("📊 Your Progress")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Interviews Completed",
            interviews_completed
        )

    with col2:
        st.metric(
            "Average Score",
            f"{average_score}%"
        )

    with col3:
        st.metric(
            "Questions Practiced",
            questions_practiced
        )

    st.write("")

    # ========================================================
    # INTERVIEW READINESS
    # ========================================================

    st.subheader("🎯 Interview Readiness")

    left, right = st.columns([0.7, 2])

    with left:
        st.metric(
            "Readiness",
            f"{latest_readiness:.1f}%" if interviews_completed else "0%"
        )

    with right:
        with st.container(border=True):
            if interviews_completed == 0:
                st.write(
                    "Complete your first interview to generate "
                    "your personalized readiness score."
                )

                st.progress(0)

                st.caption(
                    "Mirai will combine technical knowledge, "
                    "communication, problem solving and "
                    "answer structure."
                )
            else:
                st.write(
                    "Your latest interview readiness score "
                    "is shown above."
                )

                st.progress(
                    min(max(latest_readiness / 100, 0), 1)
                )

                st.caption(
                    "Mirai combines technical knowledge, "
                    "communication, problem solving and "
                    "answer structure."
                )

    st.write("")

    # ========================================================
    # DEVELOPMENT AREAS
    # ========================================================

    st.subheader("🧠 Development Areas")

    col1, col2 = st.columns(2)

    def show_latest_score(label, key):
        if completed_interviews:
            value = completed_interviews[0].get(key)

            if value is not None:
                st.metric(
                    "Latest Score",
                    f"{float(value):.1f}%"
                )
                return

        st.caption(label)

    with col1:
        with st.container(border=True):
            st.subheader("🔵 Technical Knowledge")
            show_latest_score(
                "Complete an interview to evaluate your "
                "technical performance.",
                "technical_score"
            )

        st.write("")

        with st.container(border=True):
            st.subheader("🟣 Communication")
            show_latest_score(
                "Mirai will evaluate clarity, confidence "
                "and communication.",
                "communication_score"
            )

    with col2:
        with st.container(border=True):
            st.subheader("🟢 Problem Solving")
            show_latest_score(
                "Your approach to technical problems "
                "will be analyzed.",
                "problem_solving_score"
            )

        st.write("")

        with st.container(border=True):
            st.subheader("🟡 Answer Structure")
            show_latest_score(
                "Mirai will analyze how effectively "
                "you structure your answers.",
                "answer_structure_score"
            )


# ============================================================
# INTERVIEW SETUP
# ============================================================

def interview_setup_page():

    user = st.session_state.get("user") or {}
    saved_profile = st.session_state.get("profile") or {}

    # ========================================================
    # LOAD SAVED PROFILE
    # ========================================================

    target_role = (
        user.get("target_job_role")
        or saved_profile.get("job_role")
        or ""
    ).strip()

    education = (
        user.get("education")
        or saved_profile.get("education")
        or ""
    ).strip()

    experience = (
        user.get("experience_level")
        or saved_profile.get("experience")
        or ""
    ).strip()

    technical_skills = (
        user.get("technical_skills")
        or saved_profile.get("skills")
        or ""
    ).strip()

    career_goal = (
        user.get("career_goal")
        or saved_profile.get("career_goal")
        or ""
    ).strip()

    st.title(
        "🎯 Interview Setup"
    )

    st.write(
        "Your saved profile is used automatically to "
        "personalize your interview questions."
    )

    st.write("")

    # ========================================================
    # CANDIDATE PROFILE PREVIEW
    # ========================================================

    with st.container(border=True):

        st.subheader("👤 Candidate Profile")
        st.caption(
            "These details come from My Profile and will be "
            "provided to Mirai AI when generating questions."
        )

        profile_col1, profile_col2 = st.columns(2)

        with profile_col1:
            st.caption("TARGET JOB ROLE")
            st.write(target_role or "Not provided")

            st.caption("EDUCATION")
            st.write(education or "Not provided")

            st.caption("EXPERIENCE LEVEL")
            st.write(experience or "Not provided")

        with profile_col2:
            st.caption("TECHNICAL SKILLS")
            st.write(technical_skills or "Not provided")

            st.caption("CAREER GOAL")
            st.write(career_goal or "Not provided")

        if not target_role:
            st.warning(
                "⚠️ Please add your Target Job Role in My Profile "
                "before starting an interview."
            )

    st.write("")

    left, right = st.columns(
        [1.35, 0.85],
        gap="large"
    )

    with left:

        with st.container(border=True):

            st.subheader(
                "💼 Interview Configuration"
            )

            st.caption(
                "Choose the settings for this interview. "
                "Your candidate profile is already loaded above."
            )

            interview_type = st.selectbox(
                "Interview Type",
                [
                    "Technical",
                    "HR / Behavioral",
                    "Mixed",
                    "Project-Based"
                ]
            )

            if interview_type == "Technical":

                st.info(
                    "🧠 Focuses on technical concepts, "
                    "coding knowledge and problem solving."
                )

            elif interview_type == "HR / Behavioral":

                st.info(
                    "🗣 Focuses on communication, behavioral "
                    "questions and workplace situations."
                )

            elif interview_type == "Mixed":

                st.info(
                    "🎯 Combines technical, behavioral "
                    "and problem-solving questions."
                )

            else:

                st.info(
                    "📂 Focuses on projects, decisions, "
                    "contributions and technical explanations."
                )

            difficulty = st.selectbox(
                "Difficulty",
                [
                    "Easy",
                    "Medium",
                    "Hard",
                    "Adaptive"
                ],
                index=3
            )

            if difficulty == "Adaptive":

                st.info(
                    "🤖 Adaptive Mode: Mirai will adjust "
                    "question difficulty according to your "
                    "performance."
                )

            st.subheader(
                "🧠 Preparation Focus"
            )

            focus_area = st.selectbox(
                "Focus Area",
                [
                    "Overall Performance",
                    "Technical Knowledge",
                    "Communication",
                    "Problem Solving",
                    "Answer Structure"
                ]
            )

            interview_mode = st.radio(
                "Interview Mode",
                [
                    "Practice",
                    "Full Mock Interview"
                ],
                horizontal=True
            )

    with right:

        with st.container(border=True):

            st.subheader(
                "❓ Interview Length"
            )

            st.caption(
                "Choose how many questions "
                "you want to practice."
            )

            number_of_questions = st.slider(
                "Number of Questions",
                min_value=5,
                max_value=20,
                value=10
            )

            if number_of_questions <= 7:

                time_estimate = "10–15 minutes"

            elif number_of_questions <= 12:

                time_estimate = "15–25 minutes"

            elif number_of_questions <= 16:

                time_estimate = "25–35 minutes"

            else:

                time_estimate = "35–45 minutes"

            st.write("")

            st.subheader(
                "✨ Interview Preview"
            )

            st.write(
                f"**Role:** {target_role or 'Not provided'}"
            )

            st.write(
                f"**Type:** {interview_type}"
            )

            st.write(
                f"**Difficulty:** {difficulty}"
            )

            st.write(
                f"**Questions:** {number_of_questions}"
            )

            st.write(
                f"**Estimated time:** {time_estimate}"
            )

    st.write("")
    st.write("")

    if st.button(
        "🚀 Start Interview",
        type="primary",
        use_container_width=True
    ):

        if not target_role:

            st.error(
                "Please update your Target Job Role in My Profile first."
            )

        else:

            # ====================================================
            # SAVE INTERVIEW CONFIGURATION
            # ====================================================

            candidate_profile = {
                "full_name": user.get(
                    "full_name",
                    saved_profile.get("full_name", "")
                ),
                "email": user.get(
                    "email",
                    saved_profile.get("email", "")
                ),
                "education": education,
                "job_role": target_role,
                "experience": experience,
                "skills": technical_skills,
                "career_goal": career_goal
            }

            st.session_state.interview_config = {
                "target_role": target_role,
                "interview_type": interview_type,
                "difficulty": difficulty,
                "number_of_questions": number_of_questions,
                "interview_mode": interview_mode,
                "focus_area": focus_area,
                "candidate_profile": candidate_profile
            }

            # ====================================================
            # PASS SETTINGS TO pages/interview.py
            # ====================================================

            st.session_state.selected_job_role = target_role

            st.session_state.selected_interview_type = (
                interview_type
            )

            st.session_state.selected_difficulty = (
                difficulty
            )

            st.session_state.selected_question_count = (
                number_of_questions
            )

            st.session_state.selected_interview_mode = (
                interview_mode
            )

            st.session_state.selected_focus_area = (
                focus_area
            )

            st.session_state.candidate_profile = candidate_profile

            # ====================================================
            # RESET OLD APP-LEVEL INTERVIEW STATE
            # ====================================================

            st.session_state.current_question = 0
            st.session_state.answers = []
            st.session_state.interview_started = False

            # ====================================================
            # OPEN THE REAL INTERVIEW ENGINE PAGE
            # ====================================================

            st.switch_page(
                "pages/interview.py"
            )

    st.write("")

    if st.button(
        "← Back to Dashboard",
        use_container_width=True
    ):
        go_to("dashboard")


# ============================================================
# INTERVIEW SESSION
# ============================================================

# ============================================================
# FEEDBACK
# ============================================================

def feedback_page():

    user = st.session_state.user

    # ========================================================
    # LOAD COMPLETED INTERVIEWS
    # ========================================================

    try:
        interviews = get_interview_history(user["id"])
    except Exception as error:
        st.error(
            f"Could not load interview history: {error}"
        )
        return

    completed_interviews = [
        interview
        for interview in interviews
        if interview.get("status") == "completed"
    ]

    st.title("📊 Interview Feedback")

    st.write(
        "Your personalized performance analysis."
    )

    # ========================================================
    # NO COMPLETED INTERVIEW
    # ========================================================

    if not completed_interviews:

        st.info(
            "Complete an interview first to see "
            "your personalized feedback."
        )

        st.write("")

        if st.button(
            "🚀 Start Your First Interview",
            type="primary",
            use_container_width=True
        ):
            go_to("interview_setup")

        return

    # ========================================================
    # LATEST INTERVIEW
    # ========================================================

    latest_interview = completed_interviews[0]
    interview_id = latest_interview.get("id")

    # ========================================================
    # LOAD AI EVALUATIONS
    # ========================================================

    try:
        evaluations = get_interview_answers(user["id"], interview_id)
    except Exception as error:
        st.error(
            f"Could not load interview feedback: {error}"
        )
        return

    # ========================================================
    # INTERVIEW DETAILS
    # ========================================================

    role = latest_interview.get(
        "target_job_role",
        "Interview"
    )

    interview_type = latest_interview.get(
        "interview_type",
        "General"
    )

    difficulty = latest_interview.get(
        "difficulty",
        "Adaptive"
    )

    st.caption(
        f"{role} • {interview_type} • {difficulty}"
    )

    st.write("")

    # ========================================================
    # MAIN SCORES
    # ========================================================

    overall_score = latest_interview.get(
        "overall_score"
    ) or 0

    technical_score = latest_interview.get(
        "technical_score"
    ) or 0

    communication_score = latest_interview.get(
        "communication_score"
    ) or 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Overall Score",
            f"{float(overall_score):.1f}%"
        )

    with col2:
        st.metric(
            "Technical",
            f"{float(technical_score):.1f}%"
        )

    with col3:
        st.metric(
            "Communication",
            f"{float(communication_score):.1f}%"
        )

    st.write("")

    # ========================================================
    # PERFORMANCE BREAKDOWN
    # ========================================================

    st.subheader("📊 Performance Breakdown")

    problem_solving_score = latest_interview.get(
        "problem_solving_score"
    ) or 0

    answer_structure_score = latest_interview.get(
        "answer_structure_score"
    ) or 0

    readiness_score = latest_interview.get(
        "readiness_score"
    ) or 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Technical",
            f"{float(technical_score):.1f}%"
        )

    with col2:
        st.metric(
            "Communication",
            f"{float(communication_score):.1f}%"
        )

    with col3:
        st.metric(
            "Problem Solving",
            f"{float(problem_solving_score):.1f}%"
        )

    with col4:
        st.metric(
            "Answer Structure",
            f"{float(answer_structure_score):.1f}%"
        )

    st.write("")

    # ========================================================
    # READINESS
    # ========================================================

    st.subheader("🎯 Interview Readiness")

    st.metric(
        "Readiness Score",
        f"{float(readiness_score):.1f}%"
    )

    st.progress(
        min(
            max(float(readiness_score) / 100, 0),
            1
        )
    )

    st.write("")

    # ========================================================
    # COLLECT AI FEEDBACK
    # ========================================================

    strengths = []
    weaknesses = []
    recommendations = []
    feedback_items = []

    for evaluation in evaluations:

        strength = evaluation.get("strengths")
        weakness = evaluation.get("weaknesses")
        recommendation = evaluation.get(
            "recommended_action"
        )
        feedback = evaluation.get("feedback")

        if strength:
            strengths.append(strength)

        if weakness:
            weaknesses.append(weakness)

        if recommendation:
            recommendations.append(
                recommendation
            )

        if feedback:
            feedback_items.append(feedback)

    # ========================================================
    # STRENGTHS + IMPROVEMENT AREAS
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader("💪 Strengths")

            if strengths:

                for strength in strengths:
                    st.success(strength)

            else:
                st.write(
                    "No strengths recorded."
                )

    with col2:

        with st.container(border=True):

            st.subheader("🎯 Areas to Improve")

            if weaknesses:

                for weakness in weaknesses:
                    st.warning(weakness)

            else:
                st.write(
                    "No improvement areas recorded."
                )

    st.write("")

    # ========================================================
    # RECOMMENDED PRACTICE
    # ========================================================

    with st.container(border=True):

        st.subheader("🧠 Recommended Practice")

        if recommendations:

            unique_recommendations = list(
                dict.fromkeys(recommendations)
            )

            for recommendation in unique_recommendations:
                st.write(
                    f"🚀 {recommendation}"
                )

        else:
            st.write(
                "No specific practice recommendation "
                "was recorded."
            )

    st.write("")

    # ========================================================
    # AI FEEDBACK
    # ========================================================

    with st.container(border=True):

        st.subheader("🤖 Mirai's AI Feedback")

        if feedback_items:

            for index, feedback in enumerate(
                feedback_items,
                start=1
            ):

                st.markdown(
                    f"**Question {index}:**"
                )

                st.info(feedback)

        else:

            st.write(
                "No AI feedback was recorded."
            )

    st.write("")

    # ========================================================
    # QUESTION-BY-QUESTION FEEDBACK
    # ========================================================

    st.subheader(
        "📝 Question-by-Question Feedback"
    )

    if not evaluations:

        st.info(
            "No question evaluations were found "
            "for this interview."
        )

    else:

        for index, evaluation in enumerate(
            evaluations,
            start=1
        ):

            question_text = evaluation.get(
                "question_text",
                f"Question {index}"
            )

            score = evaluation.get(
                "overall_score"
            ) or 0

            with st.expander(
                f"Question {index} • "
                f"{float(score):.1f}%"
            ):

                st.markdown(
                    f"**Question:** {question_text}"
                )

                st.write("")

                answer = evaluation.get(
                    "user_answer"
                )

                if answer:

                    st.markdown(
                        "#### 💬 Your Answer"
                    )

                    st.write(answer)

                    st.write("")

                st.markdown(
                    "#### 📊 Score Breakdown"
                )

                evaluation_technical = (
                    evaluation.get(
                        "technical_score"
                    ) or 0
                )

                evaluation_communication = (
                    evaluation.get(
                        "communication_score"
                    ) or 0
                )

                evaluation_problem_solving = (
                    evaluation.get(
                        "problem_solving_score"
                    ) or 0
                )

                evaluation_structure = (
                    evaluation.get(
                        "answer_structure_score"
                    ) or 0
                )

                score_col1, score_col2 = st.columns(2)

                with score_col1:

                    st.metric(
                        "Technical",
                        f"{float(evaluation_technical):.1f}%"
                    )

                    st.metric(
                        "Problem Solving",
                        f"{float(evaluation_problem_solving):.1f}%"
                    )

                with score_col2:

                    st.metric(
                        "Communication",
                        f"{float(evaluation_communication):.1f}%"
                    )

                    st.metric(
                        "Answer Structure",
                        f"{float(evaluation_structure):.1f}%"
                    )

                st.write("")

                strength = evaluation.get(
                    "strengths"
                )

                if strength:

                    st.markdown(
                        "#### 💪 Strength"
                    )

                    st.success(strength)

                weakness = evaluation.get(
                    "weaknesses"
                )

                if weakness:

                    st.markdown(
                        "#### 🎯 Areas to Improve"
                    )

                    st.warning(weakness)

                feedback = evaluation.get(
                    "feedback"
                )

                if feedback:

                    st.markdown(
                        "#### 💬 Mirai's Feedback"
                    )

                    st.info(feedback)

                recommendation = evaluation.get(
                    "recommended_action"
                )

                if recommendation:

                    st.markdown(
                        "#### 🚀 Recommended Next Step"
                    )

                    st.write(
                        recommendation
                    )

    st.write("")

    # ========================================================
    # RETURN TO DASHBOARD
    # ========================================================

    if st.button(
        "🏠 Return to Dashboard",
        type="primary",
        use_container_width=True
    ):
        go_to("dashboard")


# ============================================================
# PROGRESS
# ============================================================

def progress_page():

    user = st.session_state.user

    try:
        interviews = get_interview_history(user["id"])
    except Exception:
        interviews = []

    completed_interviews = [
        interview
        for interview in interviews
        if interview.get("status") == "completed"
    ]

    st.title("📈 My Progress")

    st.write(
        "Track your development across interview sessions."
    )

    st.write("")

    if not completed_interviews:

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.subheader("🧠 Technical Knowledge")
                st.metric("Current Score", "—")

        with col2:
            with st.container(border=True):
                st.subheader("🗣 Communication")
                st.metric("Current Score", "—")

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.subheader("🧩 Problem Solving")
                st.metric("Current Score", "—")

        with col2:
            with st.container(border=True):
                st.subheader("📝 Answer Structure")
                st.metric("Current Score", "—")

        st.write("")

        with st.container(border=True):
            st.subheader("📊 Performance Trend")
            st.info(
                "Complete your first interview to start "
                "tracking your performance."
            )

        return

    def average_score(key):
        values = []

        for interview in completed_interviews:
            value = interview.get(key)
            if value is None:
                continue
            try:
                values.append(float(value))
            except (TypeError, ValueError):
                continue

        if not values:
            return None

        return round(sum(values) / len(values), 1)

    technical_average = average_score("technical_score")
    communication_average = average_score("communication_score")
    problem_solving_average = average_score("problem_solving_score")
    answer_structure_average = average_score("answer_structure_score")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("🧠 Technical Knowledge")
            st.metric(
                "Current Score",
                f"{technical_average:.1f}%"
                if technical_average is not None else "—"
            )

    with col2:
        with st.container(border=True):
            st.subheader("🗣 Communication")
            st.metric(
                "Current Score",
                f"{communication_average:.1f}%"
                if communication_average is not None else "—"
            )

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("🧩 Problem Solving")
            st.metric(
                "Current Score",
                f"{problem_solving_average:.1f}%"
                if problem_solving_average is not None else "—"
            )

    with col2:
        with st.container(border=True):
            st.subheader("📝 Answer Structure")
            st.metric(
                "Current Score",
                f"{answer_structure_average:.1f}%"
                if answer_structure_average is not None else "—"
            )

    st.write("")

    with st.container(border=True):
        st.subheader("📊 Performance Trend")

        overall_scores = []

        for interview in reversed(completed_interviews):
            value = interview.get("overall_score")
            if value is None:
                continue
            try:
                overall_scores.append(float(value))
            except (TypeError, ValueError):
                continue

        if len(overall_scores) >= 2:
            st.line_chart(
                overall_scores,
                height=260,
                use_container_width=True
            )
            st.caption(
                "Overall interview score across completed sessions."
            )
        elif len(overall_scores) == 1:
            st.metric(
                "Latest Overall Score",
                f"{overall_scores[0]:.1f}%"
            )
            st.info(
                "Complete another interview to see your performance trend."
            )
        else:
            st.info(
                "Your completed interviews do not have an overall score yet."
            )


# ============================================================
# HISTORY
# ============================================================

def history_page():

    user = st.session_state.user

    try:
        interviews = get_interview_history(user["id"])
    except Exception:
        interviews = []

    completed_interviews = [
        interview
        for interview in interviews
        if interview.get("status") == "completed"
    ]

    st.title("📜 Interview History")

    st.write(
        "Review your previous interview sessions."
    )

    st.write("")

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
            go_to("interview_setup")

        return

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

    for interview in completed_interviews:

        role = interview.get(
            "target_job_role",
            "Unknown Role"
        )
        interview_type = interview.get(
            "interview_type",
            "Unknown Type"
        )
        difficulty = interview.get(
            "difficulty",
            "Unknown"
        )
        overall_score = interview.get("overall_score")
        readiness_score = interview.get("readiness_score")
        completed_questions = interview.get(
            "completed_questions",
            0
        )
        total_questions = interview.get(
            "total_questions",
            0
        )
        completed_at = interview.get("completed_at") or interview.get(
            "created_at"
        )

        with st.container(border=True):

            st.subheader(f"🎯 {role}")

            st.caption(
                f"{format_date(completed_at)}"
            )

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

    if st.button(
        "🚀 Start New Interview",
        type="primary",
        use_container_width=True
    ):
        go_to("interview_setup")


# ============================================================
# SIDEBAR
# ============================================================

show_sidebar()


# ============================================================
# PAGE ROUTING
# ============================================================

if st.session_state.page == "welcome":

    welcome_page()

elif st.session_state.page == "login":

    login_page()

elif st.session_state.page == "signup":

    signup_page()

elif st.session_state.page == "dashboard":

    dashboard_page()

elif st.session_state.page == "interview_setup":

    interview_setup_page()

elif st.session_state.page == "feedback":

    feedback_page()

elif st.session_state.page == "progress":

    progress_page()

elif st.session_state.page == "history":

    history_page()

elif st.session_state.page == "profile":

    profile_page()

else:

    st.session_state.page = "welcome"

    st.rerun()