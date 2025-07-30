## rag.py
import streamlit as st
from answers import answer_question
from embed_vec_store import vecstore
import os

# Set USER_AGENT to avoid warnings
os.environ['USER_AGENT'] = 'Neuron Archive RAG App'

def process_query(query, vectorstore):
    """Process the user query and return the answer"""
    try:
        with st.spinner("🤖 Generating answer..."):
            answer = answer_question(vectorstore, query)
            return answer["result"]
    except Exception as e:
        st.error(f"Error generating answer: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="Neuron Archive",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for chat-like interface
    st.markdown("""
    <style>
    /* Global styles */
    body {
        background-color: #FFA421;
        color: #FFFFFF;
    }
    
    .main {
        background-color: #FFFFFF;
        padding: 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1E1E1E;
        padding: 2rem 1rem;
    }
    
    /* Chat container styling */
    .chat-container {
        background-color: #000000;
        height: 100vh;
        padding: 1rem;
        overflow-y: auto;
    }
    
    /* Message bubbles */
    .user-message {
        background-color: #2C2C2C;
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 5px 15px;
        margin: 1rem 0;
        max-width: 80%;
        float: right;
        clear: both;
        word-wrap: break-word;
    }
    
    .assistant-message {
        background-color: #FFFF00;
        color: black;
        padding: 1rem;
        border-radius: 15px 15px 15px 5px;
        margin: 1rem 0;
        max-width: 80%;
        float: left;
        clear: both;
        word-wrap: break-word;
    }
    
    /* Input area container */
    .input-area {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        position: relative;
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        background-color: #FFFFFF;
        color: #0000FF;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        height: 45px;
        margin: 0;
    }
    
    /* Remove default Streamlit input container padding */
    .stTextInput>div {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        height: 45px;
        padding: 0 1.5rem;
        border: none;
        font-weight: 600;
        margin: 0;
        line-height: 45px;
        width: 100%;
    }
    
    /* Remove default Streamlit button container padding */
    .stButton {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* File uploader */
    .uploadedFile {
        background-color: #2C2C2C;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Column adjustments */
    .input-area .stColumn {
        padding: 0 !important;
    }
    
    /* Remove all default streamlit element margins */
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Clear fix for floating elements */
    .clearfix::after {
        content: "";
        display: table;
        clear: both;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check for Groq API key
    groq_api_key = os.getenv('GROQ_API_KEY')
    if not groq_api_key:
        st.error("⚠️ GROQ_API_KEY not found in environment variables. Please add it to your .env file.")
        st.stop()
    
    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar for document upload
    with st.sidebar:
        st.title("📄 Upload your doc here")
        st.caption("Powered by Groq & llama-3.3-70b-versatile")
        
        input_type = st.selectbox(
            "Document Type",
            ["Text", "PDF", "DOCX", "TXT", "Link"],
            help="Select your document format"
        )
        
        if input_type == "Link":
            number_input = st.number_input(
                "Number of Links",
                min_value=1,
                max_value=2,
                step=1
            )
            input_data = []
            for i in range(number_input):
                url = st.text_input(
                    f"URL {i+1}",
                    key=f"url_{i}",
                    placeholder="https://example.com"
                )
                if url:  # Only add non-empty URLs
                    input_data.append(url)
        elif input_type == "Text":
            input_data = st.text_area(
                "Document Text",
                height=200,
                placeholder="Paste or type your content here..."
            )
        else:
            input_data = st.file_uploader(
                f"Upload {input_type}",
                type=[input_type.lower()]
            )
        
        if st.button("Process Document", type="primary"):
            if input_type == "Link" and not input_data:
                st.error("❌ Please enter at least one URL")
            elif input_type == "Text" and not input_data:
                st.error("❌ Please enter some text")
            elif input_type in ["PDF", "DOCX", "TXT"] and not input_data:
                st.error(f"❌ Please upload a {input_type} file")
            else:
                with st.spinner("Processing document..."):
                    try:
                        vectorstore_result = vecstore(input_type, input_data)
                        st.session_state.vectorstore = vectorstore_result
                        st.success("✅ Document processed successfully!")
                        # Clear previous chat history when new document is processed
                        st.session_state.chat_history = []
                    except Exception as e:
                        st.error(f"❌ Error processing document: {str(e)}")
        
        # Show document status
        if "vectorstore" in st.session_state:
            st.success("📚 Document ready for Q&A")
        else:
            st.info("📝 No document loaded")
    
    # Main chat interface
    st.title("📚 Document Q&A Assistant")
    st.caption("Ask questions about your uploaded documents")
    
    # Display chat history
    if st.session_state.chat_history:
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            st.markdown(f"""
                <div class="clearfix">
                    <div class="user-message">{question}</div>
                    <div class="assistant-message">{answer}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # Chat input using form to avoid session state issues
    if "vectorstore" in st.session_state:
        # Use form to handle input properly
        with st.form(key="chat_form", clear_on_submit=True):
            col1, col2 = st.columns([5, 1])
            
            with col1:
                user_query = st.text_input(
                    label="Ask a question",
                    placeholder="Ask a question about your document...",
                    label_visibility="hidden"
                )
            
            with col2:
                submitted = st.form_submit_button("Send", type="primary", use_container_width=True)
            
            # Process the query when form is submitted
            if submitted and user_query.strip():
                # Get answer
                answer = process_query(user_query.strip(), st.session_state.vectorstore)
                
                if answer:
                    # Add to chat history
                    st.session_state.chat_history.append((user_query.strip(), answer))
                    # Rerun to show the new message
                    st.rerun()
    
    else:
        st.info("👈 Please upload and process a document to start chatting")
        
        # Show example questions
        st.markdown("### 💡 Example Questions:")
        st.markdown("""
        - What is the main topic of this document?
        - Can you summarize the key points?
        - What are the important dates mentioned?
        - Who are the main people discussed?
        - What conclusions can be drawn?
        """)

if __name__ == "__main__":
    main()