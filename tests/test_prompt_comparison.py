
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()


class JobDescription(BaseModel):
    job_title: str = Field(
        description="Job title mentioned in the JD"
    )
    required_skills: list[str] = Field(
        description="Required technical skills from the JD"
    )


llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

structured_llm = llm.with_structured_output(
    JobDescription,
    method="json_schema"
)


# PROMPT A - Cách ông viết
prompt_a = """
Only extract skills from the Requirements section.
Do not invent any skills.
"""


# PROMPT B - Bản chi tiết hơn
prompt_b = """
Extract the job title and required technical skills from the JD.

Only extract skills explicitly listed in the Requirements section.
Do not include skills from the Nice to Have section.
Do not invent or infer any skills.
"""


jd_text = """
We are looking for a Junior AI Engineer.

Responsibilities:
- Develop REST APIs using FastAPI.
- Collaborate with the data engineering team.
- Deploy AI applications to production.

Requirements:
- Strong programming skills in Python.
- Experience with SQL databases.
- Understanding of machine learning fundamentals.

Preferred Qualifications:
- Experience with Docker and Kubernetes.
- Familiarity with LangChain.
- Knowledge of AWS.
"""

expected_skills = {
    "Python",
    "SQL",
    "Machine Learning"
}


def run_prompt(system_prompt: str):
    response = structured_llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=jd_text)
    ])
    return response.model_dump()


result_a = run_prompt(prompt_a)
result_b = run_prompt(prompt_b)




def evaluate(result: dict):
    actual = set(result["required_skills"])
    return {
        "correct_skills": actual == expected_skills,
        "missing": sorted(expected_skills - actual),
        "extra": sorted(actual - expected_skills),
    }


print("\n=== PROMPT A ===")
print(result_a)
print(evaluate(result_a))

print("\n=== PROMPT B ===")
print(result_b)
print(evaluate(result_b))
