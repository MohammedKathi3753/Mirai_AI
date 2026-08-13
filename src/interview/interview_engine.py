# ============================================================
# MIRAI AI - INTERVIEW ENGINE
# ============================================================

import os
import random
import re
from typing import Any, Dict, List, Optional


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_INTERVIEW_TYPE = "Technical"
DEFAULT_DIFFICULTY = "Adaptive"
DEFAULT_ROLE = "General Candidate"

DIFFICULTY_ORDER = [
    "Easy",
    "Medium",
    "Hard",
]


# ============================================================
# ROLE CATEGORIES
# ============================================================

ROLE_CATEGORIES = {
    "AI/ML": [
        "ai",
        "ml",
        "machine learning",
        "artificial intelligence",
        "data scientist",
        "data science",
        "deep learning",
        "nlp",
        "computer vision",
        "machine learning engineer",
        "ai engineer",
        "ml engineer",
    ],

    "Software/IT": [
        "software",
        "software engineer",
        "software developer",
        "developer",
        "web developer",
        "backend",
        "frontend",
        "full stack",
        "full-stack",
        "application developer",
        "programmer",
        "it",
        "information technology",
        "devops",
        "cloud engineer",
        "cyber security",
        "cybersecurity",
        "network engineer",
    ],

    "Accounting/Finance": [
        "accountant",
        "accounting",
        "finance",
        "financial analyst",
        "financial manager",
        "auditor",
        "audit",
        "bookkeeper",
        "tax",
        "taxation",
        "banking",
        "investment",
        "finance manager",
    ],

    "Sales": [
        "sales",
        "sales executive",
        "sales manager",
        "business development",
        "business development executive",
        "business development manager",
        "bdm",
        "bde",
        "account executive",
        "relationship manager",
    ],

    "Marketing": [
        "marketing",
        "marketing manager",
        "digital marketing",
        "seo",
        "sem",
        "social media",
        "brand manager",
        "content marketing",
        "growth marketing",
        "product marketing",
    ],

    "HR": [
        "hr",
        "human resources",
        "human resource",
        "hr executive",
        "hr manager",
        "recruiter",
        "recruitment",
        "talent acquisition",
        "people operations",
        "people ops",
    ],

    "Management": [
        "manager",
        "management",
        "project manager",
        "product manager",
        "operations manager",
        "business manager",
        "program manager",
        "team lead",
        "team leader",
        "operations",
        "consultant",
        "management trainee",
    ],

    "General": [],
}


# ============================================================
# ROLE-SPECIFIC DOMAINS
# ============================================================

ROLE_DOMAINS = {
    "AI/ML": [
        "Machine Learning",
        "Python",
        "Statistics",
        "Data Science",
        "Deep Learning",
        "Model Evaluation",
        "Feature Engineering",
        "AI Systems",
        "Natural Language Processing",
        "Computer Vision",
    ],

    "Software/IT": [
        "Programming",
        "Data Structures",
        "Algorithms",
        "Databases",
        "APIs",
        "Software Engineering",
        "System Design",
        "Testing",
        "Cloud",
        "DevOps",
        "Cybersecurity",
    ],

    "Accounting/Finance": [
        "Accounting Fundamentals",
        "Financial Statements",
        "Journal Entries",
        "Balance Sheet",
        "Income Statement",
        "Cash Flow",
        "Financial Analysis",
        "Auditing",
        "Taxation",
        "Budgeting",
        "Financial Reporting",
    ],

    "Sales": [
        "Prospecting",
        "Lead Generation",
        "Sales Funnel",
        "Negotiation",
        "Customer Relationship",
        "Objection Handling",
        "Closing",
        "Sales Strategy",
        "CRM",
        "Sales Forecasting",
    ],

    "Marketing": [
        "Market Research",
        "Customer Segmentation",
        "Branding",
        "Digital Marketing",
        "SEO",
        "Content Marketing",
        "Campaign Management",
        "Marketing Analytics",
        "Customer Acquisition",
        "Growth Strategy",
    ],

    "HR": [
        "Recruitment",
        "Talent Acquisition",
        "Employee Relations",
        "Performance Management",
        "Conflict Resolution",
        "Onboarding",
        "HR Policies",
        "Employee Engagement",
        "Training and Development",
        "Workplace Culture",
    ],

    "Management": [
        "Leadership",
        "Project Management",
        "Risk Management",
        "Stakeholder Management",
        "Team Management",
        "Decision Making",
        "Planning",
        "Budget Management",
        "Agile",
        "Operations",
    ],

    "General": [
        "Communication",
        "Problem Solving",
        "Decision Making",
        "Teamwork",
        "Leadership",
        "Professional Skills",
    ],
}


# ============================================================
# FALLBACK QUESTION BANK
# ============================================================
#
# These questions are NOT intended to replace AI.
# They are a safe fallback if an AI API is unavailable.
#
# The real AI generator is attempted first.
# ============================================================

ROLE_QUESTION_BANK = {

    "AI/ML": {
        "Easy": [
            {
                "question": "What is the difference between supervised and unsupervised learning?",
                "topic": "Machine Learning",
                "keywords": [
                    "supervised",
                    "unsupervised",
                    "labeled",
                    "unlabeled",
                ],
            },
            {
                "question": "What is overfitting in machine learning and how can you reduce it?",
                "topic": "Machine Learning",
                "keywords": [
                    "overfitting",
                    "generalization",
                    "regularization",
                ],
            },
            {
                "question": "What is the purpose of splitting a dataset into training and testing sets?",
                "topic": "Machine Learning",
                "keywords": [
                    "training",
                    "testing",
                    "generalization",
                ],
            },
        ],

        "Medium": [
            {
                "question": "How would you decide which machine learning algorithm to use for a classification problem?",
                "topic": "Model Selection",
                "keywords": [
                    "classification",
                    "features",
                    "dataset",
                    "evaluation",
                    "algorithm",
                ],
            },
            {
                "question": "How would you handle missing values in a machine learning dataset?",
                "topic": "Data Preprocessing",
                "keywords": [
                    "missing",
                    "imputation",
                    "mean",
                    "median",
                    "preprocessing",
                ],
            },
            {
                "question": "What is cross-validation and why is it useful when building machine learning models?",
                "topic": "Model Evaluation",
                "keywords": [
                    "cross-validation",
                    "validation",
                    "training",
                    "evaluation",
                ],
            },
        ],

        "Hard": [
            {
                "question": "A machine learning model performs very well on training data but poorly in production. How would you investigate the problem?",
                "topic": "Machine Learning",
                "keywords": [
                    "overfitting",
                    "distribution",
                    "data",
                    "monitoring",
                    "validation",
                ],
            },
            {
                "question": "How would you design a machine learning system that needs to serve predictions to thousands of users with low latency?",
                "topic": "AI Systems",
                "keywords": [
                    "latency",
                    "scaling",
                    "deployment",
                    "caching",
                    "monitoring",
                ],
            },
            {
                "question": "What techniques would you use to detect and prevent data leakage in a machine learning pipeline?",
                "topic": "Machine Learning",
                "keywords": [
                    "data leakage",
                    "training",
                    "validation",
                    "features",
                ],
            },
        ],
    },

    "Software/IT": {
        "Easy": [
            {
                "question": "What is the difference between a list and a tuple in Python?",
                "topic": "Programming",
                "keywords": [
                    "list",
                    "tuple",
                    "mutable",
                    "immutable",
                ],
            },
            {
                "question": "What is a database and why is it used in software applications?",
                "topic": "Databases",
                "keywords": [
                    "database",
                    "data",
                    "storage",
                ],
            },
            {
                "question": "What is an API?",
                "topic": "APIs",
                "keywords": [
                    "api",
                    "application",
                    "communication",
                ],
            },
        ],

        "Medium": [
            {
                "question": "How would you optimize a slow database query?",
                "topic": "Databases",
                "keywords": [
                    "index",
                    "query",
                    "execution",
                    "database",
                ],
            },
            {
                "question": "Explain the difference between authentication and authorization.",
                "topic": "Security",
                "keywords": [
                    "authentication",
                    "authorization",
                    "identity",
                    "permission",
                ],
            },
            {
                "question": "How would you design an API for a web application?",
                "topic": "APIs",
                "keywords": [
                    "endpoint",
                    "request",
                    "response",
                    "authentication",
                ],
            },
        ],

        "Hard": [
            {
                "question": "How would you design a highly scalable backend system that must handle a large number of concurrent users?",
                "topic": "System Design",
                "keywords": [
                    "scaling",
                    "load balancing",
                    "database",
                    "caching",
                    "availability",
                ],
            },
            {
                "question": "A production application suddenly becomes extremely slow. Explain your debugging approach.",
                "topic": "Software Engineering",
                "keywords": [
                    "monitoring",
                    "logs",
                    "performance",
                    "database",
                    "profiling",
                ],
            },
            {
                "question": "How would you design a fault-tolerant service for a critical application?",
                "topic": "System Design",
                "keywords": [
                    "fault tolerance",
                    "redundancy",
                    "availability",
                    "failure",
                ],
            },
        ],
    },

    "Accounting/Finance": {
        "Easy": [
            {
                "question": "What is the difference between a balance sheet and an income statement?",
                "topic": "Financial Statements",
                "keywords": [
                    "balance sheet",
                    "income statement",
                    "assets",
                    "liabilities",
                    "revenue",
                ],
            },
            {
                "question": "What is a journal entry in accounting?",
                "topic": "Accounting Fundamentals",
                "keywords": [
                    "journal",
                    "debit",
                    "credit",
                    "transaction",
                ],
            },
            {
                "question": "What is the purpose of a cash flow statement?",
                "topic": "Cash Flow",
                "keywords": [
                    "cash flow",
                    "cash",
                    "operating",
                    "investing",
                    "financing",
                ],
            },
        ],

        "Medium": [
            {
                "question": "How would you analyze a company's financial statements to evaluate its financial health?",
                "topic": "Financial Analysis",
                "keywords": [
                    "ratio",
                    "revenue",
                    "profit",
                    "cash flow",
                    "financial statements",
                ],
            },
            {
                "question": "How would you identify an accounting error during a financial reconciliation?",
                "topic": "Accounting",
                "keywords": [
                    "reconciliation",
                    "transaction",
                    "ledger",
                    "error",
                ],
            },
            {
                "question": "What financial ratios would you use to evaluate a company's liquidity and profitability?",
                "topic": "Financial Analysis",
                "keywords": [
                    "liquidity",
                    "profitability",
                    "ratio",
                    "current ratio",
                    "margin",
                ],
            },
        ],

        "Hard": [
            {
                "question": "A company's revenue is increasing but its cash position is declining. How would you investigate the situation?",
                "topic": "Financial Analysis",
                "keywords": [
                    "cash flow",
                    "receivables",
                    "working capital",
                    "revenue",
                    "cash",
                ],
            },
            {
                "question": "How would you design controls to reduce the risk of material errors in a company's financial reporting process?",
                "topic": "Financial Reporting",
                "keywords": [
                    "internal controls",
                    "audit",
                    "financial reporting",
                    "risk",
                ],
            },
            {
                "question": "How would you evaluate whether a major business investment is financially justified?",
                "topic": "Financial Analysis",
                "keywords": [
                    "investment",
                    "cash flow",
                    "ROI",
                    "NPV",
                    "risk",
                ],
            },
        ],
    },

    "Sales": {
        "Easy": [
            {
                "question": "What are the main stages of a typical sales process?",
                "topic": "Sales Process",
                "keywords": [
                    "prospecting",
                    "qualification",
                    "presentation",
                    "negotiation",
                    "closing",
                ],
            },
            {
                "question": "What is lead generation and why is it important?",
                "topic": "Lead Generation",
                "keywords": [
                    "lead",
                    "prospect",
                    "customer",
                    "sales",
                ],
            },
            {
                "question": "How would you build a good relationship with a new customer?",
                "topic": "Customer Relationship",
                "keywords": [
                    "customer",
                    "trust",
                    "communication",
                    "relationship",
                ],
            },
        ],

        "Medium": [
            {
                "question": "A potential customer says your product is too expensive. How would you handle the objection?",
                "topic": "Objection Handling",
                "keywords": [
                    "objection",
                    "value",
                    "customer",
                    "price",
                    "benefit",
                ],
            },
            {
                "question": "How would you prioritize leads when you have many prospects but limited time?",
                "topic": "Sales Strategy",
                "keywords": [
                    "lead",
                    "priority",
                    "qualification",
                    "conversion",
                ],
            },
            {
                "question": "How would you improve a sales pipeline where many leads are failing to convert?",
                "topic": "Sales Funnel",
                "keywords": [
                    "pipeline",
                    "conversion",
                    "lead",
                    "funnel",
                    "analysis",
                ],
            },
        ],

        "Hard": [
            {
                "question": "Your team's sales conversion rate has fallen significantly for three consecutive months. How would you diagnose and solve the problem?",
                "topic": "Sales Strategy",
                "keywords": [
                    "conversion",
                    "pipeline",
                    "analysis",
                    "customer",
                    "strategy",
                ],
            },
            {
                "question": "A high-value customer is considering a competitor because of pricing. How would you approach the negotiation?",
                "topic": "Negotiation",
                "keywords": [
                    "negotiation",
                    "value",
                    "pricing",
                    "customer",
                    "retention",
                ],
            },
            {
                "question": "How would you build a sales forecasting system for a growing sales organization?",
                "topic": "Sales Forecasting",
                "keywords": [
                    "forecast",
                    "pipeline",
                    "historical",
                    "conversion",
                    "sales",
                ],
            },
        ],
    },

    "Marketing": {
        "Easy": [
            {
                "question": "What is market segmentation and why is it useful?",
                "topic": "Market Research",
                "keywords": [
                    "segmentation",
                    "customers",
                    "market",
                ],
            },
            {
                "question": "What is the difference between organic and paid digital marketing?",
                "topic": "Digital Marketing",
                "keywords": [
                    "organic",
                    "paid",
                    "digital",
                    "marketing",
                ],
            },
            {
                "question": "What is a target audience?",
                "topic": "Marketing Fundamentals",
                "keywords": [
                    "target",
                    "audience",
                    "customer",
                ],
            },
        ],

        "Medium": [
            {
                "question": "How would you measure whether a digital marketing campaign was successful?",
                "topic": "Marketing Analytics",
                "keywords": [
                    "campaign",
                    "conversion",
                    "ROI",
                    "CTR",
                    "analytics",
                ],
            },
            {
                "question": "How would you identify the right customer segment for a new product?",
                "topic": "Customer Segmentation",
                "keywords": [
                    "segment",
                    "customer",
                    "market",
                    "research",
                ],
            },
            {
                "question": "How would you improve a marketing campaign that has high traffic but low conversions?",
                "topic": "Campaign Management",
                "keywords": [
                    "conversion",
                    "traffic",
                    "campaign",
                    "landing page",
                    "customer",
                ],
            },
        ],

        "Hard": [
            {
                "question": "A company's customer acquisition cost has increased sharply while conversions have fallen. How would you investigate and respond?",
                "topic": "Growth Strategy",
                "keywords": [
                    "CAC",
                    "conversion",
                    "acquisition",
                    "campaign",
                    "ROI",
                ],
            },
            {
                "question": "How would you design a multi-channel marketing strategy for launching a new product in a competitive market?",
                "topic": "Marketing Strategy",
                "keywords": [
                    "channel",
                    "customer",
                    "positioning",
                    "campaign",
                    "market",
                ],
            },
            {
                "question": "How would you determine whether a declining brand performance is caused by market changes or internal marketing decisions?",
                "topic": "Marketing Analytics",
                "keywords": [
                    "brand",
                    "market",
                    "analytics",
                    "competitor",
                    "data",
                ],
            },
        ],
    },

    "HR": {
        "Easy": [
            {
                "question": "What are the main stages of the recruitment process?",
                "topic": "Recruitment",
                "keywords": [
                    "recruitment",
                    "screening",
                    "interview",
                    "selection",
                ],
            },
            {
                "question": "Why is employee onboarding important?",
                "topic": "Onboarding",
                "keywords": [
                    "onboarding",
                    "employee",
                    "training",
                    "culture",
                ],
            },
            {
                "question": "What is employee engagement?",
                "topic": "Employee Engagement",
                "keywords": [
                    "engagement",
                    "employee",
                    "motivation",
                ],
            },
        ],

        "Medium": [
            {
                "question": "How would you handle a conflict between two employees?",
                "topic": "Conflict Resolution",
                "keywords": [
                    "conflict",
                    "communication",
                    "employees",
                    "resolution",
                ],
            },
            {
                "question": "How would you improve the quality of candidates entering a recruitment pipeline?",
                "topic": "Talent Acquisition",
                "keywords": [
                    "recruitment",
                    "candidate",
                    "screening",
                    "talent",
                ],
            },
            {
                "question": "How would you design a fair employee performance review process?",
                "topic": "Performance Management",
                "keywords": [
                    "performance",
                    "review",
                    "employee",
                    "goals",
                    "feedback",
                ],
            },
        ],

        "Hard": [
            {
                "question": "Employee turnover has increased significantly in one department. How would you investigate the causes and recommend solutions?",
                "topic": "Employee Retention",
                "keywords": [
                    "turnover",
                    "retention",
                    "employee",
                    "engagement",
                    "analysis",
                ],
            },
            {
                "question": "How would you design an HR strategy for a company that is rapidly scaling from 100 to 500 employees?",
                "topic": "HR Strategy",
                "keywords": [
                    "scaling",
                    "recruitment",
                    "culture",
                    "process",
                    "workforce",
                ],
            },
            {
                "question": "How would you handle a sensitive employee complaint involving a senior manager?",
                "topic": "Employee Relations",
                "keywords": [
                    "complaint",
                    "investigation",
                    "confidential",
                    "policy",
                    "employee",
                ],
            },
        ],
    },

    "Management": {
        "Easy": [
            {
                "question": "What are the key responsibilities of a manager?",
                "topic": "Management",
                "keywords": [
                    "planning",
                    "team",
                    "decision",
                    "leadership",
                ],
            },
            {
                "question": "What is the importance of setting clear goals for a team?",
                "topic": "Leadership",
                "keywords": [
                    "goals",
                    "team",
                    "performance",
                    "planning",
                ],
            },
            {
                "question": "What is project management?",
                "topic": "Project Management",
                "keywords": [
                    "project",
                    "planning",
                    "resources",
                    "deadline",
                ],
            },
        ],

        "Medium": [
            {
                "question": "A project is falling behind schedule. How would you identify the cause and bring it back on track?",
                "topic": "Project Management",
                "keywords": [
                    "schedule",
                    "planning",
                    "resources",
                    "risk",
                    "deadline",
                ],
            },
            {
                "question": "How would you manage a team member who consistently misses deadlines?",
                "topic": "Team Management",
                "keywords": [
                    "performance",
                    "communication",
                    "deadline",
                    "feedback",
                ],
            },
            {
                "question": "How would you prioritize competing tasks when multiple stakeholders consider their work urgent?",
                "topic": "Decision Making",
                "keywords": [
                    "priority",
                    "stakeholder",
                    "impact",
                    "deadline",
                ],
            },
        ],

        "Hard": [
            {
                "question": "A critical project has limited budget, an aggressive deadline, and conflicting stakeholder requirements. How would you manage the situation?",
                "topic": "Project Management",
                "keywords": [
                    "budget",
                    "deadline",
                    "stakeholder",
                    "priority",
                    "risk",
                ],
            },
            {
                "question": "Your team is technically strong but productivity and morale are declining. How would you diagnose and address the situation?",
                "topic": "Leadership",
                "keywords": [
                    "morale",
                    "productivity",
                    "leadership",
                    "team",
                    "communication",
                ],
            },
            {
                "question": "How would you make a high-impact business decision when the available data is incomplete?",
                "topic": "Decision Making",
                "keywords": [
                    "decision",
                    "risk",
                    "data",
                    "uncertainty",
                    "impact",
                ],
            },
        ],
    },

    "General": {
        "Easy": [
            {
                "question": "Tell me about yourself and your professional background.",
                "topic": "Communication",
                "keywords": [
                    "experience",
                    "skills",
                    "education",
                    "background",
                ],
            },
            {
                "question": "What are your main strengths?",
                "topic": "Professional Skills",
                "keywords": [
                    "strength",
                    "skill",
                    "experience",
                ],
            },
            {
                "question": "Why are you interested in this role?",
                "topic": "Motivation",
                "keywords": [
                    "role",
                    "interest",
                    "career",
                    "motivation",
                ],
            },
        ],

        "Medium": [
            {
                "question": "Tell me about a difficult problem you faced and how you solved it.",
                "topic": "Problem Solving",
                "keywords": [
                    "problem",
                    "solution",
                    "approach",
                    "result",
                ],
            },
            {
                "question": "Describe a situation where you had to work with someone who disagreed with you.",
                "topic": "Communication",
                "keywords": [
                    "communication",
                    "conflict",
                    "team",
                    "solution",
                ],
            },
            {
                "question": "Tell me about a time when you had to learn something quickly.",
                "topic": "Adaptability",
                "keywords": [
                    "learn",
                    "adapt",
                    "challenge",
                    "result",
                ],
            },
        ],

        "Hard": [
            {
                "question": "Describe a situation where you made an important decision with incomplete information. What did you consider?",
                "topic": "Decision Making",
                "keywords": [
                    "decision",
                    "risk",
                    "information",
                    "reasoning",
                ],
            },
            {
                "question": "Tell me about a major failure or setback and explain what you changed afterward.",
                "topic": "Problem Solving",
                "keywords": [
                    "failure",
                    "lesson",
                    "improve",
                    "change",
                ],
            },
            {
                "question": "Describe a situation where you had to influence others without having formal authority.",
                "topic": "Leadership",
                "keywords": [
                    "influence",
                    "leadership",
                    "communication",
                    "team",
                ],
            },
        ],
    },
}


# ============================================================
# OPTIONAL AI CONFIGURATION
# ============================================================

# Load environment variables when the engine is imported directly.
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile",
)

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


# ============================================================
# NORMALIZATION HELPERS
# ============================================================

def _clean_text(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip()


def normalize_role(role: Any) -> str:
    """
    Convert a user-selected job role into a broad role category.
    """

    role_text = _clean_text(role)

    if not role_text:
        return "General"

    role_lower = role_text.casefold()

    for category, keywords in ROLE_CATEGORIES.items():

        if category == "General":
            continue

        for keyword in keywords:

            if keyword.casefold() in role_lower:
                return category

    return "General"


def normalize_interview_type(interview_type: Any) -> str:
    """
    Normalize all UI interview-type labels into stable internal values.
    """

    value = _clean_text(interview_type)

    if not value:
        return DEFAULT_INTERVIEW_TYPE

    lower = value.casefold()

    if (
        "hr" in lower
        or "behavior" in lower
        or "behaviour" in lower
    ):
        return "HR / Behavioral"

    if "mixed" in lower:
        return "Mixed"

    if (
        "project" in lower
        or "case" in lower
    ):
        return "Project-Based"

    if (
        "technical" in lower
        or "tech" in lower
    ):
        return "Technical"

    return value


def normalize_difficulty(
    difficulty: Any
) -> str:

    value = _clean_text(difficulty)

    if not value:
        return DEFAULT_DIFFICULTY

    lower = value.casefold()

    if lower == "easy":
        return "Easy"

    if lower == "medium":
        return "Medium"

    if lower == "hard":
        return "Hard"

    if lower == "adaptive":
        return "Adaptive"

    return DEFAULT_DIFFICULTY


# ============================================================
# ROLE DOMAINS
# ============================================================

def get_role_domains(
    target_role: Any
) -> List[str]:

    category = normalize_role(
        target_role
    )

    return list(
        ROLE_DOMAINS.get(
            category,
            ROLE_DOMAINS["General"],
        )
    )


# ============================================================
# ADAPTIVE DIFFICULTY
# ============================================================

def determine_next_difficulty(
    current_scores: Optional[List[float]],
    question_number: int,
) -> str:
    """
    Determine difficulty only when Adaptive mode is selected.
    """

    scores = []

    for score in current_scores or []:

        try:
            scores.append(
                float(score)
            )
        except (
            TypeError,
            ValueError,
        ):
            continue

    # First questions start easy.
    if not scores:
        return "Easy"

    average_score = (
        sum(scores) / len(scores)
    )

    if average_score < 50:
        return "Easy"

    if average_score < 70:
        return "Medium"

    if average_score < 85:

        if question_number >= 5:
            return "Hard"

        return "Medium"

    return "Hard"


# ============================================================
# QUESTION NORMALIZATION
# ============================================================

def normalize_question(
    question: Any
) -> Optional[Dict[str, Any]]:

    if not isinstance(
        question,
        dict,
    ):
        return None

    question_text = _clean_text(
        question.get(
            "question",
            "",
        )
    )

    if not question_text:
        return None

    topic = _clean_text(
        question.get(
            "topic",
            "General",
        )
    )

    keywords = question.get(
        "keywords",
        [],
    )

    if not isinstance(
        keywords,
        list,
    ):
        keywords = []

    keywords = [
        _clean_text(keyword)
        for keyword in keywords
        if _clean_text(keyword)
    ]

    return {
        "question": question_text,
        "topic": topic or "General",
        "keywords": keywords,
        "difficulty": normalize_difficulty(
            question.get(
                "difficulty",
                "Medium",
            )
        ),
        "role_category": _clean_text(
            question.get(
                "role_category",
                "General",
            )
        ),
        "interview_type": _clean_text(
            question.get(
                "interview_type",
                "",
            )
        ),
        "skill": _clean_text(
            question.get(
                "skill",
                "general",
            )
        ),
    }


# ============================================================
# DUPLICATE NORMALIZATION
# ============================================================

def question_key(
    question: Any
) -> str:

    if isinstance(
        question,
        dict,
    ):
        text = question.get(
            "question",
            "",
        )
    else:
        text = question

    text = _clean_text(
        text
    )

    # Normalize whitespace and punctuation
    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.casefold()


# ============================================================
# FALLBACK QUESTION SELECTION
# ============================================================

def _fallback_question(
    target_role: Any,
    difficulty: str,
    used_questions: Optional[List[Any]] = None,
) -> Optional[Dict[str, Any]]:

    category = normalize_role(
        target_role
    )

    difficulty = normalize_difficulty(
        difficulty
    )

    if difficulty == "Adaptive":
        difficulty = "Easy"

    used_keys = {
        question_key(item)
        for item in (
            used_questions or []
        )
        if item
    }

    bank = ROLE_QUESTION_BANK.get(
        category,
        ROLE_QUESTION_BANK["General"],
    )

    questions = bank.get(
        difficulty,
        [],
    )

    available = [
        question
        for question in questions
        if question_key(question)
        not in used_keys
    ]

    if not available:
        # Search every difficulty for a
        # remaining unique question.
        for level in DIFFICULTY_ORDER:

            for question in bank.get(
                level,
                [],
            ):

                if (
                    question_key(question)
                    not in used_keys
                ):
                    return normalize_question(
                        {
                            **question,
                            "difficulty": level,
                            "role_category": category,
                        }
                    )

        return None

    return normalize_question(
        {
            **random.choice(
                available
            ),
            "difficulty": difficulty,
            "role_category": category,
        }
    )


# ============================================================
# OPTIONAL OPENAI QUESTION GENERATOR
# ============================================================

def _get_candidate_profile(
    profile_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, str]:
    """
    Get candidate profile information for AI question generation.

    If profile_context is not passed explicitly, the active Streamlit
    session profile is used automatically. This keeps existing callers
    backward-compatible.
    """

    profile = profile_context if isinstance(profile_context, dict) else {}

    if not profile:
        try:
            import streamlit as st

            user = st.session_state.get("user", {})
            if isinstance(user, dict):
                profile = user
        except Exception:
            profile = {}

    return {
        "education": _clean_text(profile.get("education", "")),
        "experience": _clean_text(
            profile.get(
                "experience",
                profile.get("experience_level", ""),
            )
        ),
        "skills": _clean_text(
            profile.get(
                "skills",
                profile.get("technical_skills", ""),
            )
        ),
        "career_goal": _clean_text(profile.get("career_goal", "")),
    }


def _generate_ai_question(
    target_role: Any,
    interview_type: Any,
    difficulty: str,
    focus_area: Any,
    previous_questions: Optional[List[Any]],
    profile_context: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """
    Generate a question using OpenAI when an API key is configured.

    If OpenAI is unavailable, this function returns None and the
    engine automatically uses the safe fallback question bank.
    """

    if not GROQ_API_KEY:
        return None

    try:
        from openai import OpenAI

    except ImportError:
        return None

    role = _clean_text(
        target_role
    ) or DEFAULT_ROLE

    interview_type = normalize_interview_type(
        interview_type
    )

    difficulty = normalize_difficulty(
        difficulty
    )

    focus = _clean_text(
        focus_area
    ) or "General"

    profile = _get_candidate_profile(
        profile_context
    )

    category = normalize_role(
        role
    )

    domains = get_role_domains(
        role
    )

    previous = []

    for item in (
        previous_questions or []
    ):

        if isinstance(
            item,
            dict,
        ):
            text = item.get(
                "question",
                "",
            )
        else:
            text = item

        text = _clean_text(
            text
        )

        if text:
            previous.append(
                text
            )

    previous_text = "\n".join(
        f"- {item}"
        for item in previous[-15:]
    )

    if not previous_text:
        previous_text = "None"

    profile_lines = []

    if profile["education"]:
        profile_lines.append(
            f"- Education: {profile['education']}"
        )

    if profile["experience"]:
        profile_lines.append(
            f"- Experience level: {profile['experience']}"
        )

    if profile["skills"]:
        profile_lines.append(
            f"- Technical skills: {profile['skills']}"
        )

    if profile["career_goal"]:
        profile_lines.append(
            f"- Career goal: {profile['career_goal']}"
        )

    profile_text = "\n".join(profile_lines)

    if not profile_text:
        profile_text = "No additional candidate profile information provided."

    prompt = f"""
You are Mirai AI's professional interview question generator.

Generate exactly ONE interview question.

Candidate target role:
{role}

Candidate profile:
{profile_text}

Role category:
{category}

Interview type:
{interview_type}

Difficulty:
{difficulty}

Focus area:
{focus}

Relevant professional domains:
{", ".join(domains)}

Previously asked questions:
{previous_text}

STRICT REQUIREMENTS:

Candidate personalization rules:
- Use the candidate profile to personalize the question when useful.
- Match the question to the candidate's experience level when appropriate.
- Use the candidate's technical skills as relevant focus areas; do not force every skill into one question.
- Consider education and career goal when they meaningfully affect the question.
- Do not expose or unnecessarily mention the candidate profile in the question.

1. The question MUST be relevant to the target role.
2. Do NOT default to IT, programming, Python, or AI/ML unless the target role requires it.
3. The question MUST match the requested interview type.
4. The question MUST match the requested difficulty.
5. Do not repeat or closely rephrase any previous question.
6. For Easy, test fundamentals.
7. For Medium, test practical application and reasoning.
8. For Hard, test advanced reasoning, trade-offs, complex scenarios,
   leadership, strategy, or professional judgment as appropriate.
9. If the role is accounting, ask accounting/finance questions.
10. If the role is sales, ask sales questions.
11. If the role is marketing, ask marketing questions.
12. If the role is HR, ask HR questions.
13. If the role is management, ask management/project/leadership questions.
14. Keep the question suitable for an actual job interview.
15. Return ONLY valid JSON.

Return exactly:

{{
    "question": "The interview question",
    "topic": "The relevant topic",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "difficulty": "{difficulty}",
    "role_category": "{category}",
    "interview_type": "{interview_type}",
    "skill": "The main skill being evaluated"
}}
"""

    try:

        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url=GROQ_BASE_URL,
            max_retries=0,
            timeout=30.0,
        )

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            temperature=0.8,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Mirai AI, a professional "
                        "interview question generator. "
                        "Always follow the requested role "
                        "and difficulty."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = (
            response.choices[0]
            .message
            .content
        )

        if not content:
            return None

        content = content.strip()

        # Remove accidental markdown fences.
        if content.startswith(
            "```"
        ):
            content = re.sub(
                r"^```(?:json)?",
                "",
                content,
                flags=re.IGNORECASE,
            )

            content = re.sub(
                r"```$",
                "",
                content,
            )

            content = content.strip()

        import json

        data = json.loads(
            content
        )

        question = normalize_question(
            data
        )

        if question is None:
            return None

        # Enforce the configuration in Python too.
        question["role_category"] = category
        question["interview_type"] = (
            interview_type
        )

        if difficulty != "Adaptive":
            question["difficulty"] = (
                difficulty
            )

        return question

    except Exception:
        return None


# ============================================================
# MAIN QUESTION GENERATOR
# ============================================================

def generate_unique_question(
    interview_type: Any,
    scores: Optional[List[float]],
    used_questions: Optional[List[Any]],
    question_number: int,
    target_role: Any = None,
    difficulty: Any = "Adaptive",
    focus_area: Any = None,
    interview_mode: Any = None,
    profile_context: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """
    Main question-generation function.

    Supports both the old and new calling styles.

    Old:
        generate_unique_question(
            interview_type,
            scores,
            used_questions,
            question_number
        )

    New:
        generate_unique_question(
            interview_type,
            scores,
            used_questions,
            question_number,
            target_role,
            difficulty,
            focus_area,
            interview_mode
        )
    """

    target_role = (
        _clean_text(
            target_role
        )
        or DEFAULT_ROLE
    )

    interview_type = normalize_interview_type(
        interview_type
    )

    difficulty = normalize_difficulty(
        difficulty
    )

    # --------------------------------------------------------
    # Determine actual difficulty
    # --------------------------------------------------------

    if difficulty == "Adaptive":

        actual_difficulty = (
            determine_next_difficulty(
                scores,
                question_number,
            )
        )

    else:

        # Explicit Easy/Medium/Hard
        # MUST be respected.
        actual_difficulty = difficulty

    # --------------------------------------------------------
    # Used questions
    # --------------------------------------------------------

    used_questions = (
        used_questions or []
    )

    used_keys = {
        question_key(item)
        for item in used_questions
        if item
    }

    # --------------------------------------------------------
    # Try AI first
    # --------------------------------------------------------

    ai_question = _generate_ai_question(
        target_role=target_role,
        interview_type=interview_type,
        difficulty=actual_difficulty,
        focus_area=focus_area,
        previous_questions=used_questions,
        profile_context=profile_context,
    )

    if ai_question is not None:

        if (
            question_key(ai_question)
            not in used_keys
        ):
            return ai_question

    # --------------------------------------------------------
    # Safe role-aware fallback
    # --------------------------------------------------------

    fallback = _fallback_question(
        target_role=target_role,
        difficulty=actual_difficulty,
        used_questions=used_questions,
    )

    if fallback is not None:

        if (
            question_key(fallback)
            not in used_keys
        ):
            fallback["interview_type"] = (
                interview_type
            )

            return fallback

    # --------------------------------------------------------
    # Final fallback:
    # Search all role questions.
    # --------------------------------------------------------

    category = normalize_role(
        target_role
    )

    bank = ROLE_QUESTION_BANK.get(
        category,
        ROLE_QUESTION_BANK["General"],
    )

    all_questions = []

    for level in DIFFICULTY_ORDER:

        for question in bank.get(
            level,
            [],
        ):

            if (
                question_key(question)
                not in used_keys
            ):

                item = normalize_question(
                    {
                        **question,
                        "difficulty": level,
                        "role_category": category,
                        "interview_type": interview_type,
                    }
                )

                if item:
                    all_questions.append(
                        item
                    )

    if all_questions:

        return random.choice(
            all_questions
        )

    return None


# ============================================================
# ADAPTIVE QUESTION SELECTION
# ============================================================

def select_adaptive_question(
    interview_type,
    current_scores,
    used_questions,
    question_number,
    target_role=None,
    difficulty="Adaptive",
    focus_area=None,
    interview_mode=None,
    requested_difficulty=None,
    profile_context=None,
):
    """
    Backward-compatible public function used by
    pages/interview.py.

    Supports both:

        difficulty=

    and the older:

        requested_difficulty=

    This keeps the existing interview page unchanged.
    """

    # --------------------------------------------------------
    # BACKWARD COMPATIBILITY
    # --------------------------------------------------------
    #
    # Your existing pages/interview.py may send:
    #
    # requested_difficulty="Easy"
    #
    # The new engine internally uses:
    #
    # difficulty="Easy"
    #
    # If requested_difficulty exists, it takes priority.
    # --------------------------------------------------------

    if requested_difficulty is not None:

        difficulty = requested_difficulty

    # --------------------------------------------------------
    # Generate the question
    # --------------------------------------------------------

    return generate_unique_question(
        interview_type=interview_type,
        scores=current_scores,
        used_questions=used_questions,
        question_number=question_number,
        target_role=target_role,
        difficulty=difficulty,
        focus_area=focus_area,
        interview_mode=interview_mode,
        profile_context=profile_context,
    )
# ============================================================
# ANSWER EVALUATION
# ============================================================
#
# This remains the existing local evaluator for now.
#
# Step 4 will replace/upgrade this with actual AI evaluation.
# ============================================================

def _count_words(
    text: str
) -> int:

    return len(
        text.split()
    )


def _generate_ai_evaluation(
    answer,
    question,
):
    """
    Evaluate a candidate answer using Groq AI.

    Returns a normalized evaluation dictionary on success.
    Returns None if Groq is unavailable or the response cannot be
    safely parsed, allowing the existing local evaluator to run.
    """

    if not GROQ_API_KEY:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    answer = _clean_text(answer)

    if not answer:
        return None

    if not isinstance(question, dict):
        question = {}

    question_text = _clean_text(question.get("question", ""))
    topic = _clean_text(question.get("topic", "General"))
    difficulty = normalize_difficulty(question.get("difficulty", "Medium"))
    role_category = _clean_text(question.get("role_category", "General"))
    interview_type = normalize_interview_type(
        question.get("interview_type", "Technical")
    )

    keywords = question.get("keywords", [])
    if not isinstance(keywords, list):
        keywords = []
    keywords = [
        _clean_text(item)
        for item in keywords
        if _clean_text(item)
    ]

    prompt = f"""
You are Mirai AI, a professional interview evaluator.

Evaluate the candidate's answer to the interview question.

INTERVIEW INFORMATION

Role category:
{role_category}

Interview type:
{interview_type}

Difficulty:
{difficulty}

Topic:
{topic}

Question:
{question_text}

Important concepts/keywords:
{", ".join(keywords) if keywords else "None"}

Candidate answer:
{answer}

EVALUATION RULES

1. Evaluate the actual meaning of the answer, not just keyword matching.
2. Do not give a high score merely because the answer is long.
3. Do not penalize a concise answer if it is accurate and complete.
4. Judge correctness according to the role and question.
5. Consider whether the candidate directly answered the question.
6. Consider reasoning and practical understanding where appropriate.
7. Consider clarity and organization.
8. Consider whether examples are useful when an example is appropriate.
9. Do not require keywords if the candidate explains the same concept using different words.
10. For behavioral/HR questions, focus on communication, judgment, ownership,
    reasoning, and relevance rather than technical knowledge.
11. For accounting/finance questions, judge accounting/financial correctness.
12. For sales questions, judge sales reasoning, customer handling, negotiation,
    and commercial thinking.
13. For marketing questions, judge marketing reasoning and practical understanding.
14. For management questions, judge leadership, decision-making, planning,
    prioritization, and stakeholder thinking.
15. For technical questions, judge technical correctness and depth.
16. Confidence must be inferred cautiously from how clearly and decisively
    the candidate communicates. Do not claim to detect actual emotions.
17. Scores must be between 0 and 100.
18. Return ONLY valid JSON.
19. Do not use markdown.
20. Do not include additional fields.

Return exactly this JSON structure:

{{
    "overall_score": 0,
    "technical_score": 0,
    "communication_score": 0,
    "problem_solving_score": 0,
    "answer_structure_score": 0,
    "relevance_score": 0,
    "confidence_score": 0,
    "strengths": "Short explanation of the strongest parts of the answer.",
    "weaknesses": "Short explanation of what should be improved.",
    "feedback": "Specific and constructive feedback for the candidate.",
    "recommended_action": "One practical action the candidate should take next."
}}
"""

    try:
        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url=GROQ_BASE_URL,
            max_retries=0,
            timeout=30.0,
        )

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            temperature=0.2,
            max_tokens=700,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Mirai AI, a strict but fair professional "
                        "interview evaluator. Return only valid JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content
        if not content:
            return None

        content = content.strip()

        if content.startswith("```"):
            content = re.sub(
                r"^```(?:json)?",
                "",
                content,
                flags=re.IGNORECASE,
            )
            content = re.sub(r"```$", "", content).strip()

        import json
        data = json.loads(content)

        if not isinstance(data, dict):
            return None

        score_fields = [
            "overall_score",
            "technical_score",
            "communication_score",
            "problem_solving_score",
            "answer_structure_score",
            "relevance_score",
            "confidence_score",
        ]

        normalized = {}
        for field in score_fields:
            try:
                value = float(data.get(field, 0))
            except (TypeError, ValueError):
                value = 0

            normalized[field] = round(
                max(0, min(100, value)),
                1,
            )

        normalized["strengths"] = _clean_text(
            data.get("strengths", "No specific strengths were identified.")
        )
        normalized["weaknesses"] = _clean_text(
            data.get("weaknesses", "No specific weaknesses were identified.")
        )
        normalized["feedback"] = _clean_text(
            data.get(
                "feedback",
                "Review the answer and improve its clarity and depth.",
            )
        )
        normalized["recommended_action"] = _clean_text(
            data.get(
                "recommended_action",
                "Practice answering similar interview questions.",
            )
        )

        return normalized

    except Exception:
        # AI/API failure must never break the interview.
        return None


def evaluate_answer(
    answer,
    question,
):
    """
    Evaluate a candidate answer.

    Groq AI is the primary evaluator. The existing local evaluator
    remains as a safe fallback if Groq is unavailable.
    """

    answer = _clean_text(
        answer
    )

    # --------------------------------------------------------
    # AI EVALUATION - PRIMARY
    # --------------------------------------------------------

    ai_result = _generate_ai_evaluation(
        answer=answer,
        question=question,
    )

    if ai_result is not None:
        return ai_result

    if not answer:

        return {
            "overall_score": 0,
            "technical_score": 0,
            "communication_score": 0,
            "problem_solving_score": 0,
            "answer_structure_score": 0,
            "relevance_score": 0,
            "confidence_score": 0,
            "strengths": (
                "No answer was provided."
            ),
            "weaknesses": (
                "The question was not answered."
            ),
            "feedback": (
                "Please provide a complete answer."
            ),
            "recommended_action": (
                "Answer the question clearly "
                "and include an example where possible."
            ),
        }

    answer_lower = answer.casefold()

    word_count = _count_words(
        answer
    )

    keywords = question.get(
        "keywords",
        [],
    )

    if not isinstance(
        keywords,
        list,
    ):
        keywords = []

    # --------------------------------------------------------
    # Keyword relevance
    # --------------------------------------------------------

    matched_keywords = [
        keyword
        for keyword in keywords
        if _clean_text(keyword).casefold()
        in answer_lower
    ]

    if keywords:

        keyword_score = (
            len(matched_keywords)
            /
            len(keywords)
        ) * 100

    else:

        keyword_score = 60

    keyword_score = min(
        100,
        keyword_score,
    )

    # --------------------------------------------------------
    # Answer length/depth
    # --------------------------------------------------------

    if word_count < 10:
        length_score = 20

    elif word_count < 25:
        length_score = 45

    elif word_count < 50:
        length_score = 65

    elif word_count < 90:
        length_score = 80

    else:
        length_score = 92

    # --------------------------------------------------------
    # Structure
    # --------------------------------------------------------

    structure_words = [
        "first",
        "second",
        "because",
        "therefore",
        "for example",
        "for instance",
        "however",
        "finally",
        "result",
        "learned",
        "step",
        "approach",
        "reason",
    ]

    structure_matches = sum(
        1
        for word in structure_words
        if word in answer_lower
    )

    structure_score = min(
        100,
        45 + (
            structure_matches * 8
        ),
    )

    if word_count >= 50:
        structure_score += 5

    structure_score = min(
        100,
        structure_score,
    )

    # --------------------------------------------------------
    # Communication
    # --------------------------------------------------------

    communication_score = (
        length_score * 0.45
        +
        structure_score * 0.35
        +
        keyword_score * 0.20
    )

    communication_score = min(
        100,
        communication_score,
    )

    # --------------------------------------------------------
    # Technical / professional relevance
    # --------------------------------------------------------

    technical_score = keyword_score

    # --------------------------------------------------------
    # Problem solving
    # --------------------------------------------------------

    problem_solving_words = [
        "problem",
        "challenge",
        "solution",
        "approach",
        "analyze",
        "analysis",
        "reason",
        "reasoning",
        "result",
        "improve",
        "step",
        "because",
        "tradeoff",
        "alternative",
    ]

    problem_matches = sum(
        1
        for word in problem_solving_words
        if word in answer_lower
    )

    problem_solving_score = min(
        100,
        40 + (
            problem_matches * 7
        ),
    )

    if word_count >= 50:
        problem_solving_score += 5

    problem_solving_score = min(
        100,
        problem_solving_score,
    )

    # --------------------------------------------------------
    # Relevance
    # --------------------------------------------------------

    relevance_score = (
        keyword_score * 0.70
        +
        structure_score * 0.10
        +
        length_score * 0.20
    )

    relevance_score = min(
        100,
        relevance_score,
    )

    # --------------------------------------------------------
    # Confidence proxy
    # --------------------------------------------------------

    confidence_words = [
        "I believe",
        "I would",
        "I can",
        "I have",
        "my approach",
        "I handled",
        "I achieved",
    ]

    confidence_matches = sum(
        1
        for phrase in confidence_words
        if phrase.casefold()
        in answer_lower
    )

    confidence_score = min(
        100,
        50 + (
            confidence_matches * 8
        ),
    )

    # --------------------------------------------------------
    # Overall
    # --------------------------------------------------------

    overall_score = (
        relevance_score * 0.30
        +
        communication_score * 0.20
        +
        technical_score * 0.20
        +
        problem_solving_score * 0.20
        +
        structure_score * 0.10
    )

    overall_score = round(
        min(
            100,
            overall_score,
        ),
        1,
    )

    # --------------------------------------------------------
    # Feedback
    # --------------------------------------------------------

    strengths = []

    weaknesses = []

    if keyword_score >= 70:
        strengths.append(
            "Your answer addressed relevant concepts."
        )
    else:
        weaknesses.append(
            "Include more role-specific concepts."
        )

    if communication_score >= 70:
        strengths.append(
            "Your answer was reasonably clear and structured."
        )
    else:
        weaknesses.append(
            "Improve the clarity and structure of your explanation."
        )

    if problem_solving_score >= 70:
        strengths.append(
            "Your answer demonstrated reasoning."
        )
    else:
        weaknesses.append(
            "Explain your reasoning and approach more clearly."
        )

    if word_count >= 40:
        strengths.append(
            "You provided enough detail to explain your approach."
        )
    else:
        weaknesses.append(
            "Add more detail or a practical example."
        )

    if not strengths:
        strengths.append(
            "You attempted the question."
        )

    if not weaknesses:
        weaknesses.append(
            "Continue improving precision and depth."
        )

    return {
        "overall_score": overall_score,
        "technical_score": round(
            technical_score,
            1,
        ),
        "communication_score": round(
            communication_score,
            1,
        ),
        "problem_solving_score": round(
            problem_solving_score,
            1,
        ),
        "answer_structure_score": round(
            structure_score,
            1,
        ),
        "relevance_score": round(
            relevance_score,
            1,
        ),
        "confidence_score": round(
            confidence_score,
            1,
        ),
        "strengths": " ".join(
            strengths
        ),
        "weaknesses": " ".join(
            weaknesses
        ),
        "feedback": (
            "Your answer has been evaluated "
            "for relevance, communication, "
            "reasoning, and structure."
        ),
        "recommended_action": (
            "Continue practicing role-specific "
            "questions and support your answers "
            "with concrete examples."
        ),
    }


# ============================================================
# READINESS SCORE
# ============================================================

def calculate_readiness_score(
    scores: Optional[List[float]]
) -> float:

    if not scores:
        return 0.0

    valid_scores = []

    for score in scores:

        try:
            valid_scores.append(
                float(score)
            )

        except (
            TypeError,
            ValueError,
        ):
            continue

    if not valid_scores:
        return 0.0

    return round(
        sum(valid_scores)
        /
        len(valid_scores),
        1,
    )


# ============================================================
# PUBLIC HELPERS
# ============================================================

def get_role_category(
    target_role
) -> str:

    return normalize_role(
        target_role
    )


def get_available_difficulties():
    return [
        "Easy",
        "Medium",
        "Hard",
        "Adaptive",
    ]


def get_available_role_categories():
    return list(
        ROLE_CATEGORIES.keys()
    )


# ============================================================
# ENGINE STATUS
# ============================================================

def get_engine_status():
    """
    Useful for debugging without affecting the UI.
    """

    return {
        "engine": "Mirai Interview Engine",
        "role_aware": True,
        "difficulty_aware": True,
        "adaptive": True,
        "ai_question_generation": bool(
            GROQ_API_KEY
        ),
        "ai_answer_evaluation": bool(
            GROQ_API_KEY
        ),
        "fallback_questions": True,
        "duplicate_protection": True,
    }


# ============================================================
# END OF ENGINE
# ============================================================