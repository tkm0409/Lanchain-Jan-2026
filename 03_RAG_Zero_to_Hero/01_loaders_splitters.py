import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# --- Concept: ETL for LLMs ---
# RAG starts with data.
# 1. LOAD: Raw files -> LangChain Documents
# 2. SPLIT: Large Documents -> Small Chunks

def demonstrate_loading_and_splitting():
    # --- 1. LOADER ---
    # We will load a blog post from the web.
    # WebBaseLoader uses BeautifulSoup under the hood.
    print("--- 1. Loading Document ---")
    loader = WebBaseLoader(
        web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} document(s).")
    print(f"First doc length: {len(docs[0].page_content)} characters.")

    # --- 2. SPLITTING (The most critical step) ---
    # Why split? 
    # a) Context Window limits.
    # b) Retrieval precision (finding a needle in a haystack).
    
    # Strategy A: RecursiveCharacterTextSplitter (The Gold Standard)
    # Tries to split on paragraphs (\n\n), then sentences (\n), then words ( ).
    print("\n--- 2. Recursive Splitting ---")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200, # Crucial: Keeps context between chunks
        add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)
    print(f"Split into {len(all_splits)} chunks.")
    print(f"Sample Chunk:\n{all_splits[0].page_content[:200]}...")

    # Strategy B: Semantic Splitting (The Advanced Way)
    # Instead of arbitrary char counts, it splits when the "meaning" changes.
    # Requires an Embedding Model!
    print("\n--- 3. Semantic Splitting ---")
    try:
        semantic_splitter = SemanticChunker(OpenAIEmbeddings())
        semantic_splits = semantic_splitter.split_documents(docs)
        print(f"Semantically split into {len(semantic_splits)} chunks.")
        # Semantic usage creates fewer, more meaningful chunks usually.
    except Exception as e:
        print(f"Skipping Semantic Splitting (requires valid OpenAI Key): {e}")

if __name__ == "__main__":
    demonstrate_loading_and_splitting()
