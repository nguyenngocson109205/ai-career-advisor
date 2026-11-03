def match_skills(
    user_skills: list[str],
    required_skills: list[str],
) -> dict:
    user_set ={
        skill.strip().lower()
        for skill in user_skills
    }
    
    required_set = {
        skill.strip().lower()
        for skill in required_skills
    }
    
    matched = sorted(user_set & required_set)
    missing = sorted(required_set - user_set)
    
    score = (
        round(len(matched) / len(required_set) * 100, 2)
        if required_set else 0.0
    )
    
    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_score": score
    }