import streamlit as st
from answers import answer_question
from embed_vec_store import vecstore

def main():
    st.set_page_config(page_title="Document Q&A Assistant", layout="wide")
    
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .css-1d391kg {
        padding: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("📚 Document Q&A Assistant")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Document Input")
        input_type = st.selectbox("Select Input Type", 
                                ["Text", "PDF", "DOCX", "TXT", "Link"],
                                help="Choose the type of document you want to analyze")
        
        if input_type == "Link":
            number_input = st.number_input("Number of Links", 
                                         min_value=1, max_value=20, 
                                         step=1,
                                         help="Enter how many URLs you want to analyze")
            input_data = []
            for i in range(number_input):
                url = st.text_input(f"URL {i+1}", 
                                  help="Enter the complete URL including http:// or https://")
                input_data.append(url)
        elif input_type == "Text":
            input_data = st.text_area("Enter your text", 
                                    height=200,
                                    help="Paste or type your text here")
        else:
            input_data = st.file_uploader(f"Upload {input_type} file", 
                                        type=[input_type.lower()],
                                        help=f"Upload your {input_type} document")

        if st.button("Process Document", type="primary"):
            try:
                vectorstore = vecstore(input_type, input_data)
                st.session_state["vectorstore"] = vectorstore
                st.success("Document processed successfully!")
            except Exception as e:
                st.error(f"Error processing document: {str(e)}")

    with col2:
        st.subheader("Ask Questions")
        if "vectorstore" in st.session_state:
            query = st.text_input("What would you like to know about your document?",
                                help="Ask any question about the content of your document")
            
            if st.button("Get Answer", type="primary"):
                try:
                    answer = answer_question(st.session_state["vectorstore"], query)
                    st.markdown("### Answer")
                    st.markdown(answer["result"])
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
        else:
            st.info("Please process a document first before asking questions.")

        if "answers" in st.session_state:
            st.markdown("### Previous Questions & Answers")
            for q, a in st.session_state["answers"]:
                with st.expander(q):
                    st.write(a)

if __name__ == "__main__":
    main()