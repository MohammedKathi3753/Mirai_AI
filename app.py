import streamlit as st


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
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "welcome"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
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
""", unsafe_allow_html=True)


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
    # Features
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
    # Get Started
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

    st.markdown(
        "<h1 class='main-title'>🤖 Welcome Back</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>Login to continue to Mirai AI</div>",
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        email = st.text_input(
            "📧 Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Enter your password"
        )

        st.write("")

        if st.button(
            "Login",
            use_container_width=True
        ):

            if email and password:
                st.session_state.page = "dashboard"
                st.rerun()

            else:
                st.error(
                    "Please enter your email and password."
                )

        st.write("")

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button(
                "Create Account",
                use_container_width=True
            ):
                st.info(
                    "Account creation will be added soon."
                )

        with col_b:
            if st.button(
                "Forgot Password?",
                use_container_width=True
            ):
                st.info(
                    "Password recovery will be added soon."
                )

        st.write("")

        if st.button(
            "← Back to Welcome",
            use_container_width=True
        ):
            st.session_state.page = "welcome"
            st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

def dashboard_page():

    st.markdown(
        "<h1 class='main-title'>🤖 Mirai AI</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='subtitle'>AI Interview Preparation Dashboard</div>",
        unsafe_allow_html=True
    )

    st.success("Login successful! Welcome to Mirai AI.")

    st.write("")

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

    st.subheader("🎯 Start Your Interview Preparation")

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

    if st.button(
        "Logout",
        use_container_width=True
    ):
        st.session_state.page = "welcome"
        st.rerun()


# ============================================================
# PAGE ROUTING
# ============================================================

if st.session_state.page == "welcome":

    welcome_page()

elif st.session_state.page == "login":

    login_page()

elif st.session_state.page == "dashboard":

    dashboard_page()