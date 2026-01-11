# LangChain Enterprise Curriculum (State of the Art 2026)

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

### 🚀 SOTA Expansion Layers (New for 2026)
These advanced modules cover the cutting-edge requirements for Staff/Principal Engineers.

| Module | Core Concepts | Industry Focus |
| :--- | :--- | :--- |
| **07. LangGraph** | State Machines, Checkpointing, Multi-Agent Supervisors | **Orchestration**: Managing complex, long-running agent loops closer to a State Machine than a Chain. |
| **08. Deployment** | FastAPI, LangServe, Docker, Microservices | **Engineering**: Taking your script from `localhost` to a scalable K8s service. |
| **09. Advanced RAG** | **CRAG** (Self-Correction), **GraphRAG**, **Vision** | **Reasoning**: Moving beyond "semantic search" to structural understanding and visual perception. |

---

## 🛠️ The "Excluded" Topics (What's Next?)
To keep this curriculum focused on *Application Engineering*, we explicitly excluded these deep-dive topics:

1.  **Fine-Tuning (PeFT/LoRA)**: Training models is a separate ML Engineering track.
2.  **Training Foundation Models**: We assume you *consume* APIs, not build GPT-5.

---

## 🚀 The AI Engineer Roadmap (2026 Edition)

Based on industry trends, here is the path from Junior to Staff AI Engineer.

### Level 1: The "Prompter" (0-1 Year)
*   **Focus**: Getting good outputs from APIs.
*   **Checkpoint**: You can build a chatbot that "pretends" to be a pirate.

### Level 2: The "RAG Architect" (1-3 Years) - *Modules 1-6*
*   **Focus**: Grounding AI in private data.
*   **Checkpoint**: A system that answers questions about a 500-page PDF with <5% hallucination rate.

### Level 3: The "Agentic Engineer" (3-5 Years) - *Module 7 (LangGraph)*
*   **Focus**: Autonomous systems that *do* work.
*   **Skills**:
    *   **LangGraph / AutoGen**: Managing complex state machines.
    *   **Multi-Agent Systems**: Supervisor/Worker patterns.
    *   **Human-in-the-loop**: Approval flows for dangerous actions.

### Level 4: The "AI Systems Architect" (5+ Years) - *Modules 8 & 9*
*   **Focus**: Scale, Cost, and Governance.
*   **Skills**:
    *   **Production Deployment**: Docker, LangServe, Async API.
    *   **Advanced RAG**: GraphRAG, Vision RAG, Self-RAG.
    *   **FinOps**: Attribution of costs per-feature.
*   **Checkpoint**: You manage a platform serving 1M+ AI requests/day with 99.9% uptime.

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
├── 07_Module_Solutions/         # The Answer Key (Tasks)
├── 08_LangGraph_Orchestration/  # [SOTA] State Machines
├── 09_Deployment_LangServe/     # [SOTA] Production API
└── 10_Advanced_RAG_2026/        # [SOTA] Self-RAG, Graphs, Vision
```

**Happy Building.**
