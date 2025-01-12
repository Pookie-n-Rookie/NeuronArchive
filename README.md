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
   - These chunks are sent to Mistral-7B-Instruct along with your question
   - Mistral-7B-Instruct generates a contextual answer based on the retrieved information

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
HUGGING_FACE_API_KEY=your-api-key-here
```

5. Start the application:
```bash
streamlit run rag.py
```

## Usage 💡

1. Select your input type from the dropdown menu (Text, PDF, DOCX, TXT, or Link)
2. Upload or input your document
3. Click "Process Document" to analyze the content
4. Ask questions about your document in the text input field
5. View answers and previous Q&A history in the expandable sections

## Acknowledgments 🙏

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://langchain.readthedocs.io/)
- Uses [HuggingFace](https://huggingface.co/) models and [FAISS](https://github.com/facebookresearch/faiss) for vector search
- Language model: [Mistral-7B-Instruct-v0.2](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)
