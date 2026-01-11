# Module 4 Tasks: Memory & State

## Challenge 1: The "Forgetful" Bot (Window Memory)
**Goal**: Implement a sliding window memory manually.
- **Requirements**:
    - Build a `get_session_history` function that uses a simple list.
    - However, enforce a constraint: "Only keep the last 2 interactions".
    - Test it: Chat 5 times. Ask "What was the very first thing I said?". It should reply "I don't know".
    - **Hint**: Extend `ChatMessageHistory` and override `add_message` to pop old messages.

## Challenge 2: The "Summary" Bot
**Goal**: Compact conversation history to save tokens.
- **Requirements**:
    - Use `ConversationSummaryBufferMemory` (or its Runnable equivalent: a chain that summarizes history).
    - Chat for 10 turns about a specific topic (e.g., "History of Rome").
    - Print the "Buffer" sent to the LLM. It should be a short paragraph summarizing the Rome discussion, not the raw chat logs.

## Challenge 3: Persistent File Storage
**Goal**: Persist memory to a JSON file so it survives a script restart.
- **Steps**:
    1. Create a `FileChatMessageHistory` class.
    2. When `get_session_history(session_id)` is called, it loads `session_id.json`.
    3. Run the script, tell it "My name is Bob".
    4. Kill the script.
    5. Run it again, ask "What is my name?". It should say "Bob".
