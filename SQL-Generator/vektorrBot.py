import streamlit as st
from groq import Groq
from model import get_deepseek_response
import re

database_type = "MONGO-DB"
isinstance = "mongodb://localhost:27017/"
database_name = "admin"
collection_name = "chat-bot-alita"
sql_type = "NO-SQL"
schema = """
  - DocumentBillID (INT32)
  - PlateNumber (STRING)
  - PlateState (STRING)
  - PlateCountry (STRING)
  - BillNumber (INT32)
  - BillDate (DATE)
  - BillType (STRING)
  - NoticeType (STRING)
  - VendorCode (STRING)
  - TotalTransactionAmount (DOUBLE)
  - TotalFeeAmount1 (DOUBLE)
  - PaymentStatus (STRING)
  - PlateStatus (INT32)
  - PlateStartDate (STRING)
  - PlateEndDate (STRING)
"""
prombt = [
            {
              "role": "system",
              "content": f"""
                  You are an AI assistant for a chatbot. Your task is to generate {database_type}-style Python query code using the PyMongo `find()` method in response to user data-related questions.

                  # Instructions #
                  - Only use the **PyMongo `find()` function** with method chaining like `.limit()`, `.sort()`, or `.project()` where appropriate.
                  - Always return your answer as a single line of valid Python code like:

                    Mongo_DB_FindQuery = [collection.find({{ "field": "value" }}).limit(20)]

                  - Never include explanations, comments, or formatting outside this line of code.
                  - Never Use Date field without user asking for sorting
                  - If a query involves conditions (e.g., range, `$in`, `$gte`, etc.), embed them directly into the filter object.
                  - If a user asks for a specific number of results, use `.limit(n)`.
                  - If sorting is mentioned, add `.sort("field", 1)` for ascending or `.sort("field", -1)` for descending based on primarykey.
                  - If field projection is requested, use `.find(filter, projection)` with the appropriate keys set to 1 or 0.
                  
                  ## Context ##
                  - Database Type: {database_type}
                  - SQL Type: {sql_type}
                  - Schema: {schema}

                  For general, non-database questions, respond as a normal AI assistant.
              """
          },
            {
                "role": "user", 
                # "content": f"User Query: {st.chat_message("user")}"
            }
   
]

if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="VEKTORR Chatbot", layout="centered")
st.markdown("<h1 style='text-align: center;'>🤖 VEKTORR Chatbot</h1>", unsafe_allow_html=True)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if user_input := st.chat_input("Enter your query"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)
model_prombt = get_deepseek_response(prombt)













# # React to user input
# print(1)
# if prompt := st.chat_input():
#     # Display user message in chat message container
#     st.chat_message("user").markdown(prompt)
#     # Add user message to chat history
    
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     model_prombt = get_deepseek_response(prombt)

    
# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
#         # print(st.session_state.messages)
    
    
    
