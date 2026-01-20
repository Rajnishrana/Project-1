from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text):
    """Breaks long text into chunks that fit in the AI's memory."""
    # chunk_size is the number of characters per piece
    # chunk_overlap ensures no context is lost between pieces
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.create_documents([text])
    return chunks