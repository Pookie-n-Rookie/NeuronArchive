import streamlit as st
from answers import answer_question
from embed_vec_store import vecstore

def handle_enter():
    if "vectorstore" in st.session_state and st.session_state.query:
        try:
            answer = answer_question(st.session_state.vectorstore, st.session_state.query)
            if "answers" not in st.session_state:
                st.session_state.answers = []
            st.session_state.answers.insert(0, (st.session_state.query, answer["result"]))
            st.session_state.query = ""
        except Exception as e:
            st.error(f"Error generating answer: {str(e)}")

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
    }
    
    .assistant-message {
        background-color: #FFF00;
        color: black;
        padding: 1rem;
        border-radius: 15px 15px 15px 5px;
        margin: 1rem 0;
        max-width: 80%;
        float: left;
        clear: both;
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
        border-radius: 20px;
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
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar for document upload
    with st.sidebar:
        st.title("📄 Upload your doc here")
        
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
            with st.spinner("Processing..."):
                try:
                    vectorstore = vecstore(input_type, input_data)
                    st.session_state.vectorstore = vectorstore
                    st.success("✅ Document processed!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Main chat interface
    st.title("📚 A Document Q&A Assistant")
    
    # Display chat history
    if "answers" in st.session_state and st.session_state.answers:
        for q, a in reversed(st.session_state.answers):
            st.markdown(f"""
                <div class="user-message">{q}</div>
                <div class="assistant-message">{a}</div>
            """, unsafe_allow_html=True)
    
    # Chat input
    if "vectorstore" in st.session_state:
        if "query" not in st.session_state:
            st.session_state.query = ""
        
        # Fixed container at the bottom
        with st.container():
            st.markdown('<div class="input-area">', unsafe_allow_html=True)
            col1, col2 = st.columns([6, 1])
            with col1:
                query = st.text_input(
                    "",
                    key="query",
                    placeholder="Ask a question...",
                    on_change=handle_enter
                )
            with col2:
                if st.button("Send", type="primary"):
                    handle_enter()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👈 Please upload and process a document to start chatting")

if __name__ == "__main__":
    main()