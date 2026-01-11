# Chain Formatting & Composition

## Concept Overview
The "Chain" is the fundamental unit of work.
In the old days (`LangChain v0.0.x`), we used `LLMChain`. **That is depreciated.**
The modern way is `Prompt | Model | Parser`.

## Code Breakdown (`02_chain_formatting.py`)

### 1. `StrOutputParser`
Crucial for cleaning up output.
- Without it: `AIMessage(content="The joke is...", response_metadata={...})`
- With it: `"The joke is..."`

### 2. Chain Composition
```python
composed_chain = (
    {"joke": chain} 
    | analysis_prompt 
    | model
)
```
This is where LCEL shines. You can compose chains endlessly.
The output of `chain` (which is a string) is mapped to the key `"joke"`.
This dictionary `{"joke": "..."}` is then passed to `analysis_prompt`.

## Real-World Interview Questions (War Stories)

### Q1: "We have a 5-step chain. If Step 3 fails, we lose all data from Step 1 and 2. How do we checkpoint?"
**Real World Answer**:
"LCEL is stateless. If it crashes, it crashes.
**The Fix**: We migrated big workflows to **LangGraph**.
LangGraph has a `MemorySaver` checkpointer. It saves the state after every node. If Step 3 crashes, I can resume the graph from Step 3 without re-running Step 1 and 2. It's essentially 'Save Game' for AI agents."

### Q2: "Why did you use `RunnablePassthrough.assign()` instead of just a dict?"
**Real World Answer**:
"Code readability and immutability.
`assign` (additive) keeps the inputs and *adds* the new result.
`chain | {"context": retriever, "question": RunnablePassthrough()}` is destructive; it *replaces* the stream.
Using `assign(context=retriever)` ensures that if I have other metadata in the stream (like `user_id`), it is preserved for later steps."

## Topics Excluded
*   **Legacy `LLMChain`**: You will see this in old StackOverflow posts. Avoid it.
*   **RouterChain**: The old multi-prompt router. We now prefer using Function Calling (Tools) for routing interpretation.
