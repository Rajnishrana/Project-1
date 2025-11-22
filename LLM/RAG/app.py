import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Load environment variables
load_dotenv()

# Initialize local embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Chroma client with persistence
chroma_client = chromadb.PersistentClient(path="chroma_persistent_storage")
collection_name = "document_qa_collection"
collection = chroma_client.get_or_create_collection(name=collection_name)

# Load documents from a directory
def load_documents_from_directory(directory_path):
    print("==== Loading documents from directory ====")
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path, filename), "r", encoding="utf-8") as file:
                documents.append({"id": filename, "text": file.read()})
    return documents

# Split text into chunks
def split_text(text, chunk_size=1000, chunk_overlap=20):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks

# Generate embeddings locally
def get_local_embedding(text):
    embedding = embedding_model.encode(text)
    print("==== Generating embedding... ====")
    return embedding

# Insert documents into Chroma
def insert_documents(directory_path):
    documents = load_documents_from_directory(directory_path)
    chunked_documents = []
    for doc in documents:
        chunks = split_text(doc["text"])
        print(f"==== Splitting {doc['id']} into chunks ====")
        for i, chunk in enumerate(chunks):
            chunked_documents.append({"id": f"{doc['id']}_chunk{i+1}", "text": chunk})

    for doc in chunked_documents:
        doc["embedding"] = get_local_embedding(doc["text"])

    for doc in chunked_documents:
        print(f"==== Inserting {doc['id']} into DB ====")
        collection.upsert(ids=[doc["id"]], documents=[doc["text"]], embeddings=[doc["embedding"]])

# Query documents
def query_documents(question, n_results=3):
    query_embedding = get_local_embedding(question)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]
    print("==== Returning relevant chunks ====")
    return relevant_chunks

# Initialize GPT-2 for answer generation
tokenizer = AutoTokenizer.from_pretrained("gpt2")
gen_model = AutoModelForCausalLM.from_pretrained("gpt2")
generator = pipeline("text-generation", model=gen_model, tokenizer=tokenizer, max_new_tokens=200)

# Generate answer from retrieved chunks
def generate_answer(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = f"Answer the question based on the context below:\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    result = generator(prompt)[0]["generated_text"]
    return result

# Example usage
directory_path = "./articles"
# Uncomment the next line if you haven't inserted documents yet
# insert_documents(directory_path)

question = "tell me about "
relevant_chunks = query_documents(question)
answer = generate_answer(question, relevant_chunks)
print("\n==== GENERATED ANSWER ====\n")
print(answer)
