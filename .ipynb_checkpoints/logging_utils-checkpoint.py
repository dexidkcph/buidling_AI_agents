import json
import secrets
from pathlib import Path
from datetime import datetime
from pydantic_ai.messages import ModelMessagesTypeAdapter

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def log_entry(agent, messages, source="user", version=None):
    tools = []
    for ts in agent.toolsets:
        tools.extend(ts.tools.keys())

    dict_messages = ModelMessagesTypeAdapter.dump_python(messages)

    return {
        "agent_name": agent.name,
        "agent_version": version,
        "system_prompt": agent._instructions,
        "provider": agent.model.system,
        "model": agent.model.model_name,
        "tools": tools,
        "messages": dict_messages,
        "source": source,
    }

def log_interaction_to_file(agent, messages, source="user", version=None):
    entry = log_entry(agent, messages, source, version)

    ts = entry["messages"][-1].get("timestamp")

    if isinstance(ts, str):
        try:
            ts_obj = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except Exception:
            ts_obj = datetime.utcnow()
    elif isinstance(ts, datetime):
        ts_obj = ts
    else:
        ts_obj = datetime.utcnow()

    ts_str = ts_obj.strftime("%Y%m%d_%H%M%S")

    rand_hex = secrets.token_hex(3)
    filename = f"{agent.name}_{ts_str}_{rand_hex}.json"
    filepath = LOG_DIR / filename

    with filepath.open("w", encoding="utf-8") as f_out:
        json.dump(entry, f_out, indent=2, default=serializer)

    return filepath
