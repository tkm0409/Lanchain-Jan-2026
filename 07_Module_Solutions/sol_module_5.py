import os
from dotenv import load_dotenv
from langchain_core.tools import tool, StructuredTool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

# ==========================================
# Challenge 1: The "Secure" Shell Tool
# ==========================================
print("--- Challenge 1: Secure Shell Tool ---")

@tool
def safe_shell(command: str) -> str:
    """Executes a shell command. BLOCKS dangerous commands like 'rm', 'sudo'."""
    blacklist = ["rm", "sudo", "chmod", "mv", ">"]
    
    # Security Check
    if any(b in command for b in blacklist):
        return f"SECURITY ALERT: Command '{command}' is blocked."
    
    # Simulation (don't actually run shell in this demo for safety)
    return f"Executed: {command}"

# Test directly
print(safe_shell.invoke("ls -la"))
print(safe_shell.invoke("rm -rf /")) # Should be blocked


# ==========================================
# Challenge 2: The "Travel" Agent
# ==========================================
print("\n--- Challenge 2: Travel Agent ---")

@tool
def book_flight(origin: str, destination: str, date: str):
    """Book a flight."""
    return f"Flight booked: {origin} -> {destination} on {date}"

@tool
def lookup_hotel(location: str):
    """Find a hotel in a city."""
    return f"Found hotel in {location}: Hilton"

tools = [book_flight, lookup_hotel]
model = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a travel assistant."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_openai_tools_agent(model, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

executor.invoke({"input": "I want to go from NY to London on Friday. Book the flight and find a hotel."})
# Watch stdout: It should call book_flight(origin="NY", destination="London", ...) AND lookup_hotel(location="London")
