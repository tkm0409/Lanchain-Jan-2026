# RAG Part 2: Embeddings & Vector Stores

## Concept Overview
An **Embedding** represents the "semantic meaning" of text.
"Dog" and "Puppy" will have vectors that are very close together in multi-dimensional space, even though the words share no letters.

**Chroma** is a fantastic open-source vector store that runs locally (in-memory or on-disk). For production, you might use **Pinecone**, **Weaviate**, or **pgvector** (Postgres).

## Code Breakdown (`02_embeddings_vector_stores.py`)

### 1. `similarity_search`
This performs a "Nearest Neighbor" search. Ideally, it finds the chunk with the highest cosine similarity to the query.

### 2. Metadata Filtering
We didn't show it in the code, but you can pass `filter={"source": "history"}` to `similarity_search`. This is crucial. If a user asks "What did I say yesterday?", you MUST filter by `date=yesterday` first, otherwise you search the entire universe.

## Real-World Interview Questions (War Stories)

### Q1: "We have 10 million vectors in Pinecone. It's getting expensive ($3000/mo). How do we cut costs?"
**Real World Answer**:
"I migrated the archive data (stuff older than 1 year) to **pgvector** (Postgres) on standard disk storage.
We kept the 'Hot' data (last 3 months) in Pinecone/Redis for low-latency search.
We implemented a 'Hybrid Router': check Hot Store first; if confidence is low, check Cold Store. Saved 80% on bills."

### Q2: "We changed our Embedding Model from OpenAI-Ada-002 to OpenAI-Small-3. Now search returns garbage."
**Real World Answer**:
"Code Red. Vectors from different models live in different geometric spaces.
**The Fix**:
You cannot 'convert' vectors. You must **Re-Index**.
I wrote a script to:
1. Iterate through the database and fetch the *Source Text* (metadata).
2. Re-embed the text with the new v3 model.
3. Upsert to a *new* collection.
*Lesson*: Always store the raw text in metadata or a separate SQL DB, otherwise you are locked into your embedding provider forever."

## Topics Excluded
*   **Fine-tuning Embeddings**: You can train a custom embedding model (SentenceTransformers) on your specific domain data (e.g., Medical Records).
*   **Quantization**: Compressing vectors (float32 -> int8) to save RAM.
