from model import hf_embeddings
import numpy as np
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from preprocess import process_input


def vecstore(input_type, input_data):
      texts=process_input(input_type, input_data)
      sample_embedding = np.array(hf_embeddings.embed_query("sample text"))
      dimension = sample_embedding.shape[0]
      index = faiss.IndexFlatL2(dimension)
          
      vector_store = FAISS(
              embedding_function=hf_embeddings.embed_query,
              index=index,
              docstore=InMemoryDocstore(),
              index_to_docstore_id={},
          )
      vector_store.add_texts(texts)

      return vector_store