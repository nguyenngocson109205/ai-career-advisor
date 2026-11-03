from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()

JD_EXTRACTION_PROMPT = """
You are a job description information extraction assistant.

Task:
Extract the job title and mandatory technical skills from the JD.

Rules:
- Extract only skills explicitly required by the employer.
- Consider Requirements, Must-have Skills and Required Qualifications.
- Exclude Nice to Have, Preferred and Bonus Skills.
- Do not infer skills from responsibilities unless explicitly required.
- Normalize skills into short technical names.
  Examples:
  "Experience with Python programming" -> "Python"
  "Knowledge of SQL databases" -> "SQL"
  "Understanding of machine learning fundamentals" -> "Machine Learning"
- Do not invent skills.
- Remove duplicate skills.
- If no job title is found, return "Unknown".
- If no mandatory technical skills are found, return an empty list.
"""


class JobDescription(BaseModel):
    job_title : str = Field(
        description="Job title mentioned in JD"
    )

    required_skills: list[str] = Field(
        description="Technical skills explicity required by JD"
    )
    


llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

structured_llm = llm.with_structured_output(
    JobDescription,
    method="json_schema"
)


def extract_jd(jd_text: str) -> JobDescription:
    messages = [
        SystemMessage(content=JD_EXTRACTION_PROMPT),
        HumanMessage(content=jd_text)
    ]

    return structured_llm.invoke(messages)

