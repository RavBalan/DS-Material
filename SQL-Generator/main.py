from pymongo import MongoClient
from model import get_deepseek_response
import re
from mongo import mongoClient

# Configuration
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

# Query input
user_query = "How Many Plates are active"
# "I want latest records of 100$ higher of fee amount not as billed date"
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
                "content": f"User Query: {user_query}"
            }
   
]

# Call DeepSeek
model_prombt = get_deepseek_response(prombt)
llm_output = ''
for chunk in model_prombt:
    content = chunk.choices[0].delta.content
    if content:
        llm_output += content  
print(llm_output)  

pattern = r'\[collection\.find\((.*?)\)\]'
match = re.search(pattern, llm_output)
if match:
  query = match.group(1)
  mongoOutput = mongoClient(isinstance, database_name, collection_name, query)
  print(mongoOutput)
  





# if match:
#     model_prombt = match.group(1) 
#     # print(model_prombt)
#     client = MongoClient("mongodb://localhost:27017/")
#     collection = client['admin']['chat-bot-alita']

#     try:
#         query = f"collection.find({model_prombt})"
#         filtered = eval(query)
#         for doc in filtered:
#             print(doc)
#     except Exception as e:
#         print(f"Error executing query: {e}")
# else:
#     print("Pattern not found")
