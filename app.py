from __future__ import annotations

import json
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "skillsbridge.db"

app = Flask(__name__)
app.secret_key = os.environ.get("SKILLSBRIDGE_SECRET_KEY", "skillsbridge-sa-local-development-key")

# A transparent, explainable skills vocabulary for common entry-level digital roles.
# This is intentionally editable: add terms and synonyms as the project grows.
SKILL_CATALOG = {
    "Python": ["python", "pandas", "numpy", "flask", "django", "fastapi"],
    "Java": ["java", "spring boot", "spring"],
    "JavaScript": ["javascript", "js", "typescript", "react", "node.js", "nodejs", "vue", "angular"],
    "C# / .NET": ["c#", "c sharp", ".net", "dotnet", "asp.net"],
    "SQL & Databases": ["sql", "sqlite", "mysql", "postgresql", "postgres", "sql server", "database", "databases"],
    "HTML & CSS": ["html", "css", "responsive design", "bootstrap", "tailwind"],
    "Git & GitHub": ["git", "github", "version control", "gitlab"],
    "REST APIs": ["rest api", "restful", "api development", "apis", "http"],
    "Testing & Debugging": ["unit testing", "pytest", "testing", "debugging", "test-driven", "tdd"],
    "Data Analysis": ["data analysis", "data analytics", "excel", "power bi", "tableau", "data visualization"],
    "Machine Learning": ["machine learning", "scikit-learn", "sklearn", "classification", "regression", "model training"],
    "Natural Language Processing": ["nlp", "natural language processing", "text classification", "sentiment analysis"],
    "Cloud & Deployment": ["aws", "azure", "google cloud", "gcp", "docker", "deployment", "cloud computing"],
    "Agile & Collaboration": ["agile", "scrum", "kanban", "teamwork", "collaboration", "sprint planning"],
    "Problem Solving": ["problem solving", "analytical thinking", "critical thinking", "troubleshooting"],
    "Linux & Command Line": ["linux", "bash", "command line", "terminal", "powershell"],
    "Security Basics": ["cybersecurity", "information security", "authentication", "authorization", "secure coding"],
    "UI/UX Basics": ["ui/ux", "user experience", "user interface", "wireframe", "accessibility"],
}

RESOURCE_MAP = {
    "Python": ("Python for Everybody", "https://www.py4e.com/"),
    "Java": ("Dev.java learning resources", "https://dev.java/learn/"),
    "JavaScript": ("MDN JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"),
    "C# / .NET": (".NET learning centre", "https://learn.microsoft.com/en-us/dotnet/"),
    "SQL & Databases": ("SQLBolt interactive lessons", "https://sqlbolt.com/"),
    "HTML & CSS": ("MDN Learn Web Development", "https://developer.mozilla.org/en-US/docs/Learn"),
    "Git & GitHub": ("GitHub Skills", "https://skills.github.com/"),
    "REST APIs": ("MDN: HTTP overview", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview"),
    "Testing & Debugging": ("Python unittest documentation", "https://docs.python.org/3/library/unittest.html"),
    "Data Analysis": ("Kaggle Learn", "https://www.kaggle.com/learn"),
    "Machine Learning": ("Google Machine Learning Crash Course", "https://developers.google.com/machine-learning/crash-course"),
    "Natural Language Processing": ("Hugging Face NLP Course", "https://huggingface.co/learn/nlp-course/chapter1/1"),
    "Cloud & Deployment": ("Microsoft Azure Fundamentals", "https://learn.microsoft.com/en-us/training/azure/"),
    "Agile & Collaboration": ("Atlassian Agile Coach", "https://www.atlassian.com/agile"),
    "Problem Solving": ("HackerRank practice", "https://www.hackerrank.com/domains/algorithms"),
    "Linux & Command Line": ("Linux Journey", "https://linuxjourney.com/"),
    "Security Basics": ("OWASP Top 10", "https://owasp.org/www-project-top-ten/"),
    "UI/UX Basics": ("Google UX Design resources", "https://design.google/library/"),
}

ROLE_STARTER_SKILLS = {
    "Software Developer": ["Python", "Java", "SQL & Databases", "Git & GitHub", "REST APIs", "Testing & Debugging", "Problem Solving"],
    "Web Developer": ["HTML & CSS", "JavaScript", "Python", "Git & GitHub", "REST APIs", "UI/UX Basics"],
    "Data Analyst": ["SQL & Databases", "Data Analysis", "Python", "Problem Solving"],
    "Junior Data Scientist": ["Python", "SQL & Databases", "Data Analysis", "Machine Learning", "Statistics"],
    "IT Support / Systems": ["Linux & Command Line", "SQL & Databases", "Security Basics", "Problem Solving", "Cloud & Deployment"],
}

def connect_db():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                candidate_name TEXT NOT NULL,
                target_role TEXT NOT NULL,
                match_score INTEGER NOT NULL,
                matched_skills TEXT NOT NULL,
                missing_skills TEXT NOT NULL,
                job_title TEXT NOT NULL
            )
        """)


def normalize_text(value: str) -> str:
    value = (value or "").lower()
    value = value.replace("c sharp", "c#").replace("nodejs", "node.js")
    return re.sub(r"\s+", " ", value).strip()


def find_skills(text: str) -> list[str]:
    """Identify catalogued skills using case-insensitive phrase matching."""
    normalized = normalize_text(text)
    found = []
    for skill, terms in SKILL_CATALOG.items():
        if any(re.search(r"(?<![a-z0-9+#])" + re.escape(term.lower()) + r"(?![a-z0-9+#])", normalized) for term in terms):
            found.append(skill)
    return found


def analyze_match(candidate_skills_text: str, job_description: str, target_role: str):
    candidate_skills = set(find_skills(candidate_skills_text))
    job_skills = set(find_skills(job_description))

    # If a description does not contain catalogued skills, use a starter profile for
    # the chosen role so the user still gets a useful, clearly labelled baseline.
    used_role_baseline = False
    if not job_skills and target_role in ROLE_STARTER_SKILLS:
        job_skills = set(ROLE_STARTER_SKILLS[target_role])
        used_role_baseline = True

    matched = sorted(candidate_skills & job_skills)
    missing = sorted(job_skills - candidate_skills)
    extra = sorted(candidate_skills - job_skills)

    score = round((len(matched) / len(job_skills)) * 100) if job_skills else 0
    roadmap = []
    for skill in missing[:6]:
        title, link = RESOURCE_MAP.get(skill, ("Explore learning resources", "https://www.google.com/search?q=learn+" + skill.replace(" ", "+")))
        roadmap.append({"skill": skill, "resource": title, "url": link})

    if score >= 80:
        message = "Strong skills overlap. Check the role's full requirements and prepare examples that prove your skills."
    elif score >= 50:
        message = "Promising foundation. Focus on the missing skills below and build evidence through small projects."
    elif score > 0:
        message = "There are some relevant skills to build on. Follow the roadmap in order and practise with a portfolio project."
    else:
        message = "Start with the core skills listed for this role, then add practical evidence such as a small project or certificate."

    return {
        "score": score,
        "candidate_skills": sorted(candidate_skills),
        "job_skills": sorted(job_skills),
        "matched": matched,
        "missing": missing,
        "extra": extra,
        "roadmap": roadmap,
        "message": message,
        "used_role_baseline": used_role_baseline,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        candidate_name = request.form.get("candidate_name", "").strip()[:80]
        target_role = request.form.get("target_role", "").strip()
        job_title = request.form.get("job_title", "").strip()[:120]
        candidate_skills = request.form.get("candidate_skills", "").strip()[:8000]
        job_description = request.form.get("job_description", "").strip()[:12000]

        if not candidate_name or not target_role or not candidate_skills or not job_description:
            flash("Please complete your name, target role, current skills, and job description.", "error")
            return render_template("index.html", form=request.form, roles=list(ROLE_STARTER_SKILLS))

        analysis = analyze_match(candidate_skills, job_description, target_role)
        safe_title = job_title or target_role

        with connect_db() as connection:
            cursor = connection.execute(
                """INSERT INTO analyses
                   (created_at, candidate_name, target_role, match_score, matched_skills, missing_skills, job_title)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    candidate_name,
                    target_role,
                    analysis["score"],
                    json.dumps(analysis["matched"]),
                    json.dumps(analysis["missing"]),
                    safe_title,
                ),
            )
            analysis["analysis_id"] = cursor.lastrowid

        analysis["candidate_name"] = candidate_name
        analysis["target_role"] = target_role
        analysis["job_title"] = safe_title
        return render_template("results.html", analysis=analysis)

    return render_template("index.html", form={}, roles=list(ROLE_STARTER_SKILLS))


@app.route("/history")
def history():
    with connect_db() as connection:
        rows = connection.execute(
            "SELECT * FROM analyses ORDER BY id DESC LIMIT 25"
        ).fetchall()
    return render_template("history.html", analyses=rows)


@app.route("/health")
def health():
    return {"status": "ok", "application": "SkillsBridge SA"}


@app.errorhandler(404)
def not_found(_error):
    return render_template("error.html", title="Page not found", message="The page you're looking for doesn't exist."), 404


@app.errorhandler(500)
def server_error(_error):
    return render_template("error.html", title="Something went wrong", message="The application hit an unexpected error. Check the terminal for details."), 500


init_db()

if __name__ == "__main__":
    app.run(debug=True)
