import streamlit as st
from dotenv import load_dotenv
from src.scraper import extract_video_id, get_transcript
from src.processor import split_text
from src.database import create_vector_store
from src.llm_engine import get_qa_chain

# Load environment variables (API Keys)
load_dotenv()

# --- Page Config ---
st.set_page_config(page_title="TubeMind", page_icon="🎥")
st.title("🎥 TubeMind: Chat with YouTube")
st.markdown("Paste a YouTube link below to start a conversation with the video content.")

# --- Sidebar/Settings ---
with st.sidebar:
    st.header("Status")
    if "chain" in st.session_state:
        st.success(" Video Processed")
    else:
        st.info("Awaiting Video")

# --- Video Processing ---
url = st.text_input("YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Process Video"):
    v_id = extract_video_id(url)
    if v_id:
        with st.spinner("Watching the video and taking notes..."):
            raw_text = get_transcript(v_id)
            if raw_text:
                chunks = split_text(raw_text)
                vector_db = create_vector_store(chunks)
                st.session_state.chain = get_qa_chain(vector_db)
                st.success("I'm ready! Ask me anything about the video.")
            else:
                st.error("I couldn't find a transcript for this video. Captions might be disabled.")
    else:
        st.error("That link doesn't look right. Please check the URL.")

# --- Chat Interface ---
if "chain" in st.session_state:
    st.divider()
    user_q = st.text_input("Ask a question about the video content:")
    
    if user_q:
        with st.spinner("Thinking..."):
            # UPDATED: The modern chain expects a dictionary with an 'input' key
            response = st.session_state.chain.invoke({"input": user_q})
            
            st.markdown("### Answer:")
            # UPDATED: The modern chain returns the result in an 'answer' key
            st.info(response["answer"])
            
            # Optional: Show the context used to answer (for transparency)
            with st.expander("See Source Material"):
                for i, doc in enumerate(response["context"]):
                    st.write(f"**Source {i+1}:** {doc.page_content[:200]}...")