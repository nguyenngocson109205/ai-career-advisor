

from app.tools.career_tools import rank_jobs

result = rank_jobs.invoke({
    "user_skills": [
        "Python",
        "FastAPI",
        "SQL",
        "LangChain"
    ]
})

for job in result:
    print(
        job["job_title"],
        "-",
        job["match_score"],
        "%"
    )
