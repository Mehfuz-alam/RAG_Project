
import redis
import json
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.redis_host,
    port=6379,
    decode_responses=True
)


def get_memory(session_id: str) -> list[dict]:
    """
    Retrieve chat history for a session.
    Returns a list of {"role": "user"/"assistant", "content": "..."}.
    """
    data = redis_client.get(session_id)
    if data:
        return json.loads(data)
    return []


def update_memory(session_id: str, role: str, text: str):
    """
    Append a message to the session's memory in Redis.
    """
    history = get_memory(session_id)
    history.append({"role": role, "content": text})
    redis_client.set(session_id, json.dumps(history))


def get_all_sessions() -> list[dict]:
    """
    List all active sessions in Redis with optional metadata.
    """
    keys = redis_client.keys("*")
    sessions = []
    for k in keys:
        val = redis_client.get(k)
        if val:
            try:
                data = json.loads(val)
                sessions.append({"session_id": k, "history_length": len(data)})
            except json.JSONDecodeError:
                sessions.append({"session_id": k, "history_length": 0})
    return sessions