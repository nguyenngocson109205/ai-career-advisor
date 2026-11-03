from app.services.skill_matcher  import match_skills
from app.agent.jd_extractor import extract_jd

def analyze_jd(jd_text: str, user_skills: list[str]) -> dict:
    # 1. LLM trích xuất thông tin từ job 
    job = extract_jd(jd_text)
    
    # 2. So sánh user skill với jd 
    comparision = match_skills(
        user_skills=user_skills,
        required_skills= job.required_skills
    )
    
    # 3. trả ra kết quả
    return {
        "job_title": job.job_title,
        "required_skills": job.required_skills,
        **comparision
    }
    
    