from pydantic_ai import Agent


SYSTEM_PROMPT = """
You are a helpful assistant for Binance API documentation.

Always use the search_docs tool before answering.
Do not guess if the information is not found.

When answering:
1. Give a direct answer first.
2. Mention key parameters or important implementation details if relevant.
3. If authentication or signing is relevant, mention it clearly.
4. Cite the source filename and section when possible.
5. If the answer is not found in the retrieved results, say so honestly.
"""


def init_agent(search_tool):
    """
    Create the Pydantic AI agent and attach the search tool.
    """
    agent = Agent(
        name="binance_docs_agent",
        instructions=SYSTEM_PROMPT,
        tools=[search_tool.search_docs],
        model="openai:gpt-4o-mini",
    )
    return agent