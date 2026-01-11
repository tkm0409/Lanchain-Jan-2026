# Module 5 Tasks: Agents & Tools

## Challenge 1: The "Secure" Shell Tool
**Goal**: Create a custom tool that executes shell commands BUT blocks dangerous ones.
- **Requirements**:
    - Define `RunShellCommand` tool.
    - Input: `command` (str).
    - Validation: If `rm`, `sudo`, or `chmod` is in the string, raise a `ValueError("Dangerous command blocked")`.
    - Test: Ask the agent to "list files" (should work) and "delete header.txt" (should fail).

## Challenge 2: The "Travel" Agent (Multi-Input Tool)
**Goal**: Create a tool with a complex schema key.
- **Requirements**:
    - Tool `BookFlight(origin: str, destination: str, date: str)`.
    - Tool `LookupHotel(location: str)`.
    - Ask the agent: "I want to go from NY to London on Friday. Book the flight and find a hotel."
    - Verify it calls *both* tools with the correct arguments.

## Challenge 3: Structure Fixer
**Goal**: Agent fails to call tool correctly.
- **Requirements**:
    - Create a tool `calculate_tax(amount: int)`.
    - Manually invoke the tool with a string: `calculate_tax("100 dollars")`.
    - It should error.
    - Catch the error and pass it back to the agent: *"Error: 100 dollars is not a valid integer. Call the tool again with just the number."*
    - The agent should self-correct.
