# Agents Part 1: Custom Tools

## Concept Overview
The "Reasoning Loop" of an agent depends entirely on the clarity of its tools.
If you have a tool named `search(query)`, and the description is "searches stuff", the agent will fail.
If the description is "Searches the internal knowledge base for technical documentation about API endpoints", the agent will succeed.

**The Tool Description IS the Prompt.**

## Code Breakdown (`01_custom_tools.py`)

### 1. `@tool` vs `StructuredTool`
- `@tool`: Great for simple functions. Infers schema from type hints and docstrings.
- `StructuredTool`: Necessary when you have complex validation logic (e.g. regex on input string) defined in a Pydantic model.

### 2. `args_schema`
This enables validation *before* the function runs.
If the LLM sends a string for an integer field, Pydantic raises an error.
LangChain catches this and tells the LLM: *"Invalid Argument. Expected int, got string. Please try again."*

## Real-World Interview Questions (War Stories)

### Q1: "The agent keeps calling `SendEmail` with a made-up email address 'john@example.com' when it doesn't know the real one."
**Real World Answer**:
"This is an Agent alignment issue. It wants to 'please' you by completing the task.
**The Fix**:
1. **Docstring Engineering**: I updated the tool description: *'ONLY use this tool if you have retrieved the email from the DatabaseTool. NEVER invent an email.'*
2. **Schema Validation**: I added a Pydantic regex validator to the input schema to ensure the email format is valid, though that doesn't fix the hallucination of the *value* itself."

### Q2: "Our 'SQLQueryTool' nuked the production database. The agent ran `DROP TABLE users;`."
**Real World Answer**:
"Never give an LLM write access to a production DB without guardrails.
**The Fix**:
1. **Read-Only Credentials**: The DB connection string used by the agent now has only `SELECT` permissions.
2. **Human-in-the-Loop**: For any `UPDATE` or `DELETE`, the tool now returns a special string: *'Action requires approval. Verification Link generated.'* The agent pauses, and we notify a human admin to click the link."

## Topics Excluded
*   **OpenAPI Toolkits**: Automatically converting a Swagger/OpenAPI spec into a list of 50 tools.
*   **Multi-Modal Tools**: Tools that accept Images as input (e.g. `DescribeImageTool`).

## Interview Questions & Concepts (SENIOR LEVEL)

### Q1: What happens when a tool call fails (raises Exception)?
**Answer**:
By default, the whole chain crashes.
**Best Practice**: The tool should return a string starting with "Error: ...".
The Agent sees this text observation ("Error: File not found") and can reason: "Oh, I made a typo. I will try a different filename."
*Tip*: Use `handle_tool_error=True` in `StructuredTool`.

### Q2: How do you handle a tool that requires user credentials (OAuth)?
**Answer**:
You cannot hardcode credentials in the tool definition if it's shared across users.
You must use **Runtime Configuration**.
Pass the user's token in the `config` dictionary of `invoke()`, and access it inside the tool via `CurrentConfig`.

### Q3: Can an Agent call multiple tools in parallel?
**Answer**:
Yes, modern models (GPT-4o, Claude 3.5) support **Parallel Function Calling**.
They output a list of tool invocations: `[get_weather(Paris), get_weather(London)]`.
LangChain's `AgentExecutor` or `LangGraph` executes them in parallel threads.
