from app.agent.react_agent import run_react_agent

result = run_react_agent(
    question="Tôi biết Python và SQL. Hãy xếp hạng tất cả công việc.",
    return_trace=True
)

print(result)

