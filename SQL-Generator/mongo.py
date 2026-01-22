import streamlit as st
from pymongo import MongoClient 
from groq import Groq
import json
import re
import pymongo
# st.set_page_config(page_title="Vektorr", layout="wide")

# st.title("VEKTORR CHAT BOT ")
# client = Groq(api_key="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")


# databaseType = "MONGO"
# databaseName = 'admin'
# collectionName = 'chat-bot-alita'
# sql = "NO-SQL"
# schema = """
#           - DocumentBillID (INT32)
#           - PlateNumber (STRING)
#           - PlateState (STRING)
#           - PlateCountry (STRING)
#           - BillNumber (INT32)
#           - BillDate (DATE)
#           - BillType (STRING)
#           - NoticeType (STRING)
#           - VendorCode (STRING)
#           - TotalTransactionAmount (DOUBLE)
#           - TotalFeeAmount1 (DOUBLE)
#           - PaymentStatus (STRING)
#           - PlateStatus (INT32)
#           - PlateStartDate (STRING)
#           - PlateEndDate (STRING)
                  
#         """

# completion = client.chat.completions.create(
#     model="deepseek-r1-distill-llama-70b",
#     messages=[    
#             {
#                 "role": "system",
#                 "content": f"""
#             You are an AI assistant for a chatbot. Your job is to respond to user queries involving data by generating {databaseType}-style JSON queries.

#             🔹 Instructions:
#             - When the user asks a data-related question, respond with a **pure {databaseType} query object** inside the format:
#             SQL_QUERY={{...}}
#             - Do **NOT** include explanations, comments, or anything outside the `SQL_QUERY=...` block.

#             DatabaseType: {databaseType}
#             SqlType: {sql}
#             Schema: {schema}

#             For general, non-data questions, respond as a normal AI assistant.
#             """
#             },
#             {"role": "user", "content": "User Query: I want details of this plate EXN822"}        
#     ],    
#     temperature=0.1,
#     max_completion_tokens=4096,
#     top_p=0.95,
#     stream=True,
#     stop=None,
# )

# response = ""
# for chunk in completion:
#     content = chunk.choices[0].delta.content
#     if content:
#         response += content
        
# match = re.search(r'SQL_QUERY\s*=\s*(\{.*?\})', response, re.DOTALL)
# if match:
#     mongo_query_str = match.group(1)

#     try:
#         mongo_query = json.loads(mongo_query_str)

#         client = MongoClient("mongodb://localhost:27017/")
#         collection = client[databaseName].get_collection(collectionName)

#         results = collection.find(mongo_query)

#         for doc in results:
#             print(doc)

#     except json.JSONDecodeError as e:
#         print("Failed to parse Mongo query JSON:", e)
# else:
#     print("SQL_QUERY= not found in response")


# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
        

# # React to user input
# if prompt := st.chat_input("What is up?"):
#     # Display user message in chat message container
#     st.chat_message("user").markdown(prompt)
    
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     response = f"Echo: {prompt}"
#     # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         st.markdown(response)
#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})


  # Update URI as needed

# # Select database and collection


# # Fetch one document
# record = collection.find_one()
# print("Single Record:", record)

# # Fetch all documents (use limit for large datasets)
# records = collection.find().limit(1)
# for r in records:
#     print("Record:", r)

# # Optional: Query with filter

def mongoClient(instance,database,collection,query):
    client      = MongoClient(instance)
    coll        = client[database].get_collection(collection)
    output = []
    try:
        query = f"coll.{query}"
        filtered = eval(query)
        if isinstance(filtered, pymongo.cursor.Cursor):
            for doc in filtered:
                output.append(doc)
            return output  # Convert cursor to list and return
        else:
            return [{"count":filtered}]
    except Exception as e:
        print("Mongo Execution Error:", e)
        return "Given Query is wrong"

    
    
# client = MongoClient("mongodb://localhost:27017/")
# collection = client['admin'].get_collection('chat-bot-alita')
# # filtered = collection.find({"TotalFeeAmount1": {"$gt": 100}}).sort("_id", -1).limit(100)
# # filtered = collection.find({"PlateStatus": 1})
# output  = []

# query = 'collection.find({}).limit(1)'
# filtered = eval(query)
# for doc in filtered:
#     output.append(doc)
# print("Filtered:", output)            
    