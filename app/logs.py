import os
import json
import secrets
from pathlib import Path
from datetime import datetime
from pydantic_ai.messages import ModelMessagesTypeAdapter


LOG_DIR = Path(os.getenv("LOGS_DIRECTORY", "logs"))
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

    provider = None
    model_name = None

    try:
        provider = agent.model.system
    except Exception:
        pass

    try:
        model_name = agent.model.model_name
    except Exception:
        model_name = str(agent.model)

    return {
        "agent_name": agent.name,
        "agent_version": version,
        "system_prompt": getattr(agent, "_instructions", None),
        "provider": provider,
        "model": model_name,
        "tools": tools,
        "messages": dict_messages,
        "source": source,
    }


def log_interaction_to_file(agent, messages, source="user", version=None):
    entry = log_entry(agent, messages, source=source, version=version)
    ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    rand_hex = secrets.token_hex(3)

    filename = f"{agent.name}_{version or 'na'}_{ts_str}_{rand_hex}.json"
    filepath = LOG_DIR / filename

    with filepath.open("w", encoding="utf-8") as f_out:
        json.dump(entry, f_out, indent=2, default=serializer)

    return filepath