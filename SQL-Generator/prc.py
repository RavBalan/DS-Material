from pymongo import MongoClient
import re
from model import get_deepseek_response
import pymongo

string = '''
<think>
Mongo_DB_FindQuery =  [collection.count_documents({"PlateStatus": 1})]
'''
# [collection.find({"TotalFeeAmount1": {"$gt": 100}}).sort("BillID", -1).limit(100)]

# pattern = r'\[collection\.find\((.*?)\)\]'
pattern = r'\[collection\.(.*?)\]'


match = re.search(pattern, string)

print(match.group(1))


def mongoClient(instance,database,collection,query):
    client      = MongoClient(instance)
    coll        = client[database].get_collection(collection)
    output = []
    try:
        query = f"coll.{query}"
        print("Mongo Query: ", query)    
        filtered = eval(query)
        # print(type(filtered))
        # for doc in filtered:
        #     output.append(doc)
        # return output
        if isinstance(filtered, pymongo.cursor.Cursor):
            return list(filtered)  # Convert cursor to list and return
        else:
            return filtered
    except Exception as e:
        return "Given Query is wrong"
      

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
prompt = [
    {
        "role": "system",
        "content": f"""
            You are an AI assistant for a chatbot. 

            # Instructions #
            - If user ask data-related questions you should generate {database_type}-style Python query code using the PyMongo  method in response.
            - Only use the **PyMongo function** with method chaining like `.limit()`, `.sort()`, or `.project()` where appropriate.
            - If User Ask Count Related Question Use Like count_documents.
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
    },
    {
    "role": "user",
    "content": "How Many Plates Are active"

    }
]
    # "content": "How Many Plates Are active"


# print("prompt>>",prompt)  # Debug: Verify prompt contents
modelprombt = get_deepseek_response(prompt)

llmOutput = ''
for chunk in modelprombt:
    content = chunk.choices[0].delta.content
    if content :
        llmOutput += content
        cleanedLlmoutput = re.sub(r"<think>.*?</think>", "", llmOutput, flags=re.DOTALL).strip() 
print(llmOutput)


pattern = r'\[collection\.(.*?)\]'


match = re.search(pattern, llmOutput)
print(match.group(1))

query = match.group(1)
mongoOutput = mongoClient(instance, database_name, collection_name, query)
print(mongoOutput)
