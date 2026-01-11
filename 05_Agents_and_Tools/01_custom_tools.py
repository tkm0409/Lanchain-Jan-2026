from langchain_core.tools import tool, StructuredTool
from langchain_core.pydantic_v1 import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# --- Concept: Tools ---
# An Agent is just a Model + Tools.
# A Tool is a function with a Schema (name, description, args).
# The Model uses the description to decide WHEN to call the tool.
# It uses the schema to decide HOW to call the tool.

# --- Method 1: The Decorator (Easiest) ---
# Docstring is CRITICAL. It becomes the "System Prompt" for the tool choice.
@tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """
    Get the current weather for a specific location.
    Args:
        location: City and country (e.g. 'Paris, France')
        unit: 'celsius' or 'fahrenheit'
    """
    # Simulate API call
    return f"Weather in {location} is 25 degrees {unit}."

# --- Method 2: StructuredTool (More Control) ---
# Useful if you want to reuse existing Pydantic models.

class StockInput(BaseModel):
    ticker: str = Field(description="The stock ticker (e.g. AAPL)")

def get_stock_price(ticker: str) -> str:
    return f"{ticker} is trading at $150.00"

stock_tool = StructuredTool.from_function(
    func=get_stock_price,
    name="get_stock_ticker",
    description="Get the current price for a stock.",
    args_schema=StockInput
)

def demonstrate_tools():
    print("--- 1. Inspecting Tool Schemas ---")
    # This JSON is what the LLM actually sees.
    print(f"Weather Tool JSON:\n{get_weather.args_schema.schema_json()}")
    
    print("\n--- 2. Invoking Tools Manually ---")
    # Tools are Runnables!
    print(get_weather.invoke({"location": "London", "unit": "celsius"}))
    
    # --- 3. Error Handling ---
    # Tools can crash. You should handle errors gracefully.
    @tool
    def dangerous_tool(x: int):
        """Divides by zero."""
        return 1 / x

    try:
        dangerous_tool.invoke({"x": 0})
    except Exception as e:
        print(f"\nTool Crash: {e}")
        # In production, you'd want the tool to return "Error: Cannot divide by zero" 
        # so the Agent can try again, rather than crashing the whole program.

if __name__ == "__main__":
    demonstrate_tools()
