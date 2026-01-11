import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

# --- 1. Define the Data Schema ---
# In Enterprise apps, we NEVER want raw strings. We want objects.
# Pydantic is the standard for data validation in Python.
class MovieReview(BaseModel):
    title: str = Field(description="The title of the movie being reviewed.")
    rating: int = Field(description="A rating from 1 to 10.")
    themes: List[str] = Field(description="A list of themes present in the movie (e.g., 'Love', 'War').")
    is_family_friendly: bool = Field(description="Whether the movie is suitable for children.")

def demonstrate_structured_output():
    """
    Shows how to force an LLM to return strictly formatted JSON data 
    that matches a Pydantic object.
    """
    
    # 1. Setup the Model
    model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

    # 2. Setup the Parser
    # This object is responsible for:
    #   a) Generating the "format_instructions" for the system prompt.
    #   b) Parsing the raw string response into a Python Object.
    parser = PydanticOutputParser(pydantic_object=MovieReview)

    # 3. Setup the Prompt
    # We use a ChatPromptTemplate to compose the System and User logic.
    # Notice `partial_variables`: We inject the format instructions here.
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a movie critic. Analyze the user's input and extract details. \n{format_instructions}"),
        ("user", "{user_input}")
    ]).partial(format_instructions=parser.get_format_instructions())

    print("--- 1. Prompt Format Instructions (Under the Hood) ---")
    # This is what gets sent to the LLM behind the scenes.
    print(parser.get_format_instructions()) 

    # 4. The Chain (LCEL Style)
    # The pipe '|' operator: Input -> Prompt -> Model -> Parser -> Output
    chain = prompt_template | model | parser

    user_review_text = "I just watched 'The Matrix'. It was mind-blowing! I give it a 9 out of 10. \
    It deals with reality simulation and AI rebellion. Definitely a bit violent for kids though."

    print(f"\n--- 2. Processing Input: '{user_review_text[:50]}...' ---")
    
    try:
        # invoke() runs the chain.
        structured_data: MovieReview = chain.invoke({"user_input": user_review_text})
        
        print("\n--- 3. Result (Real Python Object) ---")
        print(f"Title: {structured_data.title}")
        print(f"Rating: {structured_data.rating}/10")
        print(f"Themes: {structured_data.themes}")
        print(f"Family Friendly?: {structured_data.is_family_friendly}")
        
        # Verify it's actually an object, not a dict
        assert isinstance(structured_data, MovieReview)
        print("\nSuccess: Output is a valid Pydantic Model instance.")

    except Exception as e:
        print(f"Error parsing output: {e}")

if __name__ == "__main__":
    demonstrate_structured_output()
