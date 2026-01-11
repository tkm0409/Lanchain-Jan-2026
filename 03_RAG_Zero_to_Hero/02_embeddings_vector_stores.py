import shutil
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# --- Concept: Vector Stores ---
# The "Brain" of RAG.
# 1. EMBED: Turn text into a vector (list of float numbers).
# 2. STORE: Save vectors in a database (Chroma, Pinecone, FAISS).
# 3. RETRIEVE: Find vectors closest to the query vector.

def demonstrate_vector_store():
    # 1. The Data
    documents = [
        Document(page_content="LangChain was launched in October 2022 by Harrison Chase.", metadata={"source": "history"}),
        Document(page_content="LangGraph allows creating cyclic agentic workflows.", metadata={"source": "features"}),
        Document(page_content="Apples are a type of fruit that grow on trees.", metadata={"source": "general_knowledge"}),
    ]

    # 2. The Embedding Model
    # This turns text into numbers. "King" - "Man" + "Woman" ~ "Queen"
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # 3. The Vector Store (Chroma)
    print("--- 1. Creating Index ---")
    # We use a distinct collection name to avoid conflicts
    # in-memory mode for valid tutorial usage (persist_directory can be added for disk storage)
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="tutorial_collection"
    )

    # 4. Retrieval (The Query)
    query = "Who created LangChain?"
    print(f"\n--- 2. Querying: '{query}' ---")
    
    # search_type="similarity" is standard KNN (K-Nearest Neighbors)
    results = vector_store.similarity_search(query, k=1)
    
    for doc in results:
        print(f"Found Doc: {doc.page_content}")
        print(f"Metadata: {doc.metadata}")

    # 5. Search with Scores (Euclidean Distance or Cosine Similarity)
    print("\n--- 3. Querying with Scores ---")
    results_with_score = vector_store.similarity_search_with_score("fruit", k=1)
    for doc, score in results_with_score:
        print(f"Content: {doc.page_content}")
        # Note: In Chroma, lower score is usually 'closer' distance (depending on metric).
        print(f"Distance Score: {score}")

    # Cleanup
    vector_store.delete_collection()

if __name__ == "__main__":
    demonstrate_vector_store()
