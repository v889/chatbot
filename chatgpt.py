import warnings
import logging
import streamlit as st
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv


load_dotenv()

warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

st.set_page_config(page_title="Ask Chatbot!", layout="wide")
st.title("Ask Chatbot!")

# --- Initialize session variables ---
if 'chat_sessions' not in st.session_state:
    st.session_state.chat_sessions = {}

if 'current_session' not in st.session_state:
    session_id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    st.session_state.current_session = session_id
    st.session_state.chat_sessions[session_id] = {
        "name": f"Chat - {session_id}",
        "messages": []
    }

if 'renaming_session' not in st.session_state:
    st.session_state.renaming_session = None

# --- SIDEBAR: Chat Management ---
with st.sidebar:
    st.header("💬 Chat Sessions")

    # New Chat Button
    if st.button("➕ New Chat"):
        session_id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.session_state.current_session = session_id
        st.session_state.chat_sessions[session_id] = {
            "name": f"Chat - {session_id}",
            "messages": []
        }

    # Search chats
    search_query = st.text_input("🔍 Search Chats").lower()
    filtered_sessions = {
        sid: chat
        for sid, chat in st.session_state.chat_sessions.items()
        if search_query in chat["name"].lower()
    }

    # List of chats with Rename & Select
    for sid, chat in filtered_sessions.items():
        if st.session_state.renaming_session == sid:
            new_name = st.text_input(
                f"Rename {chat['name']}",
                value=chat['name'],
                key=f"rename_input_{sid}"
            )
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✅ Save", key=f"save_{sid}"):
                    chat['name'] = new_name
                    st.session_state.renaming_session = None
            with col2:
                if st.button("❌ Cancel", key=f"cancel_{sid}"):
                    st.session_state.renaming_session = None
        else:
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(chat["name"], key=f"select_{sid}"):
                    st.session_state.current_session = sid
            with col2:
                if st.button("✏️", key=f"edit_{sid}"):
                    st.session_state.renaming_session = sid

# --- Chat Display ---
current_session_id = st.session_state.current_session
chat_data = st.session_state.chat_sessions[current_session_id]
messages = chat_data["messages"]

for msg in messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# --- Chat Input & Response ---
prompt = st.chat_input("Pass your prompt here")

if prompt:
    st.chat_message("user").markdown(prompt)
    messages.append({'role': 'user', 'content': prompt})

    # Use previous 5 messages as context
    old_context = "\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in messages[-6:-1]
    ) if len(messages) > 1 else "None"

    groq_sys_prompt = ChatPromptTemplate.from_template(f"""
You are a helpful assistant. Refer to previous chat context when relevant.

Previous chat context (if any):
{old_context}

Now answer the following question directly (no small talk):
{{user_prompt}}
""")

    model = "llama3-8b-8192"

    groq_chat = ChatGroq(
        groq_api_key=os.getenv("grok_api_key"),
        model_name=model
    )

    chain = groq_sys_prompt | groq_chat | StrOutputParser()
    response = chain.invoke({"user_prompt": prompt})

    st.chat_message("assistant").markdown(response)
    messages.append({'role': 'assistant', 'content': response})
