import json
from pathlib import Path
from pydantic import BaseModel
from pydantic_ai import Agent

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "evaluation_results.csv"


class EvaluationCheck(BaseModel):
    check_name: str
    justification: str
    check_pass: bool


class EvaluationChecklist(BaseModel):
    checklist: list[EvaluationCheck]
    summary: str


evaluation_prompt = """
Use this checklist to evaluate the quality of an AI agent's answer (<ANSWER>)
to a user question (<QUESTION>).
We also include the full interaction log (<LOG>) for analysis.

For each item, check if the condition is met.

Checklist:
- instructions_follow: The agent followed the system instructions
- answer_relevant: The response directly answers the user's question
- answer_clear: The answer is easy to understand and technically correct
- answer_citations: The answer includes references or source filenames/sections when appropriate
- completeness: The answer covers the key parts of the user's request
- tool_call_search: The search_docs tool was used before answering

Output true/false for each check and provide a short explanation.
""".strip()


eval_agent = Agent(
    name="binance_eval_agent",
    model="openai:gpt-4o-mini",
    instructions=evaluation_prompt,
    output_type=EvaluationChecklist,
)


def load_log_file(log_file):
    with open(log_file, "r", encoding="utf-8") as f_in:
        log_data = json.load(f_in)
    log_data["log_file"] = str(log_file)
    return log_data


def simplify_log_messages(messages):
    log_simplified = []

    for m in messages:
        parts = []

        for original_part in m["parts"]:
            part = original_part.copy()
            kind = part["part_kind"]

            if kind == "user-prompt" and "timestamp" in part:
                del part["timestamp"]

            if kind == "tool-call" and "tool_call_id" in part:
                del part["tool_call_id"]

            if kind == "tool-return":
                if "tool_call_id" in part:
                    del part["tool_call_id"]
                if "metadata" in part:
                    del part["metadata"]
                if "timestamp" in part:
                    del part["timestamp"]
                part["content"] = "RETURN_RESULTS_REDACTED"

            if kind == "text" and "id" in part:
                del part["id"]

            parts.append(part)

        log_simplified.append({
            "kind": m["kind"],
            "parts": parts
        })

    return log_simplified


user_prompt_format = """
<INSTRUCTIONS>{instructions}</INSTRUCTIONS>
<QUESTION>{question}</QUESTION>
<ANSWER>{answer}</ANSWER>
<LOG>{log}</LOG>
""".strip()


async def evaluate_log_record(log_record):
    messages = log_record["messages"]
    instructions = log_record["system_prompt"]
    question = messages[0]["parts"][0]["content"]
    answer = messages[-1]["parts"][0]["content"]

    log_simplified = simplify_log_messages(messages)
    log_json = json.dumps(log_simplified)

    user_prompt = user_prompt_format.format(
        instructions=instructions,
        question=question,
        answer=answer,
        log=log_json,
    )

    result = await eval_agent.run(user_prompt)
    return result.output
