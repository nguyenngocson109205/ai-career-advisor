
import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
)

from app.agent.jd_extractor import JobDescription

from app.tools.career_tools import (
    analyze_skills,
    search_jobs,
    compare_skills,
    rank_jobs,
)

load_dotenv()

# 1. Khởi tạo LLM và đăng ký tools
tools = [
    analyze_skills,
    search_jobs,
    compare_skills,
    rank_jobs
]

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
)

structured_llm = llm.with_structured_output(
    JobDescription,
    method="json_schema"
)

def extract_id(jd_text: str) -> JobDescription:
    message = [
            SystemMessage(content="""
    Task:
    Extract the job title and required technical skills from a job description.

    Rules:
    - Use only information provided in the job description.
    - Include skills that are explicitly required.
    - Exclude optional or preferred skills.
    - Do not infer skills that are not mentioned.

    Missing information:
    - If no job title is provided, return "Unknown".
    - If no required technical skills are found, return an empty list.
    """)
]

llm_with_tools = llm.bind_tools(tools)

tool_map = {tool.name: tool for tool in tools}


# 2. Vòng lặp ReAct
def run_react_agent(question: str, max_rounds: int = 6, return_trace: bool = False) -> str:
    tool_trace = []

    messages = [
        SystemMessage(content="""
You are an AI career recommendation assistant.

Use available tools to analyze user skills,
search for relevant jobs, and compare skill gaps.

Only recommend jobs found in the provided data.
Do not invent job requirements or match scores.
Ask for clarification if essential information is missing.
Answer in Vietnamese.
"""),
        HumanMessage(content=question),
    ]

    for round_num in range(max_rounds):

        print(f"\n=== ROUND {round_num + 1} ===")

        # LLM quyết định hành động tiếp theo
        response = llm_with_tools.invoke(messages)

        messages.append(response)

        # Không còn tool calls -> kết thúc
        if not response.tool_calls:
            answer =  str(response.content)

            if return_trace:
                return{
                    "answer": answer,
                    "tools_used": tool_trace
                }

            return answer




        # Thực thi tất cả tool calls của vòng này
        for tool_call in response.tool_calls:
            
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            tool_trace.append(tool_name)

            print("ACTION:", tool_name)
            print("ARGS:", tool_args)

            selected_tool = tool_map.get(tool_name)

            if selected_tool is None:
                result = {"error": "Unknown tool"}
            else:
                try:
                    result = selected_tool.invoke(tool_args)
                except Exception as exc:
                    print("TOOL ERROR:", exc) 
                    result = {"error": "Tool execution failed"}

            print("OBSERVATION:", result)

            # Đưa kết quả tool về cho LLM
            messages.append(
                ToolMessage(
                    content=json.dumps(
                        result,
                        ensure_ascii=False,
                    ),
                    tool_call_id=tool_call["id"],
                )
            )

    answer = "Agent đã đạt giới hạn số vòng xử lý."

    if return_trace:
        return {
            "answer": answer,
            "tools_used": tool_trace
        }

    return answer
