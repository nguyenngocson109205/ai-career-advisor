
from app.services.jd_analyzer import analyze_jd


jd_text = """
We are hiring a Junior AI Engineer.

Requirements:
- Strong Python programming skills
- Experience with FastAPI
- Knowledge of SQL
- Experience with Docker
- Familiarity with LangChain

Nice to Have:
- AWS
- Kubernetes
"""

user_skills = [
    "Python",
    "FastAPI",
    "SQL"
]

result = analyze_jd(
    jd_text=jd_text,
    user_skills=user_skills
)

print("\n=== JD ANALYSIS ===")
print(result)
