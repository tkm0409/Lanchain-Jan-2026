import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

load_dotenv()

# ==========================================
# CONCEPT: Vector Store Router
# Dynamically choosing where to save/search based on User Tier.
# Free User -> Local Disk (Chroma)
# Pro User -> Cloud (Pinecone/Weaviate) - Simulated here
# ==========================================

print("--- Lesson 4: Vector Store Router ---")

class VectorStoreRouter:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        # Tier 1: Local
        self.local_db = Chroma(collection_name="free_tier", embedding_function=self.embeddings)
        # Tier 2: Cloud (MockedDict for demo, replace with Pinecone in prod)
        self.cloud_db_mock = {}

    def ingest(self, doc: Document, user_tier: str):
        print(f"Ingesting doc for {user_tier} user...")
        if user_tier == "free":
            self.local_db.add_documents([doc])
            print(" -> Saved to Local ChromaDB")
        elif user_tier == "pro":
            # self.pinecone.upsert(...)
            self.cloud_db_mock["doc_id"] = doc.page_content
            print(" -> Saved to Cloud High-Performance DB")
        else:
            raise ValueError("Unknown Tier")

    def search(self, query: str, user_tier: str):
        print(f"Searching for {user_tier} user...")
        if user_tier == "free":
            return self.local_db.similarity_search(query, k=1)
        elif user_tier == "pro":
            return [Document(page_content="Cloud Result: Fast & Scalable")]

# Run
router = VectorStoreRouter()
doc = Document(page_content="The user is on the free plan.")

# 1. Ingest
router.ingest(doc, "free")
router.ingest(Document(page_content="Premium content"), "pro")

# 2. Search
res_free = router.search("plan", "free")
print(f"Free Search Result: {res_free[0].page_content}")

res_pro = router.search("plan", "pro")
print(f"Pro Search Result: {res_pro[0].page_content}")

# Clean
# self.local_db.delete_collection()
print("\n[System] Router Pattern enables Multi-Tenant RAG at scale.")
