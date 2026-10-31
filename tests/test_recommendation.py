
from app.tools.career_tools import rank_jobs, compare_skills


def test_rank_jobs_order():
    result = rank_jobs.invoke({
        "user_skills": ["Python", "FastAPI", "SQL", "LangChain"]
    })

    scores = [job["match_score"] for job in result]

    assert scores == sorted(scores, reverse=True)


def test_rank_jobs_top_result():
    result = rank_jobs.invoke({
        "user_skills": ["Python", "FastAPI", "SQL", "LangChain"]
    })

    assert result[0]["job_title"] == "Junior AI Engineer"
    assert result[0]["match_score"] == 80.0


def test_compare_skills():
    result = compare_skills.invoke({
        "user_skills": ["Python", "FastAPI", "LangChain"],
        "job_id": 1
    })

    assert result["match_score"] == 60.0


def test_invalid_job_id():
    result = compare_skills.invoke({
        "user_skills": ["Python"],
        "job_id": 999
    })

    assert "error" in result
