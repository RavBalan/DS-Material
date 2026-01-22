#api_key= "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"
from groq import Groq
import streamlit as st
import re

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="VEKTORR Chatbot", layout="centered")
st.markdown("<h1 style='text-align: center;'>🤖 VEKTORR Chatbot</h1>", unsafe_allow_html=True)
st.markdown("---")

def render_chat():
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(
                f"<div style='background-color:#077A7D; padding:10px; border-radius:10px; margin:5px 0;'><strong>You:</strong> {msg['content']}</div>",
                unsafe_allow_html=True,
            )
        else:
            cleaned = re.sub(r"<think>.*?</think>", "", msg["content"], flags=re.DOTALL).strip()
            st.markdown(
                f"<div style='background-color:#034C53; padding:10px; border-radius:10px; margin:5px 0;'><strong>Vektorr: </strong> {cleaned}</div>",
                unsafe_allow_html=True,
            )

render_chat()

if "user_query" not in st.session_state:
    st.session_state.user_query = ""
    
user_query = st.text_area("Enter your query:", st.session_state.user_query)
submit_button = st.button("Send", use_container_width=True)


def fetch_response():
    client = Groq(api_key="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")  

    st.session_state.chat_history.append({"role": "user", "content": user_query})

    response = ""
    placeholder = st.empty()

    print(">>>>",st.session_state.chat_history)
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=st.session_state.chat_history,
        temperature=0.1,
        max_tokens=4096,
        top_p=0.95,
        stream=True,
    )

    for chunk in completion:
        if chunk.choices and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            response += content
            cleaned_live = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
            placeholder.markdown(
                f"<div style='background-color:#222121; padding:10px; border-radius:10px;'><strong>Bot:</strong> {cleaned_live}</div>",
                unsafe_allow_html=True
            )

    cleaned_final = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    st.session_state.chat_history.append({"role": "assistant", "content": cleaned_final})

if submit_button and user_query.strip():
    fetch_response()
    st.rerun()
elif submit_button:
    st.warning("Please enter a message before sending.")