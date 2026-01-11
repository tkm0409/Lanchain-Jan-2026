import time
from typing import Dict, List
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

load_dotenv()

# --- Concepts ---
# LCEL (LangChain Expression Language) is built on the "Runnable Protocol".
# Almost everything in LangChain is a Runnable.
# A Runnable must implement:
#   - invoke(input) -> output
#   - stream(input) -> iterator[output]
#   - batch([inputs]) -> [outputs]

def simple_multiplier(x: int) -> int:
    """A standard Python function."""
    print(f"Computing {x} * 2...") 
    time.sleep(0.5) # Simulate work
    return x * 2

def formatting_func(data: Dict) -> str:
    """Formats the output."""
    return f"The Result is: {data['multiplied_value']}"

def demonstrate_runnables():    
    # 1. RunnableLambda
    # Wrap standard python functions to make them usable in chains.
    runnable_mul = RunnableLambda(simple_multiplier)
    
    # 2. RunnableParallel
    # Runs multiple branches in parallel. Dictionary output.
    # Input x -> { "original": x, "multiplied": x*2 }
    parallel_branch = RunnableParallel({
        "original_value": RunnablePassthrough(), # Passes the input through unchanged
        "multiplied_value": runnable_mul
    })

    # 3. The Chain
    # Input -> Parallel -> Formatting
    chain = parallel_branch | RunnableLambda(formatting_func)

    # --- A. Invoke (Synchronous) ---
    print("--- A. Invoke (Single Input) ---")
    result = chain.invoke(5)
    print(result) # "The Result is: 10"

    # --- B. Batch (Parallel Execution) ---
    # LangChain automatically uses ThreadPoolExecutor for batch operations.
    # Since we added sleep(0.5), sequential would take 1.5s. Batch should take ~0.5s.
    print("\n--- B. Batch (Multiple Inputs) ---")
    start = time.time()
    results = chain.batch([1, 2, 3])
    end = time.time()
    print(f"Batch Results: {results}")
    print(f"Time Taken: {end - start:.2f}s (Should be approx 0.5s, not 1.5s)")

    # --- C. Stream (Generator) ---
    # Even though our functions aren't generators, LangChain can stream the final result step-by-step
    # if the components support it. For LLMs, this prints tokens as they arrive.
    print("\n--- C. Stream ---")
    # For a simple function chain, stream yields the final result at once, 
    # but for LLMs it yields tokens.
    for chunk in chain.stream(4):
        print(f"Chunk: {chunk}")

    # --- D. RunnablePassthrough details ---
    # often used to pass extra arguments to a prompt.
    # chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | model

if __name__ == "__main__":
    demonstrate_runnables()
