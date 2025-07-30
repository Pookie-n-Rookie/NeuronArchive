# NeuronArchive 🧠

Neuron Archive is an intelligent document Q&A assistant built with Streamlit that allows users to interact with their documents through natural language queries using Retrieval Augmented Generation (RAG).

## How It Works 🔍

Neuron Archive uses RAG (Retrieval Augmented Generation) architecture to provide accurate answers from your documents:

1. **Document Processing:**
   - Documents are split into smaller chunks
   - Each chunk is converted into a vector embedding using sentence transformers
   - These embeddings are stored in a FAISS vector database for efficient retrieval

2. **Question Answering:**
   - When you ask a question, it's also converted into a vector embedding
   - The system finds the most relevant document chunks using similarity search
   - These chunks are sent to *llama-3.3-70b-versatile* along with your question
   - *llama-3.3-70b-versatile* generates a contextual answer based on the retrieved information

This approach ensures answers are grounded in your documents' actual content, reducing hallucinations and providing accurate responses.

## Features 📋

- **Multiple Document Format Support:**
  - PDF files
  - DOCX files
  - TXT files
  - Plain text input
  - Web links

- **User-Friendly Interface:**
  - Clean and intuitive Streamlit UI
  - Real-time document processing
  - Interactive Q&A interface
  - History tracking of previous questions and answers

## Getting Started 🚀

1. Clone the repository:
```bash
git clone https://github.com/Pookie-n-Rookie/NeuronArchive.git
cd NeuronArchive
```

2. Set up a Python virtual environment:
```bash
# Using venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your HuggingFace API key:
```
GROQ_API_KEY=your-api-key-here
```

5. Start the application:
```bash
streamlit run rag.py
```

## Test
1.For docx file
<img width="1789" height="873" alt="image" src="https://github.com/user-attachments/assets/b2b97e88-4982-485b-84c6-bd900cf92a09" />


2.For pdf file
<img width="1874" height="889" alt="image" src="https://github.com/user-attachments/assets/aa4516ef-5631-4ba4-b0cf-f972d278d7a6" />


3.For any link
<img width="1914" height="885" alt="image" src="https://github.com/user-attachments/assets/79016d2d-0c83-43e6-b616-9c05cfd42b51" />


4.For any txt file
<img width="1904" height="888" alt="image" src="https://github.com/user-attachments/assets/cd0328f2-fb5b-4031-808d-892f6ca04666" />


5.For any random text inserted in the input text box
<img width="1839" height="802" alt="image" src="https://github.com/user-attachments/assets/c087d076-9215-475e-87d7-5f84ad75a7b2" />


## Usage 💡

1. Select your input type from the dropdown menu (Text, PDF, DOCX, TXT, or Link)
2. Upload or input your document
3. Click "Process Document" to analyze the content
4. Ask questions about your document in the text input field
5. View answers and previous Q&A history in the expandable sections

## Acknowledgments 🙏

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://langchain.readthedocs.io/)
- Uses [GroqCloud]((https://console.groq.com/home)) for model  and [FAISS](https://github.com/facebookresearch/faiss) for vector search
- Language model: [llama-3.3-70b-versatile]((https://console.groq.com/docs/model/llama-3.3-70b-versatile)) 
