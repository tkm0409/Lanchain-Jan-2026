# Module 2 Tasks: LCEL & Runnables

## Challenge 1: The "Parallel Analyst"
**Goal**: Use `RunnableParallel` to get two diverse opinions on a topic and then synthesize them.
- **Steps**:
    1. Define `chain_optimist`: A chain that writes a positive take on `{topic}`.
    2. Define `chain_pessimist`: A chain that writes a negative take on `{topic}`.
    3. Use `RunnableParallel` to run them simultaneously.
    4. Pass the dictionary output `{'optimist': ..., 'pessimist': ...}` into a final `synthesis_chain` that combines them.

## Challenge 2: The "Fallback" Chain
**Goal**: Build a chain that tries GPT-4, and if it fails (simulate an error), falls back to a cheaper model.
- **Hint**: Look up the `.with_fallbacks()` method in LCEL documentation.
- **Requirement**: Create a `RunnableLambda` that raises an exception 50% of the time, and attach a fallback runnable that says "Fallback Activated!".

## Challenge 3: The "Streaming" Converter
**Goal**: Consume a streamed response and accumulate it manually.
- **Requirement**:
    - Call `chain.stream({"topic": "AI"})`.
    - Iterate over the chunks.
    - Write them to a file `output.txt` in real-time (simulating a UI buffer).
    - Print "Done" only after the stream is exhausted.
