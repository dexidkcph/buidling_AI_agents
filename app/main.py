import asyncio
from pathlib import Path
from dotenv import load_dotenv

from ingest import initialize_search_system
from search_tools import SearchTool
from search_agent import init_agent
from logs import log_interaction_to_file


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

JSON_PATH = PROJECT_ROOT / "my_chunks_sections.json"


def initialize_agent_system():
    print("Loading Binance documentation and building search system...")

    data = initialize_search_system(str(JSON_PATH))

    search_tool = SearchTool(
        binance_docs=data["binance_docs"],
        text_index=data["text_index"],
        embedding_model=data["embedding_model"],
        vector_embeddings=data["vector_embeddings"],
    )

    agent = init_agent(search_tool)

    print("Agent initialized successfully.")
    return agent


def main():
    agent = initialize_agent_system()

    print("\nReady to answer your Binance documentation questions.")
    print("Type 'stop' to exit.\n")

    while True:
        question = input("Your question: ").strip()

        if question.lower() == "stop":
            print("Goodbye!")
            break

        if not question:
            continue

        print("Processing...\n")
        response = asyncio.run(agent.run(user_prompt=question))

        print("Response:\n")
        print(response.output)
        print("\n" + "=" * 60 + "\n")

        log_interaction_to_file(agent, response.new_messages(), source="user", version="v3")


if __name__ == "__main__":
    main()