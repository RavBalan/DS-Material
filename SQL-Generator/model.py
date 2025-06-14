import re
import json
from groq import Groq


client = Groq(api_key="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")

def get_deepseek_response(prombt):
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages= prombt,
        temperature=0.1,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=True,
    )
    return completion


        # response = ""
        # for chunk in completion:
        #     content = chunk.choices[0].delta.content
        #     if content:
        #         response += content

    # print(">>>", response)

    # match = re.search(r'SQL_QUERY\s*=\s*(\{.*?\})', response, re.DOTALL)
    # if match:
    #     try:
    #         mongo_query_str = match.group(1)
    #         mongo_query = json.loads(mongo_query_str)
    #         return mongo_query
    #     except json.JSONDecodeError as e:
    #         print("Failed to parse Mongo query JSON:", e)
    #         return None
    # else:
    #     print("SQL_QUERY= not found in response")
    #     return None
