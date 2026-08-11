import streamlit as st

from database.database import (
    initialize_database,
    create_user,
    authenticate_user
)


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
            "📈 My Progress",
            use_container_width=True
        ):
            go_to("progress")

        if st.button(
            "📜 Interview History",
            use_container_width=True
        ):
            go_to("history")

        if st.button(
            "👤 My Profile",
            use_container_width=True
        ):
            go_to("profile")

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

                if not email or not password:

                    st.error(
                        "Please enter your email and password."
                    )

                else:

                    try:

                        user = authenticate_user(
                            email,
                            password
                        )

                        if user is None:

                            st.error(
                                "❌ Incorrect email or password."
                            )

                        else:

                            st.session_state.user = user

                            go_to("dashboard")

                    except Exception as error:

                        st.error(
                            f"Login error: {error}"
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
                                f"Account creation error: {error}"
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

            st.success(
                "Ready to practice"
            )

    st.write("")
    st.subheader("📊 Your Progress")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Interviews Completed",
            "0"
        )

    with col2:
        st.metric(
            "Average Score",
            "0%"
        )

    with col3:
        st.metric(
            "Questions Practiced",
            "0"
        )

    st.write("")

    st.subheader(
        "🎯 Interview Readiness"
    )

    left, right = st.columns(
        [0.7, 2]
    )

    with left:

        st.metric(
            "Readiness",
            "0%"
        )

    with right:

        with st.container(border=True):

            st.write(
                "Complete your first interview to generate "
                "your personalized readiness score."
            )

            st.progress(0)

            st.caption(
                "Mirai will eventually combine technical "
                "knowledge, communication, problem solving "
                "and answer structure."
            )

    st.write("")

    st.subheader(
        "🧠 Development Areas"
    )

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader(
                "🔵 Technical Knowledge"
            )

            st.caption(
                "Complete an interview to evaluate your "
                "technical performance."
            )

        st.write("")

        with st.container(border=True):

            st.subheader(
                "🟣 Communication"
            )

            st.caption(
                "Mirai will evaluate clarity, confidence "
                "and communication."
            )

    with col2:

        with st.container(border=True):

            st.subheader(
                "🟢 Problem Solving"
            )

            st.caption(
                "Your approach to technical problems "
                "will be analyzed."
            )

        st.write("")

        with st.container(border=True):

            st.subheader(
                "🟡 Answer Structure"
            )

            st.caption(
                "Mirai will analyze how effectively "
                "you structure your answers."
            )


# ============================================================
# INTERVIEW SETUP
# ============================================================

def interview_setup_page():

    st.title(
        "🎯 Interview Setup"
    )

    st.write(
        "Build an interview that matches your goals, "
        "role and current preparation level."
    )

    st.write("")

    left, right = st.columns(
        [1.35, 0.85],
        gap="large"
    )

    with left:

        with st.container(border=True):

            st.subheader(
                "💼 Role & Interview"
            )

            st.caption(
                "Tell Mirai what kind of interview "
                "you want to practice."
            )

            target_role = st.text_input(
                "Target Job Role",
                placeholder="Example: AI/ML Engineer"
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
                    "🤖 Adaptive Mode: Mirai will eventually "
                    "adjust question difficulty according "
                    "to your performance."
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

            preview_role = (
                target_role.strip()
                if target_role.strip()
                else "Not selected"
            )

            st.write(
                f"**Role:** {preview_role}"
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

        if not target_role.strip():

            st.error(
                "Please enter your target job role first."
            )

        else:

            st.session_state.interview_config = {
                "target_role": target_role.strip(),
                "interview_type": interview_type,
                "difficulty": difficulty,
                "number_of_questions": number_of_questions,
                "interview_mode": interview_mode,
                "focus_area": focus_area
            }

            st.session_state.current_question = 0
            st.session_state.answers = []
            st.session_state.interview_started = True

            go_to("interview")

    st.write("")

    if st.button(
        "← Back to Dashboard",
        use_container_width=True
    ):
        go_to("dashboard")


# ============================================================
# INTERVIEW SESSION
# ============================================================

def interview_page():

    config = st.session_state.interview_config

    if not config:

        go_to("interview_setup")
        return

    question_number = (
        st.session_state.current_question + 1
    )

    total_questions = (
        config["number_of_questions"]
    )

    st.title(
        "🎙️ Interview Session"
    )

    st.caption(
        f"{config['target_role']} • "
        f"{config['interview_type']} • "
        f"{config['difficulty']}"
    )

    progress_value = (
        st.session_state.current_question
        / total_questions
    )

    st.progress(progress_value)

    st.write(
        f"Question {question_number} "
        f"of {total_questions}"
    )

    st.write("")

    with st.container(border=True):

        st.caption(
            "INTERVIEW QUESTION"
        )

        st.subheader(
            "Tell me about yourself and explain why "
            "you are interested in this role."
        )

    st.write("")

    answer = st.text_area(
        "Your Answer",
        placeholder=(
            "Write your answer as if you were speaking "
            "to the interviewer..."
        ),
        height=220
    )

    st.write("")

    if st.button(
        "Submit Answer →",
        type="primary",
        use_container_width=True
    ):

        if not answer.strip():

            st.error(
                "Please enter your answer before continuing."
            )

        else:

            st.session_state.answers.append(
                answer.strip()
            )

            if question_number < total_questions:

                st.session_state.current_question += 1

                st.rerun()

            else:

                go_to("feedback")


# ============================================================
# FEEDBACK
# ============================================================

def feedback_page():

    st.title(
        "📊 Interview Feedback"
    )

    st.write(
        "Your personalized performance analysis."
    )

    st.info(
        "The AI evaluation engine will be connected next. "
        "This section will eventually evaluate your answers, "
        "identify weaknesses and generate personalized "
        "recommendations."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Overall Score",
            "—"
        )

    with col2:
        st.metric(
            "Technical",
            "—"
        )

    with col3:
        st.metric(
            "Communication",
            "—"
        )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader(
                "💪 Strengths"
            )

            st.write(
                "AI-generated strengths will appear here."
            )

    with col2:

        with st.container(border=True):

            st.subheader(
                "🎯 Areas to Improve"
            )

            st.write(
                "AI-generated weaknesses will appear here."
            )

    st.write("")

    with st.container(border=True):

        st.subheader(
            "🧠 Recommended Practice"
        )

        st.write(
            "Mirai will recommend targeted practice "
            "based on your performance."
        )

    st.write("")

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

    st.title(
        "📈 My Progress"
    )

    st.write(
        "Track your development across interview sessions."
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader(
                "🧠 Technical Knowledge"
            )

            st.metric(
                "Current Score",
                "—"
            )

    with col2:

        with st.container(border=True):

            st.subheader(
                "🗣 Communication"
            )

            st.metric(
                "Current Score",
                "—"
            )

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader(
                "🧩 Problem Solving"
            )

            st.metric(
                "Current Score",
                "—"
            )

    with col2:

        with st.container(border=True):

            st.subheader(
                "📝 Answer Structure"
            )

            st.metric(
                "Current Score",
                "—"
            )

    st.write("")

    with st.container(border=True):

        st.subheader(
            "📊 Performance Trend"
        )

        st.info(
            "Complete multiple interviews to generate "
            "your performance trend."
        )


# ============================================================
# HISTORY
# ============================================================

def history_page():

    st.title(
        "📜 Interview History"
    )

    st.write(
        "Review your previous interview sessions."
    )

    st.write("")

    with st.container(border=True):

        st.subheader(
            "No interviews completed yet."
        )

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


# ============================================================
# PROFILE
# ============================================================

def profile_page():

    user = st.session_state.user

    st.title(
        "👤 My Profile"
    )

    st.write(
        "Manage your candidate information."
    )

    st.write("")

    with st.container(border=True):

        st.subheader(
            "Account Information"
        )

        st.write(
            f"**Name:** {user['full_name']}"
        )

        st.write(
            f"**Email:** {user['email']}"
        )

    st.write("")

    st.subheader(
        "🎯 Interview Profile"
    )

    profile = st.session_state.profile

    target_role = st.text_input(
        "Target Job Role",
        value=profile.get(
            "job_role",
            ""
        ),
        placeholder="AI/ML Engineer"
    )

    experience = st.selectbox(
        "Experience Level",
        [
            "Student / Fresher",
            "Entry Level",
            "1–2 Years",
            "3–5 Years",
            "5+ Years"
        ]
    )

    skills = st.text_area(
        "Technical Skills",
        value=profile.get(
            "skills",
            ""
        ),
        placeholder=(
            "Python, Machine Learning, SQL, NLP..."
        )
    )

    career_goal = st.text_area(
        "Career Goal",
        value=profile.get(
            "career_goal",
            ""
        ),
        placeholder=(
            "What role are you preparing for?"
        )
    )

    st.write("")

    if st.button(
        "💾 Save Profile",
        type="primary",
        use_container_width=True
    ):

        st.session_state.profile = {
            **profile,
            "job_role": target_role,
            "experience": experience,
            "skills": skills,
            "career_goal": career_goal
        }

        st.success(
            "Profile saved successfully."
        )


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

elif st.session_state.page == "interview":

    interview_page()

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