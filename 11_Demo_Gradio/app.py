import gradio as gr
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# --- BACKEND LOGIC ---
model = ChatOpenAI(model="gpt-3.5-turbo")

def simple_chat(message, history):
    # History handling in Gradio is usually list of [user, bot] lists
    # We just use the last message for this simple demo
    response = model.invoke(message).content
    return response

def rag_chat(file, question):
    if not file:
        return "Please upload a PDF first."
    # Simulation of RAG logic from Module 3
    # 1. Load PDF, 2. Split, 3. Embed, 4. Retrieve
    return f"SIMULATED RAG ANSWER: I read '{file.name}' and the answer to '{question}' is: The document discusses AI Safety."

def agent_action(goal):
    # Simulation of Agent logic from Module 5/7
    steps = [
        "Thinking: Breaking down goal...",
        f"Action: Searching web for '{goal}'...",
        "Observation: Found 3 results.",
        "Final Answer: The data suggests..."
    ]
    # Generator for streaming updates
    log = ""
    for step in steps:
        time.sleep(1) # Simulate work
        log += step + "\n"
        yield log

# --- UI LAYOUT ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🦜🔗 LangChain Enterprise Demo (Gradio)")
    
    with gr.Tabs():
        # TAB 1: Simple Chat
        with gr.TabItem("💬 Basic Chat"):
            gr.ChatInterface(simple_chat)
        
        # TAB 2: RAG
        with gr.TabItem("📄 Doc Q&A (RAG)"):
            with gr.Row():
                pdf_input = gr.File(label="Upload PDF")
                rag_input = gr.Textbox(label="Ask a question about the PDF")
            rag_output = gr.Textbox(label="Answer")
            rag_btn = gr.Button("Analyze")
            rag_btn.click(rag_chat, inputs=[pdf_input, rag_input], outputs=rag_output)

        # TAB 3: Agent
        with gr.TabItem("🤖 Agent Simulator"):
            goal_input = gr.Textbox(label="Agent Goal (e.g. 'Research AI Trends')")
            agent_output = gr.Textbox(label="Execution Log", lines=10)
            agent_btn = gr.Button("Deploy Agent")
            agent_btn.click(agent_action, inputs=goal_input, outputs=agent_output)

if __name__ == "__main__":
    demo.launch()
