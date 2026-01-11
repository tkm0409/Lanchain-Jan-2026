# RAG Part 1: Loaders & Splitters

## Concept Overview
**Garbage In, Garbage Out.**
If you just dump a PDF into a vector store without cleaning or proper splitting, your RAG system will fail.

**RecursiveCharacterTextSplitter** is the default because it respects the natural structure of text (paragraphs -> sentences).
**SemanticChunker** is the future. It calculates the cosine similarity between sentences and creates a break only when the topic shifts.

## Code Breakdown (`01_loaders_splitters.py`)

### 1. `chunk_overlap`
```python
chunk_overlap=200
```
**CRITICAL**: Never set this to 0.
LLMs need context. If a sentence is cut in half, the meaning is lost. Overlap ensures the end of chunk A and the start of chunk B share context, so the retriever can find either.

### 2. `WebBaseLoader` & `bs_kwargs`
We used `bs_kwargs` (BeautifulSoup arguments) to specifically target the `post-content` div.
*Pro-Tip*: In production, parsing HTML is messy. 80% of RAG engineering is writing custom parsing logic to strip navbars, ads, and footers.

## Real-World Interview Questions (War Stories)

### Q1: "We ingest 100 HTML pages. The splitter breaks the code blocks in the middle. The LLM can't understand the code snippets. Fix it."
**Real World Answer**:
"Generic splitters are bad for code.
**The Fix**:
I switched to `CodeTextSplitter.from_language(Language.PYTHON)`.
It understands `def` and `class` indentation and ensures it chunks *around* the logical blocks, not through them.
For HTML, I used `HTMLHeaderTextSplitter` first to break by `<h1>`/`<h2>`, preserving the semantic hierarchy."

### Q2: "We are building an RAG system for a Law Firm. They have 500-page contracts. Similarity search is failing."
**Real World Answer**:
"500 pages is too big for dense vectors. The 'Needle' gets lost.
** The Fix (Parent Document Retrieval)**:
I treated the document as a hierarchy.
1. I split the document into 50-page 'Chapters' (Parents).
2. I split chapters into 500-token 'Chunks' (Children).
3. I indexed the Children embeddings.
4. When a child is retrieved, I return the *Parent* (Chapter) to the LLM.
This gives the LLM enough context to answer complex legal questions without polluting the vector index with huge blobs."

## Topics Excluded
*   **Unstructured API (Hosted)**: We used local loaders. In enterprise, you often pay Unstructured.io to parse complex Tables/Images from PDFs.
*   **OCR**: We didn't cover Tesseract or Azure Document Intelligence for scanned PDFs.
