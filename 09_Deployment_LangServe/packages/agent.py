from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# This file represents a reusable "Package" or "Library"
# In a real repo, this might be pip-installable.

model = ChatOpenAI(model="gpt-3.5-turbo")

prompt = ChatPromptTemplate.from_template(
    "You are a helpful pirate assistant. Answer the user question briefly in pirate speak.\n\nUser: {text}"
)

# A simple chain
pirate_agent = prompt | model | StrOutputParser()

# A more complex chain could go here
# ...
