
from app.services.skill_matcher import match_skills


def test_match_skills():
    result = match_skills(
        user_skills=["Python", "SQL", "FastAPI"],
        required_skills=[
            "Python", "SQL", "Docker", "FastAPI", "LangChain"
        ]
    )

    assert result["match_score"] == 60.0
    assert result["matched_skills"] == [
        "fastapi", "python", "sql"
    ]
    assert result["missing_skills"] == [
        "docker", "langchain"
    ]
