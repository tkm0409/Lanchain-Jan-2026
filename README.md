# LangChain Enterprise Curriculum (2025-2026 Edition)

> **Manifesto**: This repository is not a "Hello World" tutorial. It is a **flight simulator** for Senior AI Engineers. It focuses on the patterns, failures, and architectural decisions required to put Large Language Models into production.

## 📚 Curriculum Overview

We have built a modular, code-first curriculum designed to take you from "Prompt Engineering" to "Agentic Orchestration".

| Module | Core Concepts | Industry Focus (The "Why") |
| :--- | :--- | :--- |
| **01. Foundations** | Polyglot Models, Structured Output, Pydantic | **Vendor Lock-in**: How to switch from OpenAI to Anthropic in 1 line of code to save costs. |
| **02. LCEL Engine** | Runnables, Parallelism, Fallbacks, Streaming | **Latency**: How to run 5 chains in parallel and stream tokens to the UI instantly. |
| **03. RAG Zero-to-Hero** | Hybrid Search, Re-ranking, Parent Document Retrieval | **Accuracy**: Why "Vector Search" isn't enough for Enterprise Knowledge Bases. |
| **04. Memory & State** | Windowing, Summarization, Redis/File Persistence | **Scaling**: Managing infinite chat history without blowing up the context window. |
| **05. Agents & Tools** | Tool Definition, Loop Control, Error Handling | **Reliability**: Stopping agents from getting stuck in "Death Spirals" or hallucinating inputs. |
| **06. Production** | RAGAS Evaluation, LangSmith Tracing, CI/CD | **Trust**: How to prove to your boss that the bot is safe to deploy. |

---

## 🛠️ The "Excluded" Topics (What's Next?)
To keep this curriculum focused on *Application Engineering*, we explicitly excluded these deep-dive topics. You should study these independently:

1.  **Fine-Tuning (PeFT/LoRA)**: We focused on RAG. Fine-tuning models (like Llama-3-70b) on custom datasets is a separate skillset involving PyTorch/HuggingFace.
2.  **Infrastructure / Deployment**: We ran everything locally. Real production requires `vLLM` or `TGI` for inference, and Kubernetes/Docker for hosting the API.
3.  **GraphRAG**: Using Knowledge Graphs (Neo4j) for retrieval. This is the next frontier after Vector RAG.
4.  **Multi-Modal**: We focused on Text. handling Images/Audio requires different splitters and models (GPT-4-Vision).

---

## 🚀 The AI Engineer Roadmap (2026 Edition)

Based on industry trends, here is the path from Junior to Staff AI Engineer.

### Level 1: The "Prompter" (0-1 Year)
*   **Focus**: Getting good outputs from APIs.
*   **Skills**:
    *   Prompt Engineering (Chain of Thought, Few-Shot).
    *   Basic API integration (OpenAI SDK).
    *   Streamlit / Gradio for demos.
*   **Checkpoint**: You can build a chatbot that "pretends" to be a pirate.

### Level 2: The "RAG Architect" (1-3 Years) - *This Curriculum matches this level*
*   **Focus**: Grounding AI in private data.
*   **Skills**:
    *   Vector Databases (Pinecone, Weaver, Chroma).
    *   ETL Pipelines (Unstructured.io, Parsing PDFs).
    *   Hybrid Search (BM25 + Dense).
    *   Evaluation (RAGAS, TruLens).
*   **Checkpoint**: You can build a system that answers questions about a 500-page PDF with <5% hallucination rate.

### Level 3: The "Agentic Engineer" (3-5 Years) - *The High Demand Role of 2026*
*   **Focus**: Autonomous systems that *do* work.
*   **Skills**:
    *   **LangGraph / AutoGen**: Managing complex state machines.
    *   **Tool Use**: Connecting to APIs (Salesforce, SQL, Stripe).
    *   **Human-in-the-loop**: Designing approval flows for dangerous actions.
*   **Checkpoint**: You can build an agent that plans a travel itinerary, books flights, and adds them to your Calendar, handling API errors gracefully.

### Level 4: The "AI Systems Architect" (5+ Years)
*   **Focus**: Scale, Cost, and Governance.
*   **Skills**:
    *   **Model Routing**: Dynamically routing traffic to tiny models (Haiku) vs big models (Opus) to save 80% on bills.
    *   **Inference & Serving**: Running Llama-3 on vLLM/Groq.
    *   **FinOps**: Attribution of costs per-feature and per-user.
    *   **Governance**: PII Redaction, Jailbreak defense.
*   **Checkpoint**: You manage a platform serving 1M+ AI requests/day with 99.9% uptime and controlled costs.

---

## 📂 Directory Structure

```
d:/Langchain-Jan/
├── 01_Foundations_And_Models/   # The Basics
├── 02_LCEL_The_Engine/          # The Syntax
├── 03_RAG_Zero_to_Hero/         # The Knowledge
├── 04_Memory_and_State/         # The Context
├── 05_Agents_and_Tools/         # The Action
├── 06_Production_and_Evaluation/# The Quality
└── 07_Module_Solutions/         # The Answer Key (Tasks)
```

**Happy Building.**
