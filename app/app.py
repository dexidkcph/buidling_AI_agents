import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from ingest import initialize_search_system
from search_tools import SearchTool
from search_agent import init_agent
from logs import log_interaction_to_file


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

if "OPENAI_API_KEY" not in os.environ and "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

JSON_PATH = PROJECT_ROOT / "my_chunks_sections.json"


@st.cache_resource
def initialize_agent_system():
    data = initialize_search_system(str(JSON_PATH))

    search_tool = SearchTool(
        binance_docs=data["binance_docs"],
        text_index=data["text_index"],
        embedding_model=data["embedding_model"],
        vector_embeddings=data["vector_embeddings"],
    )

    agent = init_agent(search_tool)
    return agent


st.set_page_config(
    page_title="Binance Docs AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Binance Docs AI Assistant")
st.caption("Ask questions about Binance API documentation")

agent = initialize_agent_system()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = asyncio.run(agent.run(user_prompt=prompt))
                answer = response.output
                st.markdown(answer)

                st.session_state.messages.append({"role": "assistant", "content": answer})
                log_interaction_to_file(agent, response.new_messages(), source="user", version="v3")

            except Exception as e:
                st.error(f"Error: {type(e).__name__}: {e}")
                raise