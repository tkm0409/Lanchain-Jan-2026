import os
import json
from typing import List
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, messages_to_dict, messages_from_dict, HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

# ==========================================
# Challenge 1: The "Forgetful" Bot (Sliding Window)
# ==========================================
print("--- Challenge 1: Sliding Window Memory ---")

class SlidingWindowHistory(BaseChatMessageHistory):
    """InMemory history that only keeps the last K interactions."""
    def __init__(self, k=2):
        self.messages = []
        self.k = k # Window size

    def add_messages(self, messages: List[BaseMessage]):
        self.messages.extend(messages)
        # Prune
        if len(self.messages) > self.k * 2: # *2 because 1 interaction = Human + AI
            self.messages = self.messages[-(self.k * 2):]
            print(f"[Memory] Pruned! Keeping last {len(self.messages)} messages.")

    def clear(self):
        self.messages = []

# Usage with Runnable
formatted_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])
model = ChatOpenAI(model="gpt-3.5-turbo")
chain = formatted_prompt | model

# Store history instances
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = SlidingWindowHistory(k=1) # VERY Short memory (1 turn)
    return store[session_id]

app = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="question", history_messages_key="history")

# Test
session_id = "user_1"
print(app.invoke({"question": "My name is Bob."}, config={"configurable": {"session_id": session_id}}).content)
print(app.invoke({"question": "What is 1+1?"}, config={"configurable": {"session_id": session_id}}).content)
print(app.invoke({"question": "What is my name?"}, config={"configurable": {"session_id": session_id}}).content) 
# Should FAIL to know name because window K=1 means it forgot "Bob" after "1+1"


# ==========================================
# Challenge 3: Persistent File Storage
# ==========================================
print("\n--- Challenge 3: File Persistence ---")

class FileChatHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, file_path: str = "chat_history.json"):
        self.session_id = session_id
        self.file_path = file_path
        self.messages = []
        self.load()

    def add_messages(self, messages: List[BaseMessage]):
        self.messages.extend(messages)
        self.save()

    def clear(self):
        self.messages = []
        self.save()

    def save(self):
        # Load existing data
        data = {}
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                try:
                    data = json.load(f)
                except:
                    pass
        # Update current session
        data[self.session_id] = messages_to_dict(self.messages)
        with open(self.file_path, "w") as f:
            json.dump(data, f)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                try:
                    data = json.load(f)
                    if self.session_id in data:
                        self.messages = messages_from_dict(data[self.session_id])
                except:
                    pass

# Test
history = FileChatHistory("user_persistent")
history.add_messages([HumanMessage(content="I persist across restarts!")])
print(f"Loaded from file: {history.messages}")
