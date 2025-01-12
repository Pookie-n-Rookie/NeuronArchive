import os
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEndpoint


load_dotenv()


huggingface_api_key= os.getenv('HUGGINGFACEHUB_API_TOKEN')

def answer_question(vectorstore, query):
    """Answers a question based on the provided vectorstore."""
    llm = HuggingFaceEndpoint(
        repo_id='mistralai/Mistral-7B-Instruct-v0.2',
        token=huggingface_api_key,
        temperature=0.5,
        max_new_tokens=512
    )
    
   
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={'k': 3})  
    )

    answer = qa({"query": query})
    return answer