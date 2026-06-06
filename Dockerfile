# Use Python 3.10
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your backend code and the best.pt model
COPY . .

# Run the FastAPI server on port 7860 (Hugging Face requires port 7860)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]