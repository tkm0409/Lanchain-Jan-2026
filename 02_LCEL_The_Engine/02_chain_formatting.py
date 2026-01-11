from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# --- The Standard Pattern ---
# In 90% of LangChain apps, the pattern is:
# Prompt -> Model -> OutputParser

def demonstrate_simple_chain():
    # 1. Model
    model = ChatOpenAI(model="gpt-4o", temperature=0)

    # 2. Prompt
    # We define inputs {topic} and {language}
    prompt = ChatPromptTemplate.from_template(
        "Tell me a short joke about {topic} in {language}."
    )

    # 3. Output Parser
    # Basics: ChatModels return a MESSAGE object (AIMessage(content="...")).
    # StrOutputParser converts that Message -> String.
    parser = StrOutputParser()

    # 4. Chain
    # The dictionary provided to invoke() is passed to the FIRST item (Prompt).
    chain = prompt | model | parser

    print("--- Invoking Chain ---")
    result = chain.invoke({"topic": "ice cream", "language": "Italian"})
    print(f"Result Type: {type(result)}")
    print(f"Content: {result}")

    # --- 5. Advanced: Composition ---
    # What if we want to chain TWO calls?
    # Step 1: Generate Joke -> Step 2: Explain why it's funny.
    
    analysis_prompt = ChatPromptTemplate.from_template(
        "Explain the cultural context of this joke: {joke}"
    )
    
    # We use RunnablePassthrough or just pipe the specific flow
    composed_chain = (
        {"joke": chain} # The output of the first chain becomes the input 'joke'
        | analysis_prompt
        | model
        | StrOutputParser()
    )
    
    print("\n--- Invoking Composed Chain ---")
    analysis = composed_chain.invoke({"topic": "politics", "language": "English"})
    print(analysis)

if __name__ == "__main__":
    demonstrate_simple_chain()
