import html
import streamlit as st

from database.database import (
    update_user_profile,
    save_user_resume,
    get_user_resume,
    delete_user_resume,
)



# ============================================================
# RESUME HELPERS
# ============================================================

def load_resume_metadata(user_id):
    """Return the currently stored resume metadata for the user."""
    try:
        resume = get_user_resume(user_id)

        if not resume:
            return None

        return {
            "id": resume.get("id"),
            "filename": str(
                resume.get("filename", "") or ""
            ).strip(),
            "uploaded_at": str(
                resume.get("uploaded_at", "") or ""
            ).strip(),
            "updated_at": str(
                resume.get("updated_at", "") or ""
            ).strip(),
        }

    except Exception:
        return None


def save_profile_resume(user_id, uploaded_file):
    """Validate and store the original PDF resume."""
    if uploaded_file is None:
        return False, "Please choose a PDF resume."

    filename = str(
        uploaded_file.name or "resume.pdf"
    ).strip()

    if not filename.lower().endswith(".pdf"):
        return False, "Only PDF resumes are supported."

    pdf_data = uploaded_file.getvalue()

    if not pdf_data:
        return False, "The uploaded PDF is empty."

    if not pdf_data.startswith(b"%PDF-"):
        return False, "This file does not appear to be a valid PDF."

    try:
        resume_id = save_user_resume(
            user_id=user_id,
            filename=filename,
            pdf_data=pdf_data,
        )
    except Exception as error:
        return False, f"Could not save your resume: {error}"

    if resume_id is None:
        return False, "Could not save your resume to the database."

    return True, filename


# ============================================================
# PROFILE PAGE
# ============================================================

def profile_page():

    user = st.session_state.get("user")

    if not user:
        st.title("👤 My Profile")
        st.info(
            "Please sign in to your Mirai AI account to view your profile."
        )
        return

    # --------------------------------------------------------
    # Keep the profile data synchronized with the logged-in user
    # --------------------------------------------------------

    profile = {
        "full_name": user.get("full_name", ""),
        "email": user.get("email", ""),
        "education": user.get("education", ""),
        "job_role": user.get("target_job_role", ""),
        "experience": user.get("experience_level", ""),
        "skills": user.get("technical_skills", ""),
        "career_goal": user.get("career_goal", ""),
        "created_at": user.get("created_at", ""),
        "updated_at": user.get("updated_at", "")
    }

    resume = load_resume_metadata(user["id"])

    if "profile_editing" not in st.session_state:
        st.session_state.profile_editing = False

    st.title("👤 My Profile")

    st.write(
        "Keep your candidate information updated so Mirai can "
        "personalize your interview preparation."
    )

    # One-time action notice. It is cleared immediately after
    # being displayed, so it does not remain permanently on the page.
    resume_upload_notice = st.session_state.pop(
        "resume_upload_notice",
        None,
    )

    if resume_upload_notice:
        st.success(resume_upload_notice)

    # ========================================================
    # VIEW MODE
    # ========================================================

    if not st.session_state.profile_editing:

        # ----------------------------------------------------
        # ACCOUNT INFORMATION
        # ----------------------------------------------------

        st.subheader("👤 Account Information")

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:
                st.caption("FULL NAME")
                st.markdown(
                    f"**{profile['full_name'] or 'Not provided'}**"
                )

            with col2:
                st.caption("EMAIL ADDRESS")
                st.markdown(
                    f"**{profile['email'] or 'Not provided'}**"
                )

        st.write("")

        # ----------------------------------------------------
        # EDUCATION & CAREER
        # ----------------------------------------------------

        st.subheader("🎓 Education & Career")

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:
                st.caption("EDUCATION")
                st.write(
                    profile["education"] or "Not provided"
                )

            with col2:
                st.caption("TARGET JOB ROLE")
                st.write(
                    profile["job_role"] or "Not provided"
                )

            st.write("")

            st.caption("EXPERIENCE LEVEL")
            st.write(
                profile["experience"] or "Not provided"
            )

        st.write("")

        # ----------------------------------------------------
        # SKILLS & CAREER GOALS
        # ----------------------------------------------------

        st.subheader("🧠 Skills & Career Goals")

        with st.container(border=True):

            st.caption("TECHNICAL SKILLS")
            st.write(
                profile["skills"] or "Not provided"
            )

            st.write("")

            st.caption("CAREER GOAL")
            st.write(
                profile["career_goal"] or "Not provided"
            )

        st.write("")

        # ----------------------------------------------------
        # RESUME
        # ----------------------------------------------------

        st.subheader("📄 Resume")

        if resume:
            filename = html.escape(
                resume["filename"] or "Resume.pdf"
            )

            st.html(
                f"""
                <div style="
                    background:
                        linear-gradient(
                            135deg,
                            #151722 0%,
                            #10121A 100%
                        );
                    border:1px solid #303442;
                    border-radius:22px;
                    padding:25px 28px;
                    box-shadow:
                        0 10px 30px
                        rgba(0,0,0,0.18);
                ">
                    <div style="
                        display:flex;
                        align-items:center;
                        gap:14px;
                    ">
                        <div style="
                            width:48px;
                            height:48px;
                            border-radius:15px;
                            background:#F0EDFF;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            font-size:23px;
                        ">
                            📄
                        </div>

                        <div style="flex:1;">
                            <div style="
                                color:#F5F6FA;
                                font-size:16px;
                                font-weight:800;
                                line-height:1.4;
                                word-break:break-word;
                            ">
                                {filename}
                            </div>

                            <div style="
                                color:#5F4BD6;
                                font-size:12px;
                                font-weight:800;
                                letter-spacing:0.7px;
                                margin-top:4px;
                            ">
                                ✓ RESUME CONNECTED
                            </div>
                        </div>
                    </div>
                </div>
                """
            )
        else:
            st.html(
                """
                <div style="
                    background:#FFFFFF;
                    border:1px solid #E2E4F0;
                    border-radius:22px;
                    padding:25px 28px;
                ">
                    <div style="
                        color:#20243A;
                        font-size:16px;
                        font-weight:800;
                        margin-bottom:6px;
                    ">
                        No resume connected
                    </div>

                    <div style="
                        color:#737D96;
                        font-size:13px;
                        line-height:1.5;
                    ">
                        Add your resume from Edit Profile.
                    </div>
                </div>
                """
            )

        st.write("")

        # ----------------------------------------------------
        # EDIT BUTTON
        # ----------------------------------------------------

        if st.button(
            "✏️ Edit Profile",
            type="primary",
            use_container_width=True
        ):
            st.session_state.profile_editing = True
            st.rerun()

        return

    # ========================================================
    # EDIT MODE
    # ========================================================

    st.subheader("✏️ Edit Profile")

    st.caption(
        "Update your information below and save your changes "
        "permanently."
    )

    with st.container(border=True):

        # ----------------------------------------------------
        # EDUCATION
        # ----------------------------------------------------

        st.markdown("### 🎓 Education")

        education = st.text_input(
            "Education",
            value=profile["education"],
            placeholder="BCA / B.Tech / MCA",
            key="profile_education"
        )

        # ----------------------------------------------------
        # TARGET JOB ROLE
        # ----------------------------------------------------

        st.markdown("### 🎯 Career")

        target_role = st.text_input(
            "Target Job Role",
            value=profile["job_role"],
            placeholder="AI/ML Engineer",
            key="profile_target_role"
        )

        # ----------------------------------------------------
        # EXPERIENCE
        # ----------------------------------------------------

        experience_options = [
            "Student / Fresher",
            "Entry Level",
            "1–2 Years",
            "3–5 Years",
            "5+ Years"
        ]

        current_experience = profile["experience"]

        if current_experience not in experience_options:
            current_experience = "Student / Fresher"

        experience = st.selectbox(
            "Experience Level",
            experience_options,
            index=experience_options.index(
                current_experience
            ),
            key="profile_experience"
        )

        # ----------------------------------------------------
        # TECHNICAL SKILLS
        # ----------------------------------------------------

        st.markdown("### 🧠 Skills")

        skills = st.text_area(
            "Technical Skills",
            value=profile["skills"],
            placeholder=(
                "Python, Machine Learning, SQL, NLP..."
            ),
            height=120,
            key="profile_skills"
        )

        # ----------------------------------------------------
        # CAREER GOAL
        # ----------------------------------------------------

        career_goal = st.text_area(
            "Career Goal",
            value=profile["career_goal"],
            placeholder=(
                "What role are you preparing for?"
            ),
            height=120,
            key="profile_career_goal"
        )

        st.write("")

        # ----------------------------------------------------
        # RESUME
        # ----------------------------------------------------

        st.markdown("### 📄 Resume")

        st.caption(
            "Upload or replace your resume. The original PDF is "
            "stored with your Mirai profile."
        )

        resume_col1, resume_col2 = st.columns(
            [1.25, 0.75]
        )

        with resume_col1:
            uploaded_resume = st.file_uploader(
                "Upload / Replace Resume",
                type=["pdf"],
                accept_multiple_files=False,
                help=(
                    "Upload your latest resume as a PDF. "
                    "The original PDF is stored with your account."
                ),
                key="profile_resume_uploader_edit",
            )

            if uploaded_resume is not None:
                if st.button(
                    "📤 Upload Resume",
                    use_container_width=True,
                    key="profile_save_resume_edit",
                ):
                    success, result = save_profile_resume(
                        user["id"],
                        uploaded_resume,
                    )

                    if success:
                        st.session_state.resume_upload_notice = (
                            f"Resume uploaded successfully: {result}"
                        )
                        st.rerun()
                    else:
                        st.error(result)

        with resume_col2:
            if resume:
                filename = html.escape(
                    resume["filename"] or "Resume.pdf"
                )

                st.html(
                    f"""
                    <div style="
                        background:#F0EDFF;
                        border:1px solid #DDD7FF;
                        border-radius:18px;
                        padding:18px;
                        min-height:112px;
                    ">
                        <div style="
                            color:#5F4BD6;
                            font-size:11px;
                            font-weight:800;
                            letter-spacing:0.8px;
                            margin-bottom:8px;
                        ">
                            ✓ CONNECTED
                        </div>

                        <div style="
                            color:#20243A;
                            font-size:14px;
                            font-weight:800;
                            line-height:1.4;
                            word-break:break-word;
                        ">
                            {filename}
                        </div>
                    </div>
                    """
                )

                if st.button(
                    "🗑️ Remove Resume",
                    use_container_width=True,
                    key="profile_delete_resume_edit",
                ):
                    if delete_user_resume(user["id"]):
                        st.session_state.resume_upload_notice = (
                            "Resume removed from your profile."
                        )
                        st.rerun()
                    else:
                        st.error(
                            "Could not remove your resume."
                        )
            else:
                st.html(
                    """
                    <div style="
                        background:#FBFAFF;
                        border:1px dashed #D8D4F2;
                        border-radius:18px;
                        padding:18px;
                        min-height:112px;
                        display:flex;
                        align-items:center;
                    ">
                        <div style="
                            color:#737D96;
                            font-size:13px;
                            line-height:1.5;
                        ">
                            No resume connected yet.
                            Upload one using the button beside this card.
                        </div>
                    </div>
                    """
                )

        st.write("")

        # ----------------------------------------------------
        # SAVE / CANCEL
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "💾 Save Changes",
                type="primary",
                use_container_width=True
            ):

                education = education.strip()
                target_role = target_role.strip()
                skills = skills.strip()
                career_goal = career_goal.strip()

                success = update_user_profile(
                    user_id=user["id"],
                    education=education,
                    target_job_role=target_role,
                    experience_level=experience,
                    technical_skills=skills,
                    career_goal=career_goal
                )

                if success:

                    # Update the logged-in user immediately.
                    user["education"] = education
                    user["target_job_role"] = target_role
                    user["experience_level"] = experience
                    user["technical_skills"] = skills
                    user["career_goal"] = career_goal

                    st.session_state.user = user

                    st.session_state.profile = {
                        "full_name": user.get(
                            "full_name",
                            ""
                        ),
                        "email": user.get(
                            "email",
                            ""
                        ),
                        "education": user.get(
                            "education",
                            ""
                        ),
                        "job_role": user.get(
                            "target_job_role",
                            ""
                        ),
                        "experience": user.get(
                            "experience_level",
                            ""
                        ),
                        "skills": user.get(
                            "technical_skills",
                            ""
                        ),
                        "career_goal": user.get(
                            "career_goal",
                            ""
                        )
                    }

                    st.session_state.profile_editing = False

                    st.success(
                        "✅ Profile updated successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Unable to save your profile. "
                        "Please try again."
                    )

        with col2:

            if st.button(
                "Cancel",
                use_container_width=True
            ):

                st.session_state.profile_editing = False
                st.rerun()


# ============================================================
# DIRECT STREAMLIT PAGE ENTRY
# ============================================================

if __name__ == "__main__":
    profile_page()