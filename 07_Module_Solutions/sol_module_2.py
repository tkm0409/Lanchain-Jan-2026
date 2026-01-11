import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
model = ChatOpenAI(model="gpt-3.5-turbo")

# ==========================================
# Challenge 1: The "Parallel Analyst"
# ==========================================
print("--- Challenge 1: The Parallel Analyst ---")

optimist_chain = (
    ChatPromptTemplate.from_template("Write a one-sentence optimist take on: {topic}")
    | model
    | StrOutputParser()
)

pessimist_chain = (
    ChatPromptTemplate.from_template("Write a one-sentence pessimist take on: {topic}")
    | model
    | StrOutputParser()
)

# Run them in parallel
analyst_chain = RunnableParallel(
    optimist=optimist_chain,
    pessimist=pessimist_chain,
)

def synthesizer(inputs):
    # This lambda runs AFTER parallel execution
    return f"CONCLUSION:\nOn one hand: {inputs['optimist']}\nOn the other: {inputs['pessimist']}"

final_chain = analyst_chain | RunnableLambda(synthesizer)

print(final_chain.invoke({"topic": "AI taking over jobs"}))


# ==========================================
# Challenge 2: The "Fallback" Chain
# ==========================================
print("\n--- Challenge 2: The Fallback Chain ---")

def unreliable_llm(x):
    # Simulates a broken API
    import random
    if random.random() < 0.8: # 80% failure rate
        raise ValueError("Service Unavailable (503)")
    return "GPT-4 Response (Success)"

def cheap_backup_llm(x):
    return "Backup Model Response (Saved the day!)"

# Create Runnables
primary = RunnableLambda(unreliable_llm)
backup = RunnableLambda(cheap_backup_llm)

# The Magic: .with_fallbacks()
safe_chain = primary.with_fallbacks([backup])

for i in range(3):
    print(f"Attempt {i+1}: {safe_chain.invoke('hi')}")


# ==========================================
# Challenge 3: The "Streaming" Converter
# ==========================================
print("\n--- Challenge 3: Streaming to File ---")

stream_chain = (
    ChatPromptTemplate.from_template("Write 3 short bullet points about: {topic}")
    | model
    | StrOutputParser()
)

print("Streaming started...")
with open("stream_output.txt", "w") as f:
    # .stream() returns an iterator
    for chunk in stream_chain.stream({"topic": "SpaceX"}):
        print(chunk, end="|", flush=True) # visual separator
        f.write(chunk)

print("\nDone! Check stream_output.txt")
