import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()
model = ChatOpenAI(model="gpt-4o")

# ==========================================
# Challenge 1: The "Synthetic" Tester
# ==========================================
print("--- Challenge 1: Synthetic Data Gen ---")

class QAData(BaseModel):
    question: str
    context: str
    answer: str

class Dataset(BaseModel):
    pairs: list[QAData]

text_corpus = """
LangChain is a framework for developing applications powered by language models. 
It enables applications that:
- Are context-aware: connect a language model to sources of context
- Reason: rely on a language model to reason (about how to answer based on provided context)
"""

generator_prompt = ChatPromptTemplate.from_template(
    """Generate 2 Question-Answer pairs from the text below. 
    Output JSON matching the schema.
    
    Text: {text}"""
)

structured_llm = model.with_structured_output(Dataset)
chain = generator_prompt | structured_llm

result = chain.invoke({"text": text_corpus})
print(json.dumps(result.dict(), indent=2))
# You would save this to 'golden_dataset.json'


# ==========================================
# Challenge 2: Custom RAGAS Metric (Simulated)
# ==========================================
print("\n--- Challenge 2: Custom Politeness Metric ---")

# Real RAGAS requires 'datasets' library, simplifying here to show the logic.
def politeness_grader(answer: str):
    grader_prompt = f"""
    On a scale of 0.0 to 1.0, how polite is this text?
    1.0 = Extremely polite/formal.
    0.0 = Rude/Abrupt.
    Return ONLY the float number.
    
    Text: "{answer}"
    """
    score = model.invoke(grader_prompt).content
    return float(score)

ans1 = "Here is your data."
ans2 = "I'd be happy to help! Here is the data you requested."

print(f"Score 1: {ans1} -> {politeness_grader(ans1)}")
print(f"Score 2: {ans2} -> {politeness_grader(ans2)}")
