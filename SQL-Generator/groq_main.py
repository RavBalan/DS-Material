#api_key="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"

import streamlit as st
from groq import Groq

# Set up Streamlit page configuration
st.set_page_config(page_title="Vektorr", layout="wide")


# Streamlit UI header
st.title("VEKTORR CHAT BOT ")

# User Input
user_query = st.text_area("Enter your query:", "")

# Submit button
if st.button("SUBMIT"):
    if not user_query.strip():
        st.warning("Please enter a query before submitting!")
    else:
        # Database schema
        table_schema = """
        ### Database Schema:
        - Table: DocumentBill
          - PlateCountry (VARCHAR)
          - PlateState (VARCHAR)
          - PlateNumber (VARCHAR)
          - BillNumber (VARCHAR, PRIMARY KEY)
          - BillDate datetime
          - BillType (VARCHAR)
          - NoticeType (VARCHAR)
          - VendorCode (VARCHAR)
          - VendorName (VARCHAR)
          - TotalTransactionAmount (DECIMAL)
          - TotalFeeAmount1 (DECIMAL)
          - TotalFeeAmount2 (DECIMAL)
          - TotalLateFeesAmount (DECIMAL)
          - TotalDelinquentAmount (DECIMAL)
          - TotalBillAmount (DECIMAL)
          - CreatedBy (VARCHAR)
          - CreatedDateTime datetime
          
        - Table: VmPlate
          - VmPlateID	(BIGINT)
          - PlateNumber	(VARCHAR)
          - PlateType	(VARCHAR)
          - PlateState	(VARCHAR)
          - PlateCountry	(VARCHAR)
          - ReceivedPlateNumber	(VARCHAR)
          - ReceivedPlateType	(VARCHAR)
          - ReceivedPlateState	(VARCHAR)
          - ReceivedPlateCountry	(VARCHAR)
          - StartDate	(DATETIME)
          - IsActive	(BIT)
          - EndDate	(DATETIME)
          - IsReactivated	(BIT)
          - IsSold	(BIT)
          - SoldDate	datetime
          - ModifiedDate	datetime
          - ModifiedBy	(VARCHAR)
          - Remarks	(VARCHAR)
          - IsReviewed	(BIT)
          - ReviewedBy	(VARCHAR)
          - ReviewedDate	datetime
          - ReviewStatus	(VARCHAR)
          - CreatedDate	datetime
          - CreatedBy	(VARCHAR)        
        
        """

        # Groq API setup
        client = Groq(api_key="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")

        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {"role": "system", "content": "You are an AI that provides SQL queries only when the user asks SQL-related questions. For general queries, respond as a normal AI."},
                {"role": "user", "content": f"Here is the database schema:\n\n{table_schema}\n\nUser Query: {user_query}"}
            ],
            temperature=0.1,
            max_completion_tokens=4096,
            top_p=0.95,
            stream=True,
            stop=None,
        )

        # Stream response
        response = ""
        placeholder = st.empty()  

        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                response += content
                placeholder.markdown(f"**Generating ...**\n\n```\n{response}\n```")  

        # Extract and display the SQL Query
        response_parts = response.split("```sql")
        if len(response_parts) > 1:
            sql_query = response_parts[1].split("```")[0].strip()
            # st.success("✅ **Generated SQL Query:**")
            st.code(sql_query, language="sql")
        # else:
            # st.error("❌ No SQL query found. The AI responded with:")
            # st.write(response)    
