from pydantic import BaseModel, Field

class JobDescription(BaseModel):
    job_title : str = Field(
        description="Job title mentioned in JD"
    )

    required_skills: list[str] = Field(
        description="Technical skills explicity required by JD"
    )