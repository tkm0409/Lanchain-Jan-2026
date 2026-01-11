# Module 3 Tasks: RAG Zero to Hero

## Challenge 1: The "Messy PDF" Ingestor
**Goal**: Load a messy PDF and clean it up before indexing.
- **Steps**:
    1. Use `PyPDFLoader` to load a PDF.
    2. Write a function `clean_text(docs)` that removes headers/footers (regex: `Page \d+ of \d+`).
    3. Split the cleaned text using `RecursiveCharacterTextSplitter`.
    4. Print the stats: "Original: 50 pages. Split into: 200 chunks."

## Challenge 2: The "Hybrid" Retriever
**Goal**: Manually implement Hybrid Search (Vector + Keyword) without using Pinecone's native hybrid.
- **Steps**:
    1. Create a `BM25Retriever` (Keyword search) from documents.
    2. Create a `Chroma` retriever (Vector search) from the same documents.
    3. Use `EnsembleRetriever(retrievers=[bm25, chroma], weights=[0.5, 0.5])`.
    4. Query: "features of LangGraph" and see if the results differ from pure vector search.

## Challenge 3: The "Re-ranker" Simulation
**Goal**: Simulate a re-ranking step using an LLM.
- **Steps**:
    1. Retrieve 10 documents for a query.
    2. Pass them to `gpt-3.5-turbo` with a prompt: *"Rank these 10 chunks by relevance to the query '{query}'. Return only the IDs of the top 3."*
    3. Print the top 3 chosen by the LLM.
    - **Why?**: This mimics what Cohere Rerank does, but slower. It teaches you the *concept* of two-stage retrieval.
