import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

# ==========================================
# CONCEPT: Deep Persistence & Interruption
# We pause execution, wait for approval, 
# and potentially EDIT the state before resuming.
# ==========================================

print("--- Lesson 2: Human-in-the-Loop & Time Travel ---")

# 1. State
class State(TypedDict):
    action: str
    approved: bool
    result: str

# 2. Nodes
def step_1_propose_action(state: State):
    print("--- Step 1: Proposing Dangerous Action ---")
    return {"action": "delete_production_db", "approved": False}

def step_2_execute_action(state: State):
    if state['approved']:
        print(f"--- Step 2: EXECUTING {state['action']} ---")
        return {"result": "Done"}
    else:
        print("--- Step 2: Action BLOCKED by Human ---")
        return {"result": "Blocked"}

# 3. Graph
workflow = StateGraph(State)
workflow.add_node("propose", step_1_propose_action)
workflow.add_node("execute", step_2_execute_action)

workflow.add_edge(START, "propose")
workflow.add_edge("propose", "execute")
workflow.add_edge("execute", END)

# 4. Checkpointer (InMemory for demo)
memory = MemorySaver()

# 5. Compile with Interrupt
app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["execute"] # PAUSE execution *before* entering 'execute' node
)

# 6. Run
thread_config = {"configurable": {"thread_id": "thread-1"}}

print("\n[Phase 1] Initial Run (Will Pause)")
res = app.invoke({"action": "none", "approved": False}, config=thread_config)
print(f"Paused State: {res}") 
# Note: 'res' might be the output of 'propose'. 
# The graph execution STOPPED.

# 7. Check Status
current_state = app.get_state(thread_config)
print("\n[Phase 2] Inspection")
print(f"Next Node: {current_state.next}")
print(f"Current Values: {current_state.values}")

# 8. Human Intervention (Time Travel / State Update)
# The human sees "delete_db" and says "NO! change action to 'say_hello' and approve it."
print("\n[Phase 3] Human Edit (Time Travel)")
app.update_state(
    thread_config, 
    {"action": "say_hello_world", "approved": True} 
)

# 9. Resume
print("\n[Phase 4] Resuming Execution")
# Calling invoke(None) resumes from the paused state
final = app.invoke(None, config=thread_config)
print(f"Final State: {final}")
