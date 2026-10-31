
from app.tools.career_tools import analyze_skills
from app.tools.career_tools import search_jobs, compare_skills

result = analyze_skills.invoke({
    "skills": [
        " Python ",
        "FastAPI",
        "LangChain"
    ]
})

print(result)

print("\n=== SEARCH JOBS ===")

jobs_result = search_jobs.invoke({
    "role": "AI Engineer"
})

print(jobs_result)


print("\n=== COMPARE SKILLS ===")

comparison = compare_skills.invoke({
    "user_skills": ["Python", "FastAPI", "LangChain"],
    "job_id": 1
})

print(comparison)