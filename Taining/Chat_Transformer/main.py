import streamlit as st
import pandas as pd
from transformers import pipeline

# Initialize the question-answering pipeline
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

# Streamlit UI components
st.title("Deecodes.io Excel QA System")
st.write("Upload an Excel file and ask questions based on its content.")

# File uploader for Excel sheet
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file:
    # Load the Excel file into a DataFrame
    df = pd.read_excel(uploaded_file)
    st.write("### Preview of Uploaded Excel Data")
    st.dataframe(df.head())  # Display the first few rows of the DataFrame

    # Convert DataFrame to a context string
    context = ""
    for _, row in df.iterrows():
        context += " | ".join([f"{col}: {val}" for col, val in row.items()]) + "\n"

    # Input field for the question
    question = st.text_input("Ask a question about the uploaded data")

    # Button to trigger the QA system
    if st.button("Get Answer"):
        if question:
            # Generate an answer using the pipeline
            result = qa_pipeline(question=question, context=context)
            st.write(f"**Answer:** {result['answer']}")
        else:
            st.write("Please enter a question.")
else:
    st.write("Upload an Excel file to get started.")
