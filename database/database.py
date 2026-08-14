import sqlite3
import hashlib
import secrets
from pathlib import Path
from datetime import datetime


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "mirai_ai.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a SQLite database connection.
    """

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    # Enable foreign key support
    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# ============================================================
# PASSWORD SECURITY
# ============================================================

def hash_password(password, salt=None, iterations=600_000):
    """
    Securely hash a password using PBKDF2-HMAC-SHA256.

    New passwords use 600,000 iterations.
    Existing passwords are verified using their stored
    iteration count during the migration period.
    """

    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations
    )

    return (
        salt,
        password_hash.hex()
    )


def verify_password(
    password,
    salt,
    stored_hash,
    iterations=600_000
):
    """
    Verify a password against its stored hash.
    """

    _, password_hash = hash_password(
        password,
        salt,
        iterations
    )

    return secrets.compare_digest(
        password_hash,
        stored_hash
    )


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database():
    """
    Create all Mirai AI database tables.
    """

    connection = get_connection()

    cursor = connection.cursor()

    # ========================================================
    # USERS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            full_name TEXT NOT NULL,

            email TEXT NOT NULL UNIQUE,

            password_hash TEXT NOT NULL,

            password_salt TEXT NOT NULL,

            password_iterations INTEGER NOT NULL DEFAULT 600000,

            education TEXT,

            target_job_role TEXT,

            experience_level TEXT,

            technical_skills TEXT,

            career_goal TEXT,

            created_at TEXT NOT NULL,

            updated_at TEXT NOT NULL
        )
        """
    )

    # ========================================================
    # SECURITY MIGRATION
    # ========================================================

    try:
        cursor.execute(
            """
            ALTER TABLE users
            ADD COLUMN password_iterations
            INTEGER NOT NULL DEFAULT 100000
            """
        )
    except sqlite3.OperationalError as error:
        if "duplicate column name" not in str(error).lower():
            raise

    # ========================================================
    # LOGIN SECURITY
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS login_security (
            email TEXT PRIMARY KEY,
            failed_attempts INTEGER NOT NULL DEFAULT 0,
            locked_until TEXT,
            last_failed_at TEXT,
            updated_at TEXT NOT NULL
        )
        """
    )

    # ========================================================
    # RESUME DOCUMENTS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS resume_documents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            filename TEXT NOT NULL,

            pdf_data BLOB NOT NULL,

            uploaded_at TEXT NOT NULL,

            updated_at TEXT NOT NULL,

            FOREIGN KEY (
                user_id
            )
            REFERENCES users(id)
            ON DELETE CASCADE
        )
        """
    )

    # ========================================================
    # INTERVIEWS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS interviews (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            target_job_role TEXT NOT NULL,

            interview_type TEXT NOT NULL,

            difficulty TEXT NOT NULL,

            interview_mode TEXT NOT NULL,

            focus_area TEXT NOT NULL,

            total_questions INTEGER NOT NULL,

            completed_questions INTEGER DEFAULT 0,

            status TEXT DEFAULT 'created',

            overall_score REAL,

            technical_score REAL,

            communication_score REAL,

            problem_solving_score REAL,

            answer_structure_score REAL,

            readiness_score REAL,

            started_at TEXT,

            completed_at TEXT,

            created_at TEXT NOT NULL,

            FOREIGN KEY (
                user_id
            )
            REFERENCES users(id)
            ON DELETE CASCADE
        )
        """
    )

    # ========================================================
    # INTERVIEW QUESTIONS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS interview_questions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            interview_id INTEGER NOT NULL,

            question_number INTEGER NOT NULL,

            question_text TEXT NOT NULL,

            question_type TEXT,

            difficulty TEXT,

            topic TEXT,

            expected_concepts TEXT,

            generated_by TEXT DEFAULT 'mirai',

            created_at TEXT NOT NULL,

            FOREIGN KEY (
                interview_id
            )
            REFERENCES interviews(id)
            ON DELETE CASCADE
        )
        """
    )

    # ========================================================
    # ANSWERS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS answers (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            interview_id INTEGER NOT NULL,

            question_id INTEGER NOT NULL,

            user_answer TEXT NOT NULL,

            response_time_seconds INTEGER,

            created_at TEXT NOT NULL,

            FOREIGN KEY (
                interview_id
            )
            REFERENCES interviews(id)
            ON DELETE CASCADE,

            FOREIGN KEY (
                question_id
            )
            REFERENCES interview_questions(id)
            ON DELETE CASCADE
        )
        """
    )

    # ========================================================
    # EVALUATIONS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS evaluations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            answer_id INTEGER NOT NULL UNIQUE,

            overall_score REAL,

            technical_score REAL,

            communication_score REAL,

            problem_solving_score REAL,

            answer_structure_score REAL,

            relevance_score REAL,

            confidence_score REAL,

            strengths TEXT,

            weaknesses TEXT,

            feedback TEXT,

            recommended_action TEXT,

            created_at TEXT NOT NULL,

            FOREIGN KEY (
                answer_id
            )
            REFERENCES answers(id)
            ON DELETE CASCADE
        )
        """
    )

    # ========================================================
    # USER PROGRESS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_progress (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL UNIQUE,

            interviews_completed INTEGER DEFAULT 0,

            questions_answered INTEGER DEFAULT 0,

            average_score REAL DEFAULT 0,

            technical_average REAL DEFAULT 0,

            communication_average REAL DEFAULT 0,

            problem_solving_average REAL DEFAULT 0,

            answer_structure_average REAL DEFAULT 0,

            readiness_score REAL DEFAULT 0,

            updated_at TEXT NOT NULL,

            FOREIGN KEY (
                user_id
            )
            REFERENCES users(id)
            ON DELETE CASCADE
        )
        """
    )

    # ========================================================
    # PERFORMANCE TOPICS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS topic_performance (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            topic TEXT NOT NULL,

            attempts INTEGER DEFAULT 0,

            average_score REAL DEFAULT 0,

            last_score REAL DEFAULT 0,

            improvement_rate REAL DEFAULT 0,

            last_practiced_at TEXT,

            FOREIGN KEY (
                user_id
            )
            REFERENCES users(id)
            ON DELETE CASCADE,

            UNIQUE (
                user_id,
                topic
            )
        )
        """
    )

    # ========================================================
    # INDEXES
    # ========================================================

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_resumes_user
        ON resume_documents(user_id)
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_interviews_user
        ON interviews(user_id)
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_questions_interview
        ON interview_questions(interview_id)
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_answers_interview
        ON answers(interview_id)
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS
        idx_topic_user
        ON topic_performance(user_id)
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# CREATE USER
# ============================================================

def create_user(
    full_name,
    email,
    password,
    education="",
    target_job_role=""
):
    """
    Create a new user.

    Compatible with the current app.py:
        create_user(full_name, email, password)

    Returns:
        (True, message)
        or
        (False, message)
    """

    connection = get_connection()

    cursor = connection.cursor()

    email = email.strip().lower()

    try:

        # ----------------------------------------------------
        # Check existing user
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            return (
                False,
                "An account with this email already exists."
            )

        # ----------------------------------------------------
        # Password hashing
        # ----------------------------------------------------

        salt, password_hash = hash_password(
            password,
            iterations=600_000
        )

        now = datetime.now().isoformat()

        # ----------------------------------------------------
        # Insert user
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO users (

                full_name,
                email,
                password_hash,
                password_salt,
                password_iterations,
                education,
                target_job_role,
                experience_level,
                technical_skills,
                career_goal,
                created_at,
                updated_at

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                full_name.strip(),
                email,
                password_hash,
                salt,
                600_000,
                education.strip(),
                target_job_role.strip(),
                "",
                "",
                "",
                now,
                now
            )
        )

        user_id = cursor.lastrowid

        # ----------------------------------------------------
        # Create initial progress record
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO user_progress (

                user_id,
                updated_at

            )

            VALUES (?, ?)
            """,
            (
                user_id,
                now
            )
        )

        connection.commit()

        return (
            True,
            "Account created successfully."
        )

    except sqlite3.IntegrityError:

        connection.rollback()

        return (
            False,
            "An account with this email already exists."
        )

    except Exception as error:

        connection.rollback()

        return (
            False,
            str(error)
        )

    finally:

        connection.close()


# ============================================================
# LOGIN BRUTE-FORCE PROTECTION
# ============================================================

LOGIN_MAX_FAILED_ATTEMPTS = 5
LOGIN_LOCKOUT_MINUTES = 10


def _get_login_security(cursor, email):
    cursor.execute(
        """
        SELECT
            email,
            failed_attempts,
            locked_until,
            last_failed_at,
            updated_at
        FROM login_security
        WHERE email = ?
        """,
        (email,)
    )
    return cursor.fetchone()


def _is_login_locked(record):
    if record is None or not record["locked_until"]:
        return False

    try:
        locked_until = datetime.fromisoformat(
            record["locked_until"]
        )
        return datetime.now() < locked_until
    except (TypeError, ValueError):
        return False


def _record_failed_login(cursor, email):
    now = datetime.now()

    record = _get_login_security(cursor, email)

    if record is None:
        failed_attempts = 1
    else:
        # If a previous lock has expired, start a fresh failure window.
        previous_locked_until = record["locked_until"]

        if previous_locked_until:
            try:
                if datetime.now() >= datetime.fromisoformat(
                    previous_locked_until
                ):
                    failed_attempts = 1
                else:
                    failed_attempts = int(
                        record["failed_attempts"] or 0
                    ) + 1
            except (TypeError, ValueError):
                failed_attempts = 1
        else:
            failed_attempts = int(
                record["failed_attempts"] or 0
            ) + 1

    locked_until = None

    if failed_attempts >= LOGIN_MAX_FAILED_ATTEMPTS:
        locked_until = (
            now.timestamp()
        )

        from datetime import timedelta

        locked_until = (
            now + timedelta(minutes=LOGIN_LOCKOUT_MINUTES)
        ).isoformat()

    cursor.execute(
        """
        INSERT INTO login_security (
            email,
            failed_attempts,
            locked_until,
            last_failed_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(email) DO UPDATE SET
            failed_attempts = excluded.failed_attempts,
            locked_until = excluded.locked_until,
            last_failed_at = excluded.last_failed_at,
            updated_at = excluded.updated_at
        """,
        (
            email,
            failed_attempts,
            locked_until,
            now.isoformat(),
            now.isoformat()
        )
    )

    return failed_attempts, locked_until


def _clear_failed_logins(cursor, email):
    cursor.execute(
        """
        DELETE FROM login_security
        WHERE email = ?
        """,
        (email,)
    )


def get_login_security_status(email):
    """
    Return safe login-attempt information for the login UI.

    This intentionally exposes only:
        - attempts remaining
        - whether the account is temporarily locked
        - seconds remaining in the lockout

    It does not expose password data.
    """

    email = (email or "").strip().lower()

    if not email:
        return {
            "attempts_left": LOGIN_MAX_FAILED_ATTEMPTS,
            "locked": False,
            "seconds_remaining": 0
        }

    connection = get_connection()
    cursor = connection.cursor()

    try:
        record = _get_login_security(
            cursor,
            email
        )

        if record is None:
            return {
                "attempts_left": LOGIN_MAX_FAILED_ATTEMPTS,
                "locked": False,
                "seconds_remaining": 0
            }

        locked_until = record["locked_until"]

        if locked_until:
            try:
                remaining = int(
                    (
                        datetime.fromisoformat(locked_until)
                        - datetime.now()
                    ).total_seconds()
                )

                if remaining > 0:
                    return {
                        "attempts_left": 0,
                        "locked": True,
                        "seconds_remaining": remaining
                    }
            except (TypeError, ValueError):
                pass

        failed_attempts = int(
            record["failed_attempts"] or 0
        )

        return {
            "attempts_left": max(
                0,
                LOGIN_MAX_FAILED_ATTEMPTS - failed_attempts
            ),
            "locked": False,
            "seconds_remaining": 0
        }

    finally:
        connection.close()


# ============================================================
# AUTHENTICATE USER
# ============================================================

def authenticate_user(
    email,
    password
):
    """
    Authenticate an existing user with brute-force protection.

    Returns:
        User dictionary if successful.
        None if authentication fails.
    """

    connection = get_connection()
    cursor = connection.cursor()

    email = email.strip().lower()

    try:

        # ----------------------------------------------------
        # Check lockout state before verifying password
        # ----------------------------------------------------

        security_record = _get_login_security(
            cursor,
            email
        )

        if _is_login_locked(security_record):
            return None

        # ----------------------------------------------------
        # Find user
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

        # Do not reveal whether an email exists.
        if user is None:
            _record_failed_login(
                cursor,
                email
            )
            connection.commit()
            return None

        # ----------------------------------------------------
        # Verify password
        # ----------------------------------------------------

        stored_iterations = user["password_iterations"]

        valid_password = verify_password(
            password,
            user["password_salt"],
            user["password_hash"],
            stored_iterations
        )

        if not valid_password:
            _record_failed_login(
                cursor,
                email
            )
            connection.commit()
            return None

        # ----------------------------------------------------
        # Successful login
        # ----------------------------------------------------

        _clear_failed_logins(
            cursor,
            email
        )

        # ----------------------------------------------------
        # Upgrade legacy password hashes
        # ----------------------------------------------------

        if stored_iterations < 600_000:

            new_salt, new_hash = hash_password(
                password,
                iterations=600_000
            )

            cursor.execute(
                """
                UPDATE users
                SET
                    password_hash = ?,
                    password_salt = ?,
                    password_iterations = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    new_hash,
                    new_salt,
                    600_000,
                    datetime.now().isoformat(),
                    user["id"]
                )
            )

        connection.commit()

        # ----------------------------------------------------
        # Return safe user data only
        # ----------------------------------------------------

        return {
            "id": user["id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "education": user["education"],
            "target_job_role": user["target_job_role"],
            "experience_level": user["experience_level"],
            "technical_skills": user["technical_skills"],
            "career_goal": user["career_goal"],
            "created_at": user["created_at"],
            "updated_at": user["updated_at"]
        }

    except Exception:
        connection.rollback()
        return None

    finally:
        connection.close()


# ============================================================
# UPDATE USER PROFILE
# ============================================================

def update_user_profile(
    user_id,
    education=None,
    target_job_role=None,
    experience_level=None,
    technical_skills=None,
    career_goal=None
):
    """
    Update candidate profile information.
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        now = datetime.now().isoformat()

        cursor.execute(
            """
            UPDATE users

            SET

                education = ?,

                target_job_role = ?,

                experience_level = ?,

                technical_skills = ?,

                career_goal = ?,

                updated_at = ?

            WHERE id = ?
            """,
            (
                education,
                target_job_role,
                experience_level,
                technical_skills,
                career_goal,
                now,
                user_id
            )
        )

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        return False

    finally:

        connection.close()


# ============================================================
# RESUME DOCUMENT STORAGE
# ============================================================

def save_user_resume(
    user_id,
    filename,
    pdf_data
):
    """
    Store or replace the user's current resume PDF.

    The original PDF is preserved as a BLOB in the database so it
    remains the source document for future resume-aware features.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        now = datetime.now().isoformat()

        # Keep one active resume per user for the first version.
        cursor.execute(
            """
            DELETE FROM resume_documents
            WHERE user_id = ?
            """,
            (user_id,)
        )

        cursor.execute(
            """
            INSERT INTO resume_documents (
                user_id,
                filename,
                pdf_data,
                uploaded_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                filename,
                sqlite3.Binary(pdf_data),
                now,
                now
            )
        )

        connection.commit()

        return cursor.lastrowid

    except Exception:
        connection.rollback()
        return None

    finally:
        connection.close()


def get_user_resume(
    user_id
):
    """
    Return the user's current stored resume.

    Returns:
        {
            "id": ...,
            "user_id": ...,
            "filename": ...,
            "pdf_data": bytes,
            "uploaded_at": ...,
            "updated_at": ...
        }

        or None if no resume exists.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                id,
                user_id,
                filename,
                pdf_data,
                uploaded_at,
                updated_at
            FROM resume_documents
            WHERE user_id = ?
            ORDER BY updated_at DESC
            LIMIT 1
            """,
            (user_id,)
        )

        resume = cursor.fetchone()

        if resume is None:
            return None

        return dict(resume)

    finally:
        connection.close()


def delete_user_resume(
    user_id
):
    """
    Delete the user's stored resume.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM resume_documents
            WHERE user_id = ?
            """,
            (user_id,)
        )

        connection.commit()

        return cursor.rowcount > 0

    except Exception:
        connection.rollback()
        return False

    finally:
        connection.close()


# ============================================================
# CREATE INTERVIEW
# ============================================================

def create_interview(
    user_id,
    target_job_role,
    interview_type,
    difficulty,
    interview_mode,
    focus_area,
    total_questions
):
    """
    Create a new interview session.

    Returns:
        interview_id
    """

    connection = get_connection()

    cursor = connection.cursor()

    now = datetime.now().isoformat()

    try:

        cursor.execute(
            """
            INSERT INTO interviews (

                user_id,
                target_job_role,
                interview_type,
                difficulty,
                interview_mode,
                focus_area,
                total_questions,
                completed_questions,
                status,
                started_at,
                created_at

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                target_job_role,
                interview_type,
                difficulty,
                interview_mode,
                focus_area,
                total_questions,
                0,
                "in_progress",
                now,
                now
            )
        )

        interview_id = cursor.lastrowid

        connection.commit()

        return interview_id

    except Exception:

        connection.rollback()

        return None

    finally:

        connection.close()


# ============================================================
# SAVE INTERVIEW QUESTION
# ============================================================

def save_question(
    interview_id,
    question_number,
    question_text,
    question_type=None,
    difficulty=None,
    topic=None,
    expected_concepts=None
):
    """
    Save an AI-generated interview question.
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO interview_questions (

                interview_id,
                question_number,
                question_text,
                question_type,
                difficulty,
                topic,
                expected_concepts,
                generated_by,
                created_at

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                interview_id,
                question_number,
                question_text,
                question_type,
                difficulty,
                topic,
                expected_concepts,
                "mirai",
                datetime.now().isoformat()
            )
        )

        question_id = cursor.lastrowid

        connection.commit()

        return question_id

    except Exception:

        connection.rollback()

        return None

    finally:

        connection.close()


# ============================================================
# SAVE ANSWER
# ============================================================

def save_answer(
    interview_id,
    question_id,
    user_answer,
    response_time_seconds=None
):
    """
    Save a candidate's answer.
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO answers (

                interview_id,
                question_id,
                user_answer,
                response_time_seconds,
                created_at

            )

            VALUES (?, ?, ?, ?, ?)
            """,
            (
                interview_id,
                question_id,
                user_answer,
                response_time_seconds,
                datetime.now().isoformat()
            )
        )

        answer_id = cursor.lastrowid

        # Update completed question count

        cursor.execute(
            """
            UPDATE interviews

            SET completed_questions =
                completed_questions + 1

            WHERE id = ?
            """,
            (interview_id,)
        )

        connection.commit()

        return answer_id

    except Exception:

        connection.rollback()

        return None

    finally:

        connection.close()


# ============================================================
# SAVE EVALUATION
# ============================================================

def save_evaluation(
    answer_id,
    overall_score=None,
    technical_score=None,
    communication_score=None,
    problem_solving_score=None,
    answer_structure_score=None,
    relevance_score=None,
    confidence_score=None,
    strengths=None,
    weaknesses=None,
    feedback=None,
    recommended_action=None
):
    """
    Save AI evaluation for an answer.
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT OR REPLACE INTO evaluations (

                answer_id,
                overall_score,
                technical_score,
                communication_score,
                problem_solving_score,
                answer_structure_score,
                relevance_score,
                confidence_score,
                strengths,
                weaknesses,
                feedback,
                recommended_action,
                created_at

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                answer_id,
                overall_score,
                technical_score,
                communication_score,
                problem_solving_score,
                answer_structure_score,
                relevance_score,
                confidence_score,
                strengths,
                weaknesses,
                feedback,
                recommended_action,
                datetime.now().isoformat()
            )
        )

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        return False

    finally:

        connection.close()


# ============================================================
# COMPLETE INTERVIEW
# ============================================================

def complete_interview(
    interview_id,
    overall_score=None,
    technical_score=None,
    communication_score=None,
    problem_solving_score=None,
    answer_structure_score=None,
    readiness_score=None
):
    """
    Mark an interview as completed.
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        now = datetime.now().isoformat()

        cursor.execute(
            """
            UPDATE interviews

            SET

                status = 'completed',

                overall_score = ?,

                technical_score = ?,

                communication_score = ?,

                problem_solving_score = ?,

                answer_structure_score = ?,

                readiness_score = ?,

                completed_at = ?

            WHERE id = ?
            """,
            (
                overall_score,
                technical_score,
                communication_score,
                problem_solving_score,
                answer_structure_score,
                readiness_score,
                now,
                interview_id
            )
        )

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        return False

    finally:

        connection.close()


# ============================================================
# GET USER PROGRESS
# ============================================================

def get_user_progress(user_id):
    """
    Get stored progress for a user.
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *

            FROM user_progress

            WHERE user_id = ?
            """,
            (user_id,)
        )

        progress = cursor.fetchone()

        if progress is None:

            return None

        return dict(progress)

    finally:

        connection.close()


# ============================================================
# GET INTERVIEW HISTORY
# ============================================================

def get_interview_history(
    user_id
):
    """
    Return completed and previous interviews.
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *

            FROM interviews

            WHERE user_id = ?

            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        interviews = cursor.fetchall()

        return [
            dict(interview)
            for interview in interviews
        ]

    finally:

        connection.close()


# ============================================================
# GET INTERVIEW QUESTIONS
# ============================================================

def get_interview_questions(
    interview_id
):
    """
    Get all questions for an interview.
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *

            FROM interview_questions

            WHERE interview_id = ?

            ORDER BY question_number ASC
            """,
            (interview_id,)
        )

        questions = cursor.fetchall()

        return [
            dict(question)
            for question in questions
        ]

    finally:

        connection.close()


# ============================================================
# GET INTERVIEW ANSWERS
# ============================================================

def get_interview_answers(
    interview_id
):
    """
    Get all answers for an interview.
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT

                answers.*,

                interview_questions.question_text,

                evaluations.overall_score,

                evaluations.technical_score,

                evaluations.communication_score,

                evaluations.problem_solving_score,

                evaluations.answer_structure_score,

                evaluations.strengths,

                evaluations.weaknesses,

                evaluations.feedback,

                evaluations.recommended_action

            FROM answers

            JOIN interview_questions

                ON answers.question_id =
                   interview_questions.id

            LEFT JOIN evaluations

                ON answers.id =
                   evaluations.answer_id

            WHERE answers.interview_id = ?

            ORDER BY
                interview_questions.question_number ASC
            """,
            (interview_id,)
        )

        answers = cursor.fetchall()

        return [
            dict(answer)
            for answer in answers
        ]

    finally:

        connection.close()


# ============================================================
# UPDATE TOPIC PERFORMANCE
# ============================================================

def update_topic_performance(
    user_id,
    topic,
    score
):
    """
    Update performance for a particular topic.

    This will become important for adaptive interviews.
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *

            FROM topic_performance

            WHERE user_id = ?

            AND topic = ?
            """,
            (
                user_id,
                topic
            )
        )

        existing = cursor.fetchone()

        now = datetime.now().isoformat()

        if existing is None:

            cursor.execute(
                """
                INSERT INTO topic_performance (

                    user_id,
                    topic,
                    attempts,
                    average_score,
                    last_score,
                    improvement_rate,
                    last_practiced_at

                )

                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    topic,
                    1,
                    score,
                    score,
                    0,
                    now
                )
            )

        else:

            old_attempts = existing["attempts"]

            old_average = existing["average_score"]

            new_attempts = old_attempts + 1

            new_average = (
                (
                    old_average * old_attempts
                )
                + score
            ) / new_attempts

            improvement = (
                score
                - existing["last_score"]
            )

            cursor.execute(
                """
                UPDATE topic_performance

                SET

                    attempts = ?,

                    average_score = ?,

                    last_score = ?,

                    improvement_rate = ?,

                    last_practiced_at = ?

                WHERE user_id = ?

                AND topic = ?
                """,
                (
                    new_attempts,
                    new_average,
                    score,
                    improvement,
                    now,
                    user_id,
                    topic
                )
            )

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        return False

    finally:

        connection.close()


# ============================================================
# GET WEAK TOPICS
# ============================================================

def get_weak_topics(
    user_id,
    limit=5
):
    """
    Return the candidate's weakest topics.

    These will later be used by the adaptive AI engine.
    """

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT *

            FROM topic_performance

            WHERE user_id = ?

            ORDER BY average_score ASC

            LIMIT ?
            """,
            (
                user_id,
                limit
            )
        )

        topics = cursor.fetchall()

        return [
            dict(topic)
            for topic in topics
        ]

    finally:

        connection.close()

# ============================================================
# GET TOPIC PERFORMANCE
# ============================================================

def get_topic_performance(
    user_id
):
    """
    Return all tracked topic performance for a candidate.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT
                topic,
                attempts,
                average_score,
                last_score,
                improvement_rate,
                last_practiced_at
            FROM topic_performance
            WHERE user_id = ?
            ORDER BY average_score ASC, attempts DESC
            """,
            (user_id,)
        )

        topics = cursor.fetchall()

        return [
            dict(topic)
            for topic in topics
        ]

    finally:
        connection.close()