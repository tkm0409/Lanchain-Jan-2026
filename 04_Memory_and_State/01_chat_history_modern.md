# Memory & State Management

## Concept Overview
REST APIs are stateless. LLMs are stateless.
**State** is the responsibility of the application layer.

In LangChain, `RunnableWithMessageHistory` is the standard middleware. It separates the **Business Logic** (the Chain) from the **UserData** (the History).

## Code Breakdown (`01_chat_history_modern.py`)

### 1. `get_session_history`
This factory function is the integration point.
In production, you replace the dict lookup with a Redis call:
```python
def get_session_history(session_id):
    return RedisChatMessageHistory(session_id, url=REDIS_URL)
```

### 2. `MessagesPlaceholder`
Crucial. It tells the prompt template: *"Insert the list of message objects right here."*
Without it, the model sees your new question but has no context of the past.

## Real-World Interview Questions (War Stories)

### Q1: "We deployed our chatbot, and after 20 minutes of chatting, it crashes with 'ContextWindowExceeded'. We are using 'MessageWindow' of 10."
**Real World Answer**:
"Message count != Token count.
User messages can be huge (pasting a 500-line error log). A window of 10 messages could be 20k tokens.
**The Fix**:
I switched to **Token-based Trimming**.
OpenAI and Anthropic now support `trim_messages(..., max_tokens=2000)`. I apply this *before* sending history to the model. It drops the oldest messages until we fit in the budget."

### Q2: "We have 1M users. Storing chat history in Postgres JSONB columns is slowing down the DB."
**Real World Answer**:
"Chat logs are high-write, append-only. Relational DBs hate this at scale.
**The Fix**:
I migrated the Session Store to **DynamoDB** (or Cassandra/Redis).
Key-Value stores are designed for `get_history(user_id)` lookups.
We set a **TTL (Time To Live)** of 30 days on the rows so we don't pay for storage of ghosts who never returned."

### Q3: "How do you handle 'Branching' conversations? (e.g. User edits a previous message)"
**Real World Answer**:
"Standard `ChatMessageHistory` is a linear list. It can't fork.
**The Fix**:
We had to implement a **Tree-based Storage**.
Every message has a `parent_id`. When a user edits a message, we create a new node branching off the parent. This is how ChatGPT's 'Edit' feature works. It's complex graph traversal, not a simple list append."

## Topics Excluded
*   **Vector Memory**: Using a VectorStore as long-term memory (simulating human hippocampus). This is covered in "Agents" usually (MemGPT concepts).
*   **Entity Memory**: Extracting entities (Names, Places) and storing them in a Knowledge Graph.

## Interview Questions & Concepts (SENIOR LEVEL)

### Q1: How do you handle infinite conversation history (Token Limit)?
**Answer**:
You cannot send infinite history. You need a strategy:
1. **WindowBuffer**: Keep last K (e.g. 10) messages. Drop old ones.
2. **SummaryBuffer**: Use an LLM to "summarize" the old conversation into a system message, and keep the last K raw messages.
3. **Vector Memory**: Store all messages in a vector DB and retrieve only relevant past messages based on current topic.

### Q2: What is the difference between `ChatMessageHistory` and `RunnableWithMessageHistory`?
**Answer**:
- `ChatMessageHistory`: A data structure (List[Message]) with `.add_user_message()` methods.
- `RunnableWithMessageHistory`: A **Runtime Wrapper** that automates the fetching and saving of that data structure during chain execution.

### Q3: Why is Redis preferred over Postgres for Chat History?
**Answer**:
- **Latency**: Retrieving history happens *every single turn*. Redis (in-memory) is faster.
- **TTL (Time To Live)**: Chat history often has an expiration (e.g. 30 days). Redis supports TTL natively. Postgres requires cleanup jobs.
