
import pytest

from app.agent.react_agent import run_react_agent


test_cases = [
    (
        "Hãy chuẩn hóa các kỹ năng Python, SQL và FastAPI.",
        "analyze_skills"
    ),
    (
        "Tìm công việc AI Engineer trong dữ liệu hiện có.",
        "search_jobs"
    ),
    (
        "Tôi biết Python và FastAPI. "
        "Hãy so sánh kỹ năng của tôi với job ID 1.",
        "compare_skills"
    ),
    (
        "Tôi biết Python, SQL và LangChain. "
        "Hãy xếp hạng tất cả công việc phù hợp.",
        "rank_jobs"
    ),
]


@pytest.mark.parametrize(
    "question, expected_tool",
    test_cases
)
def test_agent_tool_selection(question, expected_tool):

    result = run_react_agent(
        question=question,
        return_trace=True
    )

    tools_used = result["tools_used"]

    print("\nEXPECTED:", expected_tool)   
    print("ACTUAL:", tools_used)

    assert expected_tool in tools_used
