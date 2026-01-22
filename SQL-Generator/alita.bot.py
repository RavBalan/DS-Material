from pptx import Presentation
import streamlit as st
from model import get_deepseek_response
import re
import os
import asyncio

async def main():
    def extract_ppt_text(file_path):
        prs = Presentation(file_path)
        text_runs = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    text_runs.append(shape.text.strip())
        return "\n".join(text_runs)

    def load_all_ppt(folder_path):
        ppt_context = {}
        for file in os.listdir(folder_path):
            if file.endswith(".pptx"):
                file_path = os.path.join(folder_path, file)
                ppt_name = os.path.splitext(file)[0]  
                ppt_context[ppt_name] = extract_ppt_text(file_path)
        return ppt_context

    # Load all PPTs
    folder_path = r"E:\DS\DS-Material\SQL-Generator\Doc"
    ppt_contexts = load_all_ppt(folder_path)

    # Combine all into one big context
    all_ppt_context = "\n\n".join(
        [f"### TITLE: {name} ### \n'CONTEXT:'{text}" for name, text in ppt_contexts.items()]
    )

    prompt = [
        {
            "role": "system",
            "content": f"""
            You are an AI business assistant. You have access to multiple PowerPoint presentations provided as context.

            ## Core Rules ##
            - Always respond in a professional, clear, and confident manner.
            - Use ONLY the information contained in the provided PPT context.
            - If a question refers to a specific PPT, use that PPT section.
            - If the question is general, compare and summarize across all PPTs.
            - If the context does not provide an answer, say:
            "That information is not available in the provided documents."
            - For tricky or vague questions:
                • Interpret the intent and provide the closest answer from the context.
                • If some details are missing, acknowledge the gap but still summarize what is available.
            - Summarize slides in simple business-friendly language when needed.
            - Never fabricate facts or bring in outside knowledge.

            ## Context (all PPTs) ##
            {all_ppt_context}
            """
        }
    ]
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.set_page_config(page_title="VEKTORR Chatbot", layout="centered")

    # Inject custom CSS to fix the header
    st.markdown("""
        <style>
        .fixed-header {
            position: left;
            top: 10;
            transform: translateX(30%)
            width: 100%;
            background-color: red;
            z-index: 9999;
            padding: 10px 0;
            text-align: center;
            border-bottom: 1px solid #ed0e0e;
            box-shadow: 0 15px 10px rgba(0,0,0,0.1);
        }
        .stApp {
            padding-top: 80px; /* adjust this to avoid overlap */
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='fixed-header'><h1>🤖 VEKTORR Chatbot</h1></div>", unsafe_allow_html=True)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Enter your query"):

        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.messages.append({"role": "user", "content": user_input})

        # print(prompt)
        prompt = prompt[:1]
        prompt.extend(st.session_state.messages)
        cleanedLlmoutput = ''
        llmOutput = ''

        try:
            modelprombt = await get_deepseek_response(prompt)
            async for chunk in modelprombt:
                print('modelprombt',chunk)
                # if chunk.choices[0].delta.get("content"):
                content = chunk.choices[0].delta.content
                if content :
                    llmOutput += content
                    cleanedLlmoutput = re.sub(r"<think>.*?</think>", "", llmOutput, flags=re.DOTALL).strip()
            # print(llmOutput)
        except Exception as e:
            llmOutput = f"Error: Could not get response from LLM ()"
        print("cleanedLlmoutput",cleanedLlmoutput)

        with st.chat_message("assistant"):
            st.markdown(cleanedLlmoutput)
        st.session_state.messages.append({"role": "assistant", "content": cleanedLlmoutput})

asyncio.run(main())
