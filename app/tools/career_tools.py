from langchain_core.tools import tool
from app.data.jobs import jobs

"""
    Tool: analyze_skills
    Input: skills (list[str])
    Output: Danh sách những kĩ năng được chuẩn hóa
    Purpose: Chuẩn hóa kĩ năng đầu vào của người dùng
"""

@tool 
def analyze_skills(skills : list[str]) -> dict:
    """Normalize a user's technical skills"""

    normalized_skills = []
    for skill in skills:
        normalized_skills.append(
            skill.strip().lower()
        )

    return {
        "skills": normalized_skills,
        "total_skills": len(normalized_skills)
    }

@tool
def search_jobs(role:str) -> list[dict]:
    """Search for jobs matching a given role"""

    results = []

    for job in jobs:
        if role.lower() in job["title"].lower():
            results.append(job)

    return results

@tool 
def compare_skills(
    user_skills: list[str],
    job_id: int
) -> dict:
    """Compare user skills with job requirements"""

    job = next(
        (item for item in jobs if item["id"] == job_id),
        None
    )

    if job is None:
        return {"error": f"Job ID {job_id} not found"}
    user_set = {
        skill.strip().lower()
        for skill in user_skills
    }

    required_set = {
        skill.strip().lower()
        for skill in job["required_skills"]
    }

    matched = sorted(user_set & required_set)
    missing = sorted(required_set - user_set)

    score = (
        len(matched) / len(required_set) *100
        if required_set else 0
    )

    return {
        "job_id": job_id,
        "job_title": job["title"],
        "matched_skills": matched,
        "missing_skills": missing,
        "match_score": round(score, 2)
    }

@tool 
def rank_jobs(user_skills: list[str]) -> list[dict]:
    """Rank all avaliable jobs based on skill coverage"""

    user_set  = {
        skill.lower().strip()
        for skill in user_skills
    }

    recommendations = []

    for job in jobs:
        required_set = {
            skill.strip().lower()
            for skill in job["required_skills"]
        }
        matched = sorted(user_set & required_set)
        missing = sorted(required_set - user_set)

        score = (
            len(matched) / len(required_set) * 100
            if required_set else 0
        )

        recommendations.append({
            "job_id": job["id"],
            "job_title": job["title"],
            "match_score": round(score, 2),
            "matched_skills": matched,
            "missing_skills": missing,
        })

    recommendations.sort(
        key=lambda job: job["match_score"],
        reverse=True

    )

    return recommendations