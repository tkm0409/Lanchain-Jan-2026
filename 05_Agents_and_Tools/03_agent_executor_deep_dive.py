from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# --- Concept: Robustness ---
# Agents are unpredictable. They fail. They loop.
# We need to control the runtime.

@tool
def broken_tool(x: str) -> str:
    """Always raises an error."""
    raise ValueError("I am a broken tool")

def demonstrate_robust_agent():
    tools = [broken_tool]
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an agent testing error handling."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(model, tools, prompt)

    # --- Feature 1: Handling Parsing/Tool Errors ---
    # handle_parsing_errors=True: If model outputs bad JSON, LangChain sends a message back: "Invalid Format, try again"
    # handle_tool_error: Managed inside the tool definition usually, but AgentExecutor catches crashes too.
    
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        # A. Return Thoughts: Gives us the full trace of what happened.
        return_intermediate_steps=True, 
        # B. Handle Errors: prevents python crash on parsing failure
        handle_parsing_errors=True,
        # C. Max Iterations: Stops infinite loops
        max_iterations=2,
        verbose=True
    )

    print("--- Invoking Agent with Broken Tool ---")
    try:
        # The agent will try to call the tool, fail, see the error, and try to recover (or give up).
        response = agent_executor.invoke({"input": "Call the broken tool please."})
        
        print(f"\nFinal Answer: {response['output']}")
        
        print("\n--- Intermediate Steps (The 'Thoughts') ---")
        # intermediate_steps is a list of tuples: (AgentAction, Observation)
        for action, observation in response["intermediate_steps"]:
            print(f"Action: {action.tool}")
            print(f"Observation: {observation}")
            
    except Exception as e:
        print(f"Executor failed: {e}")

if __name__ == "__main__":
    demonstrate_robust_agent()
