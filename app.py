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
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "user" not in st.session_state:
    st.session_state.user = None


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0E1117;
    }

    .block-container {
        padding-top: 4rem;
        padding-bottom: 3rem;
        max-width: 1000px;
    }

    .main-title {
        font-size: 56px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 24px;
        text-align: center;
        color: #B8C0CC;
        margin-bottom: 20px;
    }

    .description {
        font-size: 18px;
        text-align: center;
        color: #D5D9E0;
        line-height: 1.6;
        margin-bottom: 35px;
    }

    .feature-card {
        background-color: #171B24;
        border: 1px solid #2A303B;
        border-radius: 15px;
        padding: 25px;
        min-height: 150px;
    }

    .feature-card h3 {
        margin-top: 0;
    }

    .feature-card p {
        color: #B8C0CC;
        line-height: 1.5;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# WELCOME PAGE
# ============================================================

def welcome_page():

    st.markdown(
        "<h1 class='main-title'>🤖 Mirai AI</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>AI Interview Preparation Platform</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='description'>
        Prepare smarter. Practice better. Build confidence for your
        next interview with AI-powered interview preparation.
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Feature Cards
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">
                <h3>🤖 AI Powered</h3>
                <p>
                Get intelligent interview questions and
                personalized feedback based on your answers.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="feature-card">
                <h3>🎯 Mock Interviews</h3>
                <p>
                Practice realistic technical, HR and
                behavioral interviews.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="feature-card">
                <h3>📊 Track Progress</h3>
                <p>
                Monitor your interview scores and
                identify areas for improvement.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.write("")

    # --------------------------------------------------------
    # Get Started Button
    # --------------------------------------------------------

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:

        if st.button(
            "🚀 Get Started",
            use_container_width=True
        ):

            st.session_state.page = "login"
            st.rerun()


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.title("🔐 Login")

    st.write(
        "Login to continue your Mirai AI interview preparation."
    )

    st.write("")

    # --------------------------------------------------------
    # Login Form
    # --------------------------------------------------------

    with st.form("login_form"):

        email = st.text_input(
            "📧 Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Enter your password"
        )

        login_button = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    # --------------------------------------------------------
    # Login Validation
    # --------------------------------------------------------

    if login_button:

        email = email.strip()

        if not email or not password:

            st.error(
                "Please enter your email and password."
            )

        else:

            user = authenticate_user(
                email,
                password
            )

            # ------------------------------------------------
            # Incorrect credentials
            # ------------------------------------------------

            if user is None:

                st.error(
                    "❌ Incorrect email or password."
                )

            # ------------------------------------------------
            # Correct credentials
            # ------------------------------------------------

            else:

                st.session_state.user = user
                st.session_state.page = "dashboard"

                st.rerun()

    # --------------------------------------------------------
    # Other Options
    # --------------------------------------------------------

    st.divider()

    if st.button(
        "📝 Create New Account",
        use_container_width=True
    ):

        st.session_state.page = "signup"
        st.rerun()

    if st.button(
        "← Back to Welcome",
        use_container_width=True
    ):

        st.session_state.page = "welcome"
        st.rerun()


# ============================================================
# SIGN UP PAGE
# ============================================================

def signup_page():

    st.markdown(
        "<h1 class='main-title'>📝 Create Account</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>Create your Mirai AI account</div>",
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # Center Signup Form
    # --------------------------------------------------------

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        full_name = st.text_input(
            "👤 Full Name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "📧 Email Address",
            placeholder="Enter your email"
        )

        education = st.text_input(
            "🎓 Education",
            placeholder="e.g. BCA, B.Tech, MCA"
        )

        job_role = st.text_input(
            "💼 Target Job Role",
            placeholder="e.g. Python Developer, AI/ML Engineer"
        )

        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Create a password"
        )

        confirm_password = st.text_input(
            "🔒 Confirm Password",
            type="password",
            placeholder="Re-enter your password"
        )

        st.write("")

        # ----------------------------------------------------
        # Create Account
        # ----------------------------------------------------

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            # -----------------------------------------------
            # Empty Field Validation
            # -----------------------------------------------

            if not all([
                full_name.strip(),
                email.strip(),
                education.strip(),
                job_role.strip(),
                password,
                confirm_password
            ]):

                st.error(
                    "Please fill in all fields."
                )

            # -----------------------------------------------
            # Email Validation
            # -----------------------------------------------

            elif "@" not in email or "." not in email:

                st.error(
                    "Please enter a valid email address."
                )

            # -----------------------------------------------
            # Password Length
            # -----------------------------------------------

            elif len(password) < 8:

                st.error(
                    "Password must contain at least 8 characters."
                )

            # -----------------------------------------------
            # Password Match
            # -----------------------------------------------

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            # -----------------------------------------------
            # Create User
            # -----------------------------------------------

            else:

                success, message = create_user(
                    full_name.strip(),
                    email.strip(),
                    education.strip(),
                    job_role.strip(),
                    password
                )

                if success:

                    st.success(
                        "✅ Account created successfully!"
                    )

                    st.info(
                        "You can now login using your email and password."
                    )

                    st.session_state.page = "login"

                    st.rerun()

                else:

                    st.error(
                        f"❌ {message}"
                    )

        st.write("")

        # ----------------------------------------------------
        # Back to Login
        # ----------------------------------------------------

        if st.button(
            "← Back to Login",
            use_container_width=True
        ):

            st.session_state.page = "login"
            st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

def dashboard_page():

    # --------------------------------------------------------
    # Security Check
    # --------------------------------------------------------

    if st.session_state.user is None:

        st.session_state.page = "login"
        st.rerun()

    # --------------------------------------------------------
    # Get User Information
    # --------------------------------------------------------

    user = st.session_state.user

    user_id = user[0]
    full_name = user[1]
    email = user[2]
    education = user[3]
    job_role = user[4]

    # --------------------------------------------------------
    # Dashboard Header
    # --------------------------------------------------------

    st.markdown(
        "<h1 class='main-title'>🤖 Mirai AI</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>AI Interview Preparation Dashboard</div>",
        unsafe_allow_html=True
    )

    st.success(
        f"Welcome, {full_name}! 👋"
    )

    st.write("")

    # --------------------------------------------------------
    # User Information
    # --------------------------------------------------------

    st.subheader("👤 Your Profile")

    col1, col2 = st.columns(2)

    with col1:

        st.write(f"**Name:** {full_name}")
        st.write(f"**Email:** {email}")

    with col2:

        st.write(f"**Education:** {education}")
        st.write(f"**Target Role:** {job_role}")

    st.divider()

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

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

    st.divider()

    # --------------------------------------------------------
    # Start Interview
    # --------------------------------------------------------

    st.subheader(
        "🎯 Start Your Interview Preparation"
    )

    st.write(
        "Choose an interview type and start practicing "
        "with AI-powered interview questions."
    )

    st.write("")

    if st.button(
        "🚀 Start New Interview",
        use_container_width=True
    ):

        st.info(
            "Interview setup will be implemented next."
        )

    st.write("")

    # --------------------------------------------------------
    # Logout
    # --------------------------------------------------------

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.user = None
        st.session_state.page = "welcome"

        st.rerun()


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