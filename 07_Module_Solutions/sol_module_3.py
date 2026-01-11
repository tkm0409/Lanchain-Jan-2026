import os
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.retrievers import EnsembleRetriever

load_dotenv()

# ==========================================
# Challenge 1: The "Messy PDF" Ingestor (ETL)
# ==========================================
print("--- Challenge 1: PDF Cleanup ---")

# Mocking a document since we don't have a PDF file handy.
# Real world: loader = PyPDFLoader("myfile.pdf"); docs = loader.load()
raw_text = """
Page 1 of 50
Header: Confidential
The contract states that...
Footer: v1.0

Page 2 of 50
Header: Confidential
...the party of the first part shall pay...
"""
docs = [Document(page_content=raw_text, metadata={"source": "dummy.pdf"})]

def clean_text(docs):
    cleaned_docs = []
    for d in docs:
        text = d.page_content
        # Regex to remove Headers/Footers
        text = re.sub(r"Page \d+ of \d+", "", text) 
        text = re.sub(r"Header: .*\n", "", text)
        text = re.sub(r"Footer: .*", "", text)
        cleaned_docs.append(Document(page_content=text.strip(), metadata=d.metadata))
    return cleaned_docs

cleaned = clean_text(docs)
splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=0)
splits = splitter.split_documents(cleaned)

print(f"Original Length: {len(raw_text)}")
print(f"Cleaned Length: {len(cleaned[0].page_content)}")
print(f"Split into {len(splits)} chunks.")
print(f"Sample Chunk: '{splits[0].page_content}'")


# ==========================================
# Challenge 2: The "Hybrid" Retriever
# ==========================================
print("\n--- Challenge 2: Hybrid Search ---")

# Dataset
texts = [
    "LangChain is a framework for LLMs.",
    "Apples are red fruits.",
    "LangGraph is for agentic workflows.",
    "Bananas are yellow."
]
docs = [Document(page_content=t) for t in texts]

# 1. Keyword Retriever (Sparse)
bm25_retriever = BM25Retriever.from_documents(docs)
bm25_retriever.k = 2

# 2. Vector Retriever (Dense)
vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())
chroma_retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 3. Ensemble (Hybrid)
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, chroma_retriever],
    weights=[0.5, 0.5] # Equal weight
)

query = "LangChain framework"
results = ensemble_retriever.invoke(query)

print(f"Query: {query}")
for i, doc in enumerate(results):
    print(f"{i+1}. {doc.page_content}")

# Cleanup
vectorstore.delete_collection()
