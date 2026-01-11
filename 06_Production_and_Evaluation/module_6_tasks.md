# Module 6 Tasks: Production & Evaluation

## Challenge 1: The "Synthetic" Tester
**Goal**: Use an LLM to generate test cases for itself.
- **Steps**:
    1. Load a document (e.g., this curriculum).
    2. Prompt GPT-4: *"Read this text and generate 5 question-answer pairs about it in JSON format."*
    3. Save this as `golden_dataset.json`.
    4. Use this dataset to evaluate your RAG pipeline in Challenge 2.

## Challenge 2: Custom RAGAS Metric
**Goal**: Define a metric "Politeness" for RAGAS.
- **Requirements**:
    - RAGAS allows custom metrics using an LLM.
    - Create a class `PolitenessMetric`.
    - Prompt: *"On a scale of 0-1, how polite is this response? 1 is extremely formal, 0 is rude."*
    - Run it on your chatbot's output.

## Challenge 3: "Where did it break?" (Tracing)
**Goal**: Manually log feedback to LangSmith (Simulation).
- **Requirements**:
    - Run a chain that answers a question.
    - Simulate a user clicking "Thumbs Down" on the result.
    - Use `langsmith.Client` to find that specific run ID and attach a feedback score `score=0.0`.
    - Go to the LangSmith UI (if you have access) and verify the feedback is tagged.
