# Production Part 2: Tracing & LangSmith

## Concept Overview
**Logging** tells you *what* happened (e.g., "Error: 500").
**Tracing** tells you the *path* it took (e.g., User -> Chain A -> Retriever -> Chain B -> Error).

LangSmith helps you visualize the `RunnableParallel` branches and see exactly how many tokens were used at each step (Cost Tracking).

## Code Breakdown (`02_tracing_langsmith.py`)

### Environment Variables
Tracing is "Code-less". You don't wrap your code. You just set `LANGCHAIN_TRACING_V2=true`. LangChain's internal execution engine checks this flag and emits HTTP requests to the LangSmith API background thread.

## Real-World Interview Questions (War Stories)

### Q1: "We are leaking PII to LangSmith cloud. Legal is screaming."
**Real World Answer**:
"Standard Enterprise issue.
**The Fix**:
1. **Self-Hosted**: We switched to self-hosting LangSmith (or Arize Phoenix) on our own Kubernetes cluster.
2. **Redaction**: We implemented a `BeforeRequest` hook that regex-replaces emails/SSNs with `***` before the trace is sent to the collector."

### Q2: "How do you explain to a CEO why the AI application is costing $500/day?"
**Real World Answer**:
"I use LangSmith's **Cost Attribution** view.
I tag every run with `user_id` and `feature_flag`.
I showed them a chart: 'Feature A (Summarization) costs $50/day. Feature B (Chatbot) costs $450/day.'
We realized Feature B was re-reading the entire chat history on every keystroke. We fixed the frontend debounce, and costs dropped to $100/day."

## Topics Excluded
*   **Prompt Hub**: Storing prompts in the cloud version control.
*   **Datasets & Testing**: Managing datasets directly in the LangSmith UI. We covered the code side (RAGAS) instead.
- You display "CSAT Score" on a dashboard in real-time.

### Q3: `verbose=True` vs Tracing?
**Answer**:
- `verbose=True`: Prints to Stdout. ephemeral. Good for local dev.
- **Tracing**: Persistent storage. searchable. shared with team. Good for production.
