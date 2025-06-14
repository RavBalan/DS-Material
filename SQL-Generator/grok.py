## Update File Of Chatbot

import streamlit as st
from model import get_deepseek_response
import re
from mongo import mongoClient
from bson import ObjectId  # Add this
from datetime import datetime
import builtins  # Add this at the top

# Define database and schema context
database_type = "MONGO-DB"
instance = "mongodb://localhost:27017/"
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

# Initialize LLM prompt with system instructions
prompt = [
    {
        "role": "system",
        "content": f"""
            You are an AI assistant for a chatbot. 

            # Instructions #
            - If user ask data-related questions you should generate {database_type}-style Python query code using the PyMongo  method in response.
            - Only use the **PyMongo function** with method chaining like `.limit()`, `.sort()`, or `.project()` where appropriate.
            - If User Ask Count Related Question Use Like count_documents Other wise use find.
            - Always return your answer as a single line of valid Python code like:

              Mongo_DB_FindQuery = [collection.{{}}]

            - You do only provide manupulation query
            - Never include explanations, comments, or formatting outside this line of code.
            - Never Use Date field without user asking for sorting.
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

# Render the fixed header
st.markdown("<div class='fixed-header'><h1>🤖 VEKTORR Chatbot</h1></div>", unsafe_allow_html=True)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Enter your query"):

    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    prompt = prompt[:1]  # Keep only system message
    prompt.extend(st.session_state.messages)  # Add all chat history
    cleanedLlmoutput = ''
    llmOutput = ''

    try:
        print("prompt>>",prompt)  # Debug: Verify prompt contents
        modelprombt = get_deepseek_response(prompt)
        
        for chunk in modelprombt:
            content = chunk.choices[0].delta.content
            if content :
                llmOutput += content
                cleanedLlmoutput = re.sub(r"<think>.*?</think>", "", llmOutput, flags=re.DOTALL).strip() 
        print(llmOutput)
    except Exception as e:
        llmOutput = f"Error: Could not get response from LLM ()"
    print("cleanedLlmoutput",cleanedLlmoutput)
    pattern = r'\[collection\.(.*?)\]'
    match = re.search(pattern, cleanedLlmoutput)
    mongoOutput = ''
    if match:
        query = match.group(1)
        mongoOutput = mongoClient(instance, database_name, collection_name, query)
        # st.code(f" Generated Query:  {query}", language='sql')
        print(mongoOutput,type(mongoOutput))
        # if mongoOutput
        formatted_output = [
            {k: str(v) if isinstance(v, (ObjectId, datetime)) else v for k, v in doc.items()}
            for doc in mongoOutput
        ]                                               
        with st.chat_message("assistant"):
            # st.markdown(mongoOutput)
            if formatted_output:
                st.table(formatted_output)  
        st.session_state.messages.append({"role": "assistant", "content": str(mongoOutput)})
    else:
        with st.chat_message("assistant"):
            st.markdown(cleanedLlmoutput)
        st.session_state.messages.append({"role": "assistant", "content": cleanedLlmoutput})


