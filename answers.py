import os
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

def answer_question(vectorstore, query):
    """Answers a question based on the provided vectorstore using Groq API."""
    
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables. Please check your .env file.")
    
    llm = ChatGroq(
        model="llama-3.3-70b-versatile", 
        groq_api_key=groq_api_key,
        temperature=0.1,
        max_tokens=2000
    )

    # Creating QA chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
        return_source_documents=True
    )

    answer = qa.invoke({"query": query})
    return answer
