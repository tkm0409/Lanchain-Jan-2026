from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

# --- Concept: Session Memory ---
# The Model itself doesn't remember you.
# We must re-send the entire conversation history every time.
# LangChain manages this via "RunnableWithMessageHistory".

# 1. The Store
# In production, this would be Redis, Postgres, or DynamoDB.
# Here, we use a simple in-memory dictionary.
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def demonstrate_modern_memory():
    model = ChatOpenAI(model="gpt-4o", temperature=0)

    # 2. The Prompt
    # We MUST include a placeholder for history.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. You answer in pirate speak."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    chain = prompt | model

    # 3. The Wrapper
    # This automatically:
    # a) Fetches history for 'session_id'
    # b) Injects it into 'history' key in prompt
    # c) Appends the new HumanInput and AIResponse to the history
    with_message_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    # 4. Usage
    # We pass a 'config' with the session_id
    config = {"configurable": {"session_id": "user_123"}}

    print("--- Message 1 ---")
    response1 = with_message_history.invoke(
        {"input": "Hi! My name is Tharun."},
        config=config
    )
    print(response1.content)

    print("\n--- Message 2 (Testing Memory) ---")
    response2 = with_message_history.invoke(
        {"input": "What is my name?"},
        config=config
    )
    print(response2.content)

    print("\n--- Message 3 (New Session) ---")
    config_new = {"configurable": {"session_id": "user_999"}}
    response3 = with_message_history.invoke(
        {"input": "What is my name?"},
        config=config_new
    )
    print(response3.content) # Should NOT know the name

if __name__ == "__main__":
    demonstrate_modern_memory()
