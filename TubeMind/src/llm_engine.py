import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain

def get_qa_chain(vector_db):
    # ADDED: max_retries handles the 429 error automatically
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite", 
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        max_retries=6, 
        timeout=60
    )
    
    system_prompt = (
        "You are a helpful assistant. Use the following transcript "
        "to answer the user's question.\n\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(vector_db.as_retriever(), question_answer_chain)