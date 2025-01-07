import os
from langchain.chains import RetrievalQA


from langchain_huggingface import HuggingFaceEndpoint

from secret_api_keys import huggingface_api_key
os.environ['HUGGINGFACEHUB_API_TOKEN'] = huggingface_api_key

def answer_question(vectorstore, query):
    """Answers a question based on the provided vectorstore."""
    llm = HuggingFaceEndpoint(
        repo_id='meta-llama/Meta-Llama-3-8B-Instruct',
        token=huggingface_api_key,
        temperature=0.6,
        max_new_tokens=512 
    )
    
   
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={'k': 3})  
    )

    answer = qa({"query": query})
    return answer