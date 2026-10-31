from langchain_core.messages import BaseMessage

sessions: dict[str, list[BaseMessage]] = {}

def get_messages(session_id: str) -> list[BaseMessage]:
    if session_id not in sessions:
        sessions[session_id] = []

    return sessions[session_id]

def clear_session(session_id: str):
    sessions.pop(session_id, None)