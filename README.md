# AI Interview Preparation Platform

An AI-powered interview preparation platform developed using Python. The application helps students and job seekers prepare for technical, HR, and behavioral interviews through AI-generated questions, mock interview sessions, personalized feedback, and performance tracking.

## 🚀 Features

- AI-generated interview questions
- Technical interview preparation
- HR interview preparation
- Behavioral interview practice
- Mock interview sessions
- AI-based answer evaluation
- Personalized feedback
- Performance tracking
- Interview history
- User profile management

## 🛠️ Technologies Used

- Python
- Artificial Intelligence / Machine Learning
- OpenAI API / Gemini API
- Streamlit
- SQLite / MySQL
- VS Code
- Git & GitHub

## 🎯 Project Objective

The main objective of this project is to provide an intelligent and interactive platform that helps users improve their interview performance, technical knowledge, communication skills, and confidence through personalized AI-powered practice.

## 🏗️ Project Structure

│
├── app.py                         # Main Streamlit application
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── .gitignore                     # Files ignored by Git
├── .env.example                   # Example environment variables
│
├── config/
│   └── config.py                  # Application configuration
│
├── src/
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── ai_service.py          # AI API integration
│   │   └── prompts.py             # AI interview prompts
│   │
│   ├── interview/
│   │   ├── __init__.py
│   │   ├── question_generator.py  # Generate interview questions
│   │   ├── interview_engine.py    # Interview logic
│   │   └── evaluator.py           # Evaluate user answers
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py             # Database connection
│   │   └── models.py               # Database models
│   │
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py               # Common helper functions
│       └── validators.py            # Input validation
│
├── pages/
│   ├── home.py                     # Home/Dashboard
│   ├── interview.py                # Interview screen
│   ├── feedback.py                 # Feedback screen
│   ├── history.py                  # Interview history
│   └── profile.py                  # User profile
│
├── data/
│   └── .gitkeep                    # Local application data
│
├── assets/
│   ├── images/
│   └── icons/
│
└── tests/
    ├── __init__.py
    ├── test_ai.py
    ├── test_interview.py
    └── test_database.py
