# Base Image
FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Install dependencies
# In a real app, you'd COPY requirements.txt .
RUN pip install langchain-openai langchain fastapi uvicorn "langserve[all]" python-dotenv

# Copy application code
COPY ./app /code/app
COPY ./packages /code/packages

# Expose port
EXPOSE 8000

# Run the application
# We use module syntax (-m) to ensure imports resolve correctly
CMD ["python", "-m", "app.server"]
