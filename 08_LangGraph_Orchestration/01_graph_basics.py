import os
import random
from typing import TypedDict, Literal
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

load_dotenv()

# ==========================================
# CONCEPT: The State Machine
# Unlike Chains (DAGs), Graphs can loop.
# ==========================================

print("--- Lesson 1: Simple Cyclic Graph ---")

# 1. Define State
class AgentState(TypedDict):
    input: str
    steps: list[str]
    sentiment: str

# 2. Define Nodes (Functions)
def analyze_sentiment(state: AgentState):
    print("--- Node: Sentiment Analysis ---")
    txt = state['input'].lower()
    if "bad" in txt or "error" in txt:
        return {"sentiment": "negative", "steps": ["analyzed"]}
    return {"sentiment": "positive", "steps": ["analyzed"]}

def generate_positive_response(state: AgentState):
    print("--- Node: Positive Response ---")
    return {"steps": ["generated_happy"]}

def generate_apology_response(state: AgentState):
    print("--- Node: Apology Response ---")
    return {"steps": ["generated_sorry"]}

def quality_control(state: AgentState):
    print("--- Node: QC (Critique) ---")
    # Simulate a loop: If QC fails, go back to generation?
    # For this basic example, we just log it.
    return {"steps": ["qc_passed"]}

# 3. Define Logic (Edges)
def router(state: AgentState) -> Literal["positive_path", "negative_path"]:
    if state['sentiment'] == "negative":
        return "negative_path"
    return "positive_path"

# 4. Build Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("analyze", analyze_sentiment)
workflow.add_node("respond_happy", generate_positive_response)
workflow.add_node("respond_sorry", generate_apology_response)

# Add Edges
workflow.add_edge(START, "analyze")

# Conditional Edge
workflow.add_conditional_edges(
    "analyze",
    router,
    {
        "positive_path": "respond_happy",
        "negative_path": "respond_sorry"
    }
)

# Convergence
workflow.add_edge("respond_happy", END)
workflow.add_edge("respond_sorry", END)

# 5. Compile
app = workflow.compile()

# 6. Run
print("\n[Run 1: Happy Path]")
res1 = app.invoke({"input": "I love LangGraph!", "steps": [], "sentiment": ""})
print(f"Final State: {res1}")

print("\n[Run 2: Sad Path]")
res2 = app.invoke({"input": "This code is bad and full of errors", "steps": [], "sentiment": ""})
print(f"Final State: {res2}")
