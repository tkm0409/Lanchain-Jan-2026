# Production Part 1: Evaluation (RAGAS)

## Concept Overview
You cannot ship what you cannot measure.
Traditional NLP metrics (BLEU, ROUGE) measure *text overlap*. They are useless for LLMs.
We use **LLM-as-a-Judge**. We ask GPT-4: *"On a scale of 0-1, does this answer contradict the context?"*

## Code Breakdown (`01_evaluation_ragas.py`)

### 1. `metrics=[faithfulness]`
- Checks if the *Answer* can be inferred from the *Retrieved Context*.
- Low Faithfulness = **Hallucination**.

### 2. `metrics=[answer_relevancy]`
- Checks if the *Answer* addresses the *Question*.
- Low Relevancy = **Dodging the question**.

## Real-World Interview Questions (War Stories)

### Q1: "We put our RAG app in production, and users say the answers 'feel worse' than last week. We haven't changed the code."
**Real World Answer**:
"This is 'Model Drift' or 'Data Drift'.
Maybe the OpenAI model was updated (gpt-4-0613 -> gpt-4-1106).
Or maybe we ingested new documents that are confusing the retriever.
**The Fix**:
We have a nightly **Regression Test Suite** (using RAGAS).
It runs 50 golden questions every night. If the 'Faithfulness' score drops by >5%, the CI pipeline fails and alerts us on Slack."

### Q2: "RAG Evaluation is too expensive. Running GPT-4 to evaluate GPT-3.5 costs double."
**Real World Answer**:
"Valid concern.
**The Strategy**:
1. **Tiered Eval**: Use a cheap model (GPT-3.5) for 'Formatting' checks (Is it JSON?).
2. **Sampling**: Only evaluate a random 5% of production traces with GPT-4, not 100%.
3. **Open Source Judge**: We fine-tuned a Llama-3-8b model specifically to act as a judge. It's free to run locally and correlates 90% with GPT-4 on our dataset."

## Topics Excluded
*   **DeepEval / Arize Phoenix**: Other great evaluation libraries. RAGAS is just one standard.
*   **Human Evaluation**: Ultimately, you need a tool (like Label Studio) for humans to spot check the machine's evaluation.
*   **Ground Truth Problem**: Generating a golden dataset of (Question, Context, Answer) is expensive. Humans have to manual review it.
    **Solution**: Synthetic Data Generation. Use GPT-4 to read your documents and *generate* questions and answers to form a synthetic test set.
*   **Chatbot (Multi-turn) vs QA system (Single-turn)**: RAGAS is primarily for Single-turn QA.
    For Chatbots, you need **End-to-End Evaluation**.
    - Did the user leave happy? (Sentiment Analysis)
    - Did the user achieve their goal? (Task Success Rate - e.g. "Did they book the flight?")
*   **Why not just use Cosine Similarity for evaluation?**
    **Answer**:
    "The capital of France is Paris" and "Paris is the capital of France" might have different embeddings depending on the model, but they mean the same thing.
    Embeddings are okay for *Retrieval* (ranking), but poor for *Fact Checking*. Logic is required.
