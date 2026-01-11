#!/usr/bin/env python
from fastapi import FastAPI
from langserve import add_routes
from packages.agent import pirate_agent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="LangChain Enterprise API",
    version="1.0",
    description="A production-ready API exposing AI Agents via LangServe",
)

# 1. Add Routes
# This automatically creates:
# - POST /pirate/invoke
# - POST /pirate/stream
# - POST /pirate/batch
# - GET  /pirate/playground (Interactive UI)
add_routes(
    app,
    pirate_agent,
    path="/pirate",
)

if __name__ == "__main__":
    import uvicorn
    # Start the server
    # Run: python 01_server.py
    # Visit: http://localhost:8000/pirate/playground
    uvicorn.run(app, host="0.0.0.0", port=8000)
