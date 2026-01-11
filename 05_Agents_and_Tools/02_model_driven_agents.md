# Agents Part 2: Model Driven Agents

## Concept Overview
The transition from **Chains** (Hardcoded sequences) to **Agents** (Dynamic reasoning) is the shift from "Automation" to "AI".
In an Agent, the LLM acts as the router. It decides what to do next.

**`create_tool_calling_agent`** is the modern standard. It uses the LLM provider's native "Function Calling" API (finetuned for tools) rather than the older "ReAct" prompting capability (asking the model to output a specific string regex).

## Code Breakdown (`02_model_driven_agents.py`)

### 1. `AgentExecutor`
This is the runtime. It manages:
- **Encoding**: Converting tool outputs to messages.
- **Looping**: Feeding outputs back to the model.
- **Stopping**: detecting when the model says "I'm done" or hitting `max_iterations`.

### 2. `agent_scratchpad`
This is a specific key in the prompt. It is where the *History of Actions* lives.
Round 1: Scratchpad = []
Round 2: Scratchpad = [ToolCall(name="get_time"), ToolOutput("12:00")]
Without this, the agent would hallucinate or repeat the same action forever.

## Real-World Interview Questions (War Stories)

### Q1: "We are using Function Calling to extract data. It works on GPT-4 but fails on Llama-2-70b."
**Real World Answer**:
"Llama-2 (and older models) don't have native 'Function Calling' fine-tuning. They just see text.
**The Fix**:
We had to switch to **Prompt Engineering**.
We injected the JSON schema into the System Prompt: *'You have access to these tools: [...]. To use one, write valid JSON.'*
Then we used a robust `OutputParser` to grep the JSON from the output. It's brittle but necessary for models without native tool support."

### Q2: "The agent gets stuck in a loop: Call Tool -> Error -> Call Tool -> Error."
**Real World Answer**:
"The 'Death Spiral'.
**The Fixes**:
1. **Loop Limit**: We reduced `max_iterations` from 15 to 5.
2. **Error Message Enrichment**: Instead of returning 'Invalid Input', the tool returns 'Invalid Input: Phone number must be 10 digits.'
3. **Scratchpad Analysis**: We check the `agent_scratchpad`. If the last 3 actions are identical, we force a 'Stop' action to break the loop."

## Topics Excluded
*   **ReAct Implementation**: Writing the raw "Thought/Action/Observation" prompt loop manually. We used the high-level API.
*   **Tool Choice Enforcement**: Forcing the model to call a specific tool (e.g. `tool_choice="Search"`).p."

## Interview Questions & Concepts (SENIOR LEVEL)

### Q1: What is the differences between ReAct and OpenAI Functions?
**Answer**:
- **ReAct**: "Thought -> Action -> Observation". The model writes a monologue. Works on *any* model. Parsing is fragile (regex).
- **OpenAI Functions / Tool Calling**: The model outputs a structured JSON object intended for tools. It's an API-level feature. Much more robust.

### Q2: Why is `AgentExecutor` considered "legacy" compared to LangGraph?
**Answer**:
`AgentExecutor` is a "Black Box". You cannot easily intervene in the middle of the loop (e.g., asking user for confirmation before a dangerous tool call).
**Reflexion/LangGraph** allows you to define the loop explicitly as a graph, giving you control over every state transition.

### Q3: How do you prevent an Agent from looping forever?
**Answer**:
1. `max_iterations`: Hard limit (e.g. 5 steps).
2. `max_execution_time`: Time limit.
3. **Prompt Engineering**: System prompt "If you catch yourself repeating, stop and ask the user for help."
