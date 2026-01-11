from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_core.documents import Document
from dotenv import load_dotenv
import logging

load_dotenv()

# --- Concept: Improving Retrieval ---
# Standard Similarity Search is often "dumb". 
# If user asks "What is the capital of the moon?", standard search might return "The capital of France is Paris" if the vectors align loosely.
# We need smarter retrieval.

def demonstrate_advanced_retrieval():
    # Setup Data
    docs = [
        Document(content="The capital of France is Paris. It is known for the Eiffel Tower."),
        Document(content="The capital of Italy is Rome. It is known for the Colosseum."),
        Document(content="The capital of Spain is Madrid."),
        Document(content="Paris is a great city for fashion and art."),
    ]
    vector_store = Chroma.from_documents(docs, OpenAIEmbeddings(), collection_name="adv_retrieval")
    model = ChatOpenAI(temperature=0)

    # --- Strategy 1: Multi-Query Retriever ---
    # Problem: Users write bad queries. "france city tower"
    # Solution: Use an LLM to generate 3 different variations of the query, search for ALL of them, and take the union of results.
    print("--- 1. Multi-Query Retriever ---")
    
    # We turn on logging to SEE the generated queries
    logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)
    
    retriever_mq = MultiQueryRetriever.from_llm(
        retriever=vector_store.as_retriever(), 
        llm=model
    )
    
    # User asks vague question
    results = retriever_mq.invoke("tell me about the french big city")
    print(f"MQ Found {len(results)} docs.")
    for d in results:
        print(f"- {d.page_content}")

    # --- Strategy 2: Contextual Compression ---
    # Problem: You retrieve a 2000 token document, but the answer is only 1 sentence in the middle.
    # Solution: Use an LLM to "compress" the retrieved document to ONLY contain relevant info before passing it to the final QA chain.
    print("\n--- 2. Contextual Compression ---")
    
    compressor = LLMChainExtractor.from_llm(model)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=vector_store.as_retriever()
    )
    
    compressed_docs = compression_retriever.invoke("What is France known for?")
    print(f"Compressed Found {len(compressed_docs)} docs.")
    for d in compressed_docs:
        print(f"Original Length: {len(docs[0].page_content)}")
        print(f"Compressed Content: {d.page_content}")

    # Cleanup
    vector_store.delete_collection()

if __name__ == "__main__":
    demonstrate_advanced_retrieval()
