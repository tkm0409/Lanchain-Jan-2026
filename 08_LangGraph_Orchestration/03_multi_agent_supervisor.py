import os
from typing import Annotated, List, TypedDict, Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

# ==========================================
# CONCEPT: The Supervisor Pattern
# One LLM (Supervisor) routes tasks to 
# specialized "Worker" Agents (Planner, Coder).
# ==========================================

print("--- Lesson 3: Multi-Agent Supervisor ---")

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 1. State: A shared message history
class AgentState(TypedDict):
    messages: List[BaseMessage]
    next: str # Who acts next?

# 2. Workers
# Creating simple agents using just the LLM for brevity
# In real life, these would be Tools Agents.

def researcher_node(state: AgentState):
    print("--- [Worker] Researcher working... ---")
    messages = state["messages"]
    # Simulate research
    response = SystemMessage(content="Researcher: Found that Python 3.12 was released in late 2023.")
    return {"messages": [response]}

def coder_node(state: AgentState):
    print("--- [Worker] Coder working... ---")
    messages = state["messages"]
    response = SystemMessage(content="Coder: print('Hello from Python 3.12')")
    return {"messages": [response]}

# 3. The Supervisor (Router)
# It sees the history and decides: "Researcher", "Coder", or "FINISH".

members = ["Researcher", "Coder"]
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers: a Researcher and a Coder."
    " Given the user request, decide who should act next."
    " If the task is done, output 'FINISH'."
)

supervisor_chain = (
    ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Who should act next? Select one of: {members} or FINISH.")
    ]).partial(members=", ".join(members))
    | llm
)

def supervisor_node(state: AgentState):
    print("--- [Supervisor] Routing... ---")
    result = supervisor_chain.invoke(state)
    # Parse the output to get the next agent name
    # Very naive parsing for demo; use Structured Outputs in prod!
    route = result.content.strip()
    if "Researcher" in route: return {"next": "Researcher"}
    if "Coder" in route: return {"next": "Coder"}
    return {"next": "FINISH"}

# 4. Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("Supervisor", supervisor_node)
workflow.add_node("Researcher", researcher_node)
workflow.add_node("Coder", coder_node)

workflow.add_edge(START, "Supervisor")

# The Router Logic
workflow.add_conditional_edges(
    "Supervisor",
    lambda state: state["next"], # Read 'next' key
    {
        "Researcher": "Researcher",
        "Coder": "Coder",
        "FINISH": END
    }
)

# Workers always report back to Supervisor
workflow.add_edge("Researcher", "Supervisor")
workflow.add_edge("Coder", "Supervisor")

# 5. Compile
app = workflow.compile()

# 6. Run
final = app.invoke({
    "messages": [
        HumanMessage(content="Find out when Python 3.12 was released and write a hello world script for it.")
    ]
})

print("\n--- Final Conversation History ---")
for m in final["messages"]:
    print(f"{m.type}: {m.content}")
