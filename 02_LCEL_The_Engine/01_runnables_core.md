# LCEL Deep Dive: The Runnable Protocol

## Concept Overview
The "Runnable Protocol" is the interface contract that allows LangChain components to compost perfectly. If you implement `invoke`, `batch`, and `stream`, you can plug into any chain.

`RunnableParallel` is the secret weapon for performance. It executes all keys in the dictionary in parallel (using threads), which is drastically faster when fetching from multiple retrievers or calling multiple APIs.

## Code Breakdown (`01_runnables_core.py`)

### 1. `RunnablePassthrough`
```python
RunnableParallel({
    "original": RunnablePassthrough(), 
    "modified": some_function
})
```
`RunnablePassthrough` acts as an identity function `f(x) = x`.
It is crucial when you need to use the *same input* for multiple distinct operations (e.g., using a user's question to generating a search query AND using it in the final prompt).

### 2. Batch Efficiency
```python
chain.batch([1, 2, 3])
```
LangChain checks if `max_concurrency` is set (default usually based on CPU cores). It uses a `ThreadPoolExecutor` to run these tasks. In an API-heavy app (hitting OpenAI), this gives you 3x-10x speedups over a for-loop.

## Real-World Interview Questions (War Stories)

### Q1: "My chain is slow. I see `RunnableParallel` in the code, but it still feels sequential. Why?"
**Real World Answer**:
"This happened when we were using `RunnableLambda` with standard CPU-bound python code.
Python's **GIL (Global Interpreter Lock)** prevents true parallelism for CPU tasks. 
`RunnableParallel` uses thread pools, which only helps for **I/O Bound** tasks (like API calls to OpenAI or DB queries).
**The Fix**: I checked our custom functions. One of them was doing heavy regex processing. I moved that into a separate microservice (or ProcessPool) so it didn't block the main thread."

### Q2: "How do you unit test an LCEL chain? Mocking the pipe operator `|` is a nightmare."
**Real World Answer**:
"We don't mock the pipe. We mock the *components*.
I use `with_config` or standard `unittest.mock` to inject a `FakeLLM` at the model step.
LangChain has a `FakeListLLM` that returns pre-set responses.
```python
model = FakeListLLM(responses=["Test Response"])
chain = prompt | model | parser
assert chain.invoke("hi") == "Test Response"
```
This tests the *flow* (parsing, routing) without hitting the API."

### Q3: "Documentation says `invoke` supports async, but my FastAPI app freezes when I call it."
**Real World Answer**:
"You called `chain.invoke()` (blocking) inside an `async def` route. That blocks the entire Event Loop!
**The Fix**: You MUST use `await chain.ainvoke()`.
Even if some underlying tools are synchronous, `ainvoke` wraps them in threads to keep the loop free. Never mix blocking calls in async endpoints."

## Topics Excluded (Self-Study)
*   **RunnableBranch**: A legacy way to do routing. The modern way is to use `RunnableLambda` with if/else logic or a Router Chain.
*   **Dynamic Construction**: Building chains based on user input at runtime. This is usually dangerous and hard to debug. Static graphs are better.
