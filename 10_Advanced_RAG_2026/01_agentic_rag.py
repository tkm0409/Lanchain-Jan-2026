import os
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.graph import StateGraph, START, END

load_dotenv()

# ==========================================
# CONCEPT: Agentic RAG (CRAG)
# 1. Retrieve
# 2. Grade Documents (Irrelevant? Discard)
# 3. Rewrite Query (If Grade is bad)
# 4. Generate
# ==========================================

print("--- Lesson 1: Agentic RAG (Self-Correcting) ---")

class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]
    re_ask_count: int

# Mock Retriever
def retrieve(state: GraphState):
    print("--- [Node] Retrieve ---")
    query = state["question"]
    # Simulate bad retrieval for the first try
    if state.get("re_ask_count", 0) == 0:
        return {"documents": ["Apple pie recipe", "How to fix a car"]} # Irrelevant to most queries
    else:
        return {"documents": ["LangChain is a framework...", "LangGraph enables cycles..."]}

# Grader
class GradeDocuments(BaseModel):
    """Binary score for relevance check."""
    binary_score: str = Field(description="yes or no")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
structured_llm_grader = llm.with_structured_output(GradeDocuments)

grader_prompt = ChatPromptTemplate.from_template(
    "You are a grader assessing relevance. \n"
    "Doc: {document} \n"
    "Question: {question} \n"
    "Give a binary 'yes' or 'no' score."
)
grader_chain = grader_prompt | structured_llm_grader

def grade_documents(state: GraphState):
    print("--- [Node] Grade Documents ---")
    question = state["question"]
    documents = state["documents"]
    
    filtered_docs = []
    relevant = False
    for d in documents:
        score = grader_chain.invoke({"question": question, "document": d})
        if score.binary_score == "yes":
            print(f"  - Doc '{d[:15]}...' is RELEVANT")
            filtered_docs.append(d)
            relevant = True
        else:
            print(f"  - Doc '{d[:15]}...' is IRRELEVANT")
            
    return {"documents": filtered_docs, "run_web_search": not relevant}

def transform_query(state: GraphState):
    print("--- [Node] Transform Query (Re-writing) ---")
    return {"question": state["question"] + " (Optimized)", "re_ask_count": state.get("re_ask_count", 0) + 1}

def generate(state: GraphState):
    print("--- [Node] Generate ---")
    return {"generation": "Here is the answer based on the vetted docs."}

def decide_to_generate(state: GraphState):
    # If no documents survived grading, re-write query
    if not state["documents"]:
        if state.get("re_ask_count", 0) > 1: # Prevent infinite loop
             return "generate" # Give up and generate with what we have
        return "transform_query"
    return "generate"

# Build Graph
workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("transform_query", transform_query)
workflow.add_node("generate", generate)

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade_documents")

workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate"
    }
)
workflow.add_edge("transform_query", "retrieve") # Loop back!
workflow.add_edge("generate", END)

app = workflow.compile()

# Run
final = app.invoke({"question": "What is LangGraph?", "re_ask_count": 0})
print(f"\nFinal Generation: {final.get('generation')}")
