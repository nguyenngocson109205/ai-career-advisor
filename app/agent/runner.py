
import json
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

from app.tools.product_tools import tools
from app.memory.session import get_messages

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)

tool_map = {tool.name: tool for tool in tools}


def run_agent(
    question: str,
    session_id: str,
    max_rounds: int = 5
) -> str:

    messages = get_messages(session_id)
    messages.append(HumanMessage(content=question))

    for round_num in range(max_rounds):

        print(f"LLM ROUND {round_num + 1}")

        response = llm_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return str(response.content)

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            selected_tool = tool_map.get(tool_name)

            if selected_tool is None:
                result = {"error": "Tool không tồn tại"}
            else:
                try:
                    result = selected_tool.invoke(tool_args)
                except Exception:
                    result = {"error": "Tool thực thi thất bại"}

            messages.append(
                ToolMessage(
                    content=json.dumps(result, ensure_ascii=False),
                    tool_call_id=tool_id
                )
            )

    # Đã hết số vòng nhưng model vẫn có thể đang yêu cầu tool.
    # Trả về thông báo thay vì giả định có câu trả lời cuối.
    return "Agent chưa hoàn thành trong giới hạn số vòng."
