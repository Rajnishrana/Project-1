from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def create_vector_store(chunks):
    """Turns text chunks into mathematical vectors and stores them."""
    # This model runs on your CPU for FREE. No API key needed.
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    
    # Create the FAISS index (your local searchable database)
    vector_db = FAISS.from_documents(chunks, embeddings)
    return vector_db