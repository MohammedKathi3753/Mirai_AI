import streamlit as st

from database.database import update_user_profile


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

    if "profile_editing" not in st.session_state:
        st.session_state.profile_editing = False

    st.title("👤 My Profile")

    st.write(
        "Keep your candidate information updated so Mirai can "
        "personalize your interview preparation."
    )

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