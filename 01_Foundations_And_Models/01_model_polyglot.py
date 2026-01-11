import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables from .env file
# Ensure you have OPENAI_API_KEY, GOOGLE_API_KEY, ANTHROPIC_API_KEY, and HUGGINGFACEHUB_API_TOKEN set.
load_dotenv()

def demonstrate_polyglot_models():
    """
    Demonstrates how to swap between different LLM providers using LangChain's unified interface.
    This "Polyglot" capability is crucial for enterprise apps to avoid vendor lock-in.
    """
    
    # --- 1. Define the input messages ---
    # In LangChain, we rarely pass raw strings. We use Message objects.
    # SystemMessage: Sets the behavior/persona of the AI.
    # HumanMessage: The user's input.
    messages = [
        SystemMessage(content="You are a helpful coding tutor. Answer concisely."),
        HumanMessage(content="Explain what a 'closure' is in Python in one sentence.")
    ]

    print("--- 1. OpenAI (The Industry Standard) ---")
    # 'temperature' controls randomness (0.0 = deterministic, 1.0 = creative)
    try:
        gpt_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
        gpt_response = gpt_model.invoke(messages)
        print(f"GPT Response:\n{gpt_response.content}\n")
    except Exception as e:
        print(f"Skipping OpenAI: {e}")

    print("--- 2. Google Gemini (The Large Context King) ---")
    # Gemini often has massive context windows (up to 2M tokens).
    try:
        gemini_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        gemini_response = gemini_model.invoke(messages)
        print(f"Gemini Response:\n{gemini_response.content}\n")
    except Exception as e:
        print(f"Skipping Gemini: {e}")

    print("--- 3. Anthropic Claude (The Reasoning Specialist) ---")
    # Claude is known for high fidelity in coding and refusing unsafe prompts.
    try:
        claude_model = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0)
        claude_response = claude_model.invoke(messages)
        print(f"Claude Response:\n{claude_response.content}\n")
    except Exception as e:
        print(f"Skipping Anthropic: {e}")

    print("--- 4. Open Source / HuggingFace (The Privacy choice) ---")
    # HuggingFaceEndpoint accesses models hosted on the HF Hub.
    # For local inference (offline), you would use `HuggingFacePipeline` instead.
    try:
        # Using Mistral-7B as a high-quality open model example
        repo_id = "meta-llama/Llama-3.1-8B-Instruct"
        hf_model = HuggingFaceEndpoint(
            repo_id=repo_id, 
            temperature=0, 
            task="text-generation"
        )

        hf_model_chat = ChatHuggingFace(llm=hf_model)
        # Note: HF Endpoints sometimes take raw string inputs differently depending on the task,
        # but LangChain standardizes `invoke` to accept message lists for chat models if wrapped correctly.
        # For raw endpoints, it often expects a string prompt.
        hf_response = hf_model_chat.invoke(messages)
        print(f"HF Mistral Response:\n{hf_response}\n") # HF often returns raw string, not AIMessage
    except Exception as e:
        print(f"Skipping HuggingFace: {e}")

if __name__ == "__main__":
    demonstrate_polyglot_models()
