# RAG Part 3: Advanced Retrieval

## Concept Overview
Getting data into the Vector DB is easy. Getting the *right* data out is hard.
Users engage in "Keyword Search" behavior even when talking to Semantic models.
**MultiQueryRetriever** helps bridge the gap between what the user *said* and what they *meant*.

## Code Breakdown (`03_advanced_retrieval.py`)

### 1. `MultiQueryRetriever`
It uses an LLM to generate variations.
Input: "french big city"
Generated:
1. "What is the largest city in France?"
2. "Major urban areas in France descriptions"
3. "Capital of France tourism"
It executes ALL 3 searches and deduplicates the results. This increases **Recall** (finding things you might have missed).

### 2. `ContextualCompression`
This increases **Precision** (filtering out noise).
It effectively runs a mini-summarization task on every retrieved document.
*Warning*: It adds latency (requires an LLM call per retrieved doc).

## Real-World Interview Questions (War Stories)

### Q1: "MultiQueryRetriever is generating 3 queries, so our cost and latency tripled. Is it worth it?"
**Real World Answer**:
"In our tests, MQ improved Recall by 20% but added 1.5s latency.
**The Fix**: We made it **Asynchronous**.
Instead of running queries sequentially, we used `asyncio.gather` for the 3 vector searches.
Also, we realized we only needed MQ for *short* queries (1-3 words). For long queries, we skipped MQ and just did a standard search."

### Q2: "The Contextual Compressor is cutting out the actual answer because it didn't look 'relevant' to the model."
**Real World Answer**:
"Compressors are aggressive.
**The Fix**:
We switched to **Cohere's Re-ranker** instead of an LLM-based compressor.
Re-ranking re-orders the docs but keeps the text intact. It's faster and less prone to accidentally deleting the answer. Compression is risky for legal/financial apps."

## Topics Excluded
*   **GraphRAG**: Using Knowledge Graphs (Neo4j) to enhance retrieval.
*   **RAPTOR**: Recursive Tree summarization for global context questions.
