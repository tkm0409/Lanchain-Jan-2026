from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# --- Concept: Evaluation ---
# How do you know if your RAG system is good? "It feels good" is not an engineering metric.
# RAGAS (Retrieval Augmented Generation Assessment) is the standard library.
# It uses an LLM (GPT-4) as a judge to score your system.

def demonstrate_ragas_eval():
    print("--- Setting up Evaluation Data ---")
    
    # 1. The Dataset
    # usually you have a "Golden Dataset" of (Question, Answer, GroundTruth)
    data_samples = {
        'question': ['When was LangChain launched?'],
        'answer': ['LangChain was launched in October 2022 by Harrison Chase.'],
        'contexts': [['LangChain was launched in October 2022. It is a framework for LLMs.']],
        'ground_truth': ['October 2022']
    }
    
    dataset = Dataset.from_dict(data_samples)

    # 2. The Metrics
    # Faithfulness: Is the answer derived ONLY from the context? (Hallucination check)
    # Answer Relevancy: Did it actually answer the user's question?
    metrics = [
        faithfulness,
        answer_relevancy,
        # context_precision, # Requires generic "ground_truth" alignment
    ]

    print("--- Running Evaluation (LLM-as-a-Judge) ---")
    # This requires an OpenAI Key. It sends prompts to GPT-4 to grade your outputs.
    try:
        results = evaluate(
            dataset,
            metrics=metrics,
            llm=ChatOpenAI(model="gpt-4"),
            embeddings=OpenAIEmbeddings()
        )
        
        print("\n--- Evaluation Results ---")
        print(results)
    except Exception as e:
        print(f"Eval failed (likely missing API key or dependencies): {e}")
        print("Note: RAGAS requires `pip install ragas`")

if __name__ == "__main__":
    demonstrate_ragas_eval()
