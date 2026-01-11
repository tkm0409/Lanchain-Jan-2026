import os
import base64
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

# ==========================================
# CONCEPT: Vision RAG
# 1. Encode Image to Base64
# 2. Ask GPT-4o to describe it
# 3. Index the description
# ==========================================

print("--- Lesson 3: Multimodal (Vision) RAG ---")

# 1. Helper to encode image
def encode_image(image_path):
    # In a real app, ensure file exists. 
    # Here we simulate with a dummy string if file missing.
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 2. The Vision Model
vision_model = ChatOpenAI(model="gpt-4o")

def summarize_image(curr_dir, filename="chart.png"):
    image_path = os.path.join(curr_dir, filename)
    base64_image = encode_image(image_path)
    
    if not base64_image:
        print("[Warn] No image found. Simulating Image Input.")
        return "Simulation: A bar chart showing sales growth of 50% in Q4."

    msg = vision_model.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": "Describe this image in detail for retrieval purposes."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ]
            )
        ]
    )
    return msg.content

# 3. Execution
print("Analyzing 'chart.png' (Simulated if missing)...")
description = summarize_image(os.getcwd())
print(f"\n[Generated Image Summary]:\n{description}")

print("\n[Next Steps]")
print("1. Embed this summary text: embeddings.embed_query(description)")
print("2. Store in ChromaDB with metadata {'original_image_path': 'chart.png'}")
print("3. On retrieval, pass the SUMMARY to the LLM, but show the IMAGE to the user.")
