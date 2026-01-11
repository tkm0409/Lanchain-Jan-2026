import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# --- Concept: Observability ---
# LangChain is complex. "Chains calling Agents calling Tools calling Chains".
# If it breaks, good luck debugging with `print()`.
# LangSmith provides a "Trace" of every execution.

# To enable it, you just set Environment Variables.
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=<your-api-key>
# LANGCHAIN_PROJECT=<your-project-name>

def demonstrate_tracing():
    # If the env vars are set, this call will automatically be logged to LangSmith UI.
    model = ChatOpenAI(model="gpt-4o", temperature=0)
    
    print("--- Invoking Model (Check LangSmith Dashboard) ---")
    response = model.invoke("What is the meaning of life?")
    print(response.content)

if __name__ == "__main__":
    if "LANGCHAIN_API_KEY" not in os.environ:
        print("Warning: LANGCHAIN_API_KEY not found. Tracing will not work.")
    else:
        demonstrate_tracing()
