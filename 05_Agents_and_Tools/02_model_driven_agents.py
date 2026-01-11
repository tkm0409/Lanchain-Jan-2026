from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# --- Concept: The Agent Loop ---
# 1. User Input -> Model
# 2. Model decides: "I need to call a tool" vs "I can answer directly"
# 3. If Tool: Execute Tool -> Feed output back to Model -> Repeat
# 4. If Answer: Return to User

@tool
def magic_number_tool(input_val: int) -> int:
    """Returns the magic number associated with the input."""
    return input_val * 42

@tool
def get_current_time() -> str:
    """Returns the current time."""
    return "12:00 PM"

def demonstrate_agent():
    # 1. Connect Tools
    tools = [magic_number_tool, get_current_time]
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # 2. Bind Tools (LCEL equivalent of function calling)
    # This tells the API: "Here are the functions you CAN call."
    # llm_with_tools = model.bind_tools(tools)
    
    # 3. Create the Prompt
    # Must include 'agent_scratchpad' where the intermediate tool thoughts/outputs go.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use tools when needed."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # 4. Create the Agent (The Brain)
    # create_tool_calling_agent simplifies the wiring of prompt | model | parser
    agent = create_tool_calling_agent(model, tools, prompt)

    # 5. Create the Executor (The Body)
    # The Executor handles the "While Loop" (Call -> Output -> Call -> Output)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, # Show thinking process
        max_iterations=3 # Safety limit
    )

    print("--- Invoking Agent ---")
    response = agent_executor.invoke({"input": "What is the magic number for 5? And what time is it?"})
    print(f"\nFinal Answer: {response['output']}")

if __name__ == "__main__":
    demonstrate_agent()
