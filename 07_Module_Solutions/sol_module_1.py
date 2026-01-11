import os
import re
from typing import List, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda
from langchain.output_parsers import OutputFixingParser

load_dotenv()

# ==========================================
# Challenge 1: The "Frugal" Chatbot (Router)
# ==========================================
print("--- Challenge 1: The Frugal Chatbot ---")

def get_cheapest_model(prompt_text: str):
    """
    Router logic: 
    - Short/Simple queries -> GPT-3.5-Turbo (Cheap)
    - Long/Complex queries -> GPT-4o (Smart/Expensive)
    """
    # Heuristic: If prompt is < 15 words or contains "define", use cheap model
    word_count = len(prompt_text.split())
    is_simple = word_count < 15 or "define" in prompt_text.lower()
    
    if is_simple:
        print(f"[Router] Detected SIMPLE query ({word_count} words). Routing to GPT-3.5-Turbo.")
        return ChatOpenAI(model="gpt-3.5-turbo")
    else:
        print(f"[Router] Detected COMPLEX query ({word_count} words). Routing to GPT-4o.")
        return ChatOpenAI(model="gpt-4o")

def smart_ask(question: str):
    model = get_cheapest_model(question)
    response = model.invoke(question)
    return response.content

# Test cases
print("Q1:", smart_ask("Define apple."))
print("Q2:", smart_ask("Write a python script to recursively walk a directory tree and calculate SHA256 hashes."))


# ==========================================
# Challenge 2: The "Stubborn" Parser (Robustness)
# ==========================================
print("\n--- Challenge 2: The Stubborn Parser ---")

class Recipe(BaseModel):
    name: str = Field(description="Name of the dish")
    ingredients: List[str] = Field(description="List of ingredients")
    calories: int = Field(description="Total calories")

parser = PydanticOutputParser(pydantic_object=Recipe)

# Simulate a "Bad" LLM response (JSON syntax error)
bad_json_output = """
Sure! Here is your recipe:
{
    "name": "Omelette",
    "ingredients": ["Eggs", "Cheese"],
    "calories": 250, 
    "notes": "Served hot"
""" # Missing closing brace }

print(f"Input Bad JSON: {bad_json_output}")

try:
    # This will fail
    parser.parse(bad_json_output)
except Exception as e:
    print(f"\n[Expected Error]: Parser crashed as expected: {e}")
    
    # Solution: Auto-Fixing using OutputFixingParser
    # This wraps the original parser. If it fails, it calls an LLM to "fix" the bad String.
    print("[System] Attempting Auto-Fix...")
    fix_model = ChatOpenAI(model="gpt-3.5-turbo")
    fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=fix_model)
    
    fixed_recipe = fixing_parser.parse(bad_json_output)
    print(f"[Success] Fixed Recipe Object: {fixed_recipe}")


# ==========================================
# Challenge 3: Cost Estimator (Token Counting)
# ==========================================
print("\n--- Challenge 3: Token Cost Estimator ---")
import tiktoken

def estimate_cost(text: str, model_name="gpt-4"):
    encoding = tiktoken.encoding_for_model("gpt-4")
    token_count = len(encoding.encode(text))
    
    # Approx pricing
    price_per_1k = 0.03 if "gpt-4" in model_name else 0.001
    cost = (token_count / 1000) * price_per_1k
    
    print(f"Query: '{text}' | Tokens: {token_count} | Est Cost: ${cost:.5f}")
    return cost

estimate_cost("Hello world")
estimate_cost("Write a history of the Roman Empire starting from Augustus...")
