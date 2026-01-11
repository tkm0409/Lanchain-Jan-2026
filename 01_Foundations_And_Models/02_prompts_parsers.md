# Prompts & Structured Output: The Enterprise Requirement

## Concept Overview
In a hobby project, getting a chatty response like *"Sure! Here is the data: ..."* is fine.
In an enterprise system, that breaks everything. You need **JSON**. You need **Schema Compliance**.

**PydanticOutputParser** is the bridge between the fuzzy world of LLMs and the strict world of software engineering. It forces the model to adhere to a schema.

## Code Breakdown (`02_prompts_parsers.py`)

### 1. The Pydantic Model
```python
class MovieReview(BaseModel):
    title: str = Field(description="...")
    rating: int = Field(description="...")
```
Defining the schema *is* the prompt engineering. The `description` fields are actually passed to the LLM to help it understand what to extract.

### 2. The Chain
```python
chain = prompt | model | parser
```
This is **LCEL** (LangChain Expression Language). It unifies the workflow.
- Input Dictionary (`{"user_input": "..."}`) enters the **Prompt**.
- **Prompt** replaces `{user_input}` and `{format_instructions}` and produces a `List[Message]`.
- **Model** takes messages, produces `AIMessage`.
- **Parser** takes `AIMessage.content`, parses the JSON, and validates it against `MovieReview`.

## Real-World Interview Questions (War Stories)

### Q1: "In production, PydanticParser fails 10% of the time because the model output 'Here is your JSON: {...}'. How do you fix this?"
**Real World Answer**:
"Models love to be polite. The preamble text ('Sure! Here is data:') breaks `json.loads`.
**The Fix**:
1. **Robust Regex**: I don't trust the raw string. I use a regex `r'\{.*\}'` (dot-all mode) to find the first `{` and last `}` and extract only that substring.
2. **JSON Mode**: I switched to `ChatOpenAI(..., model_kwargs={"response_format": {"type": "json_object"}})`. This forces the provider's API to enforce valid JSON at the sampling layer, reducing syntax errors to near zero."

### Q2: "We need to extract data from 10,000 PDFs. It's too slow. How do you speed it up?"
**Real World Answer**:
"PydanticParser is synchronous.
I converted the extraction chain to use `chain.batch(inputs)` and set `max_concurrency=10`.
However, we hit OpenAI Rate Limits (TPM).
So I implemented an **Exponential Backoff** retry decorator (`@retry(stop=stop_after_attempt(3), wait=wait_exponential())`) utilizing the Tenacity library. This smoothed out the spikes."

### Q3: "The model is hallucinating fields. It adds a 'confidence_score' field that isn't in my Pydantic model."
**Real World Answer**:
"This is 'Schema Drift'.
I set `extra='forbid'` in the Pydantic Config.
```python
class StrictModel(BaseModel):
    class Config:
        extra = 'forbid'
```
This causes validation to FAIL if extra fields are present. Combined with a `RetryOutputParser`, the error message ('Unexpected field: confidence_score') is sent back to the LLM, and it corrects itself in the next attempt."

## Topics Excluded (Self-Study)
*   **XML Parsing**: We focused on JSON. Some older models (Claude 2) preferred XML tags. LangChain has `XMLOutputParser`.
*   **Kor**: An older library for extraction that is now mostly superseded by `create_structured_output_chain`, but you might see it in legacy codebases.

## Interview Questions & Concepts (SENIOR LEVEL)

### Q1: What happens if the Model returns valid JSON but it fails Pydantic validation (e.g. missing field)?
**Answer**:
`PydanticOutputParser` will raise a `ValidationError` (or `OutputParserException`).
*Advanced Follow-up*: How do you fix this automatically?
*Answer*: You use an **OutputFixingParser** or **RetryOutputParser**. These wrap the original parser and, on error, send the specific error message *back* to the LLM, asking it to correct its own mistake.

### Q2: What is "Chain of Thought" (CoT) prompting?
**Answer**:
It's a technique where you ask the model to "think step-by-step" before giving the final answer.
In LangChain, you often add a field `reasoning: str` to your Pydantic model *before* the final answer field. This forces the model to generate its thought process first, which drastically improves accuracy on complex logic tasks.
*Key concept*: "Output Tokens allow the model to *compute*."

### Q3: Why use `ChatPromptTemplate` instead of f-strings?
**Answer**:
1. **Security**: Prevents Prompt Injection to some degree (though not a silver bullet).
2. **Modularity**: You can `partial` out variables (like format instructions) separately from user input.
3. **Multi-modal**: It handles the complexity of image inputs and different roles (System/User/Placeholder) gracefully.

### Q4: `StructuredOutput` vs `PydanticOutputParser`?
**Answer**:
Note that many new models (GPT-4o, Gemini 1.5) support **Native Tool Calling** or **JSON Mode**.
- `model.with_structured_output(Schema)` is the modern, preferred way if the model supports it. It uses the provider's native reliable JSON mode.
- `PydanticOutputParser` is the fallback "Prompt Engineering" way (appending instructions to the prompt text). It works on *any* model, even dumb ones.
