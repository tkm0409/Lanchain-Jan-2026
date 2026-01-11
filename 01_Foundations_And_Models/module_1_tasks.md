# Module 1 Tasks: Foundations & Models

## Challenge 1: The "Frugal" Chatbot
**Goal**: Create a function `smart_ask(question: str)` that automatically selects the cheapest model based on the complexity of the question.
- **Requirements**:
    - If the user asks for a simple definition (length < 10 words), use `gpt-3.5-turbo` or a local HuggingFace model.
    - If the user asks for code or reasoning, use `gpt-4o` or `claude-3-sonnet`.
    - **Hint**: You can use a regex or string length check as a proxy for "complexity" for now, or make a cheap LLM call to classify the intent first!

## Challenge 2: The "Stubborn" Parser
**Goal**: Implement a `PydanticOutputParser` that handles failure gracefully without crashing.
- **Requirements**:
    - define a Pydantic model for a `Recipe` (ingredients, instructions, calories).
    - Feed the LLM text that is *almost* valid JSON but missing a closing brace or has a typo.
    - Catch the `OutputParserException`.
    - **Bonus**: In the `except` block, automatically call the LLM again with the error message: *"You sent invalid JSON. Here is the error: {e}. Try again."*

## Challenge 3: The Token Counter
**Goal**: Estimate the cost of a prompt before sending it.
- **Requirements**:
    - Use `tiktoken` (for OpenAI) to count the tokens in `SystemMessage` + `HumanMessage`.
    - Print: "This query will cost approx $0.002".
    - Then execute the query.
