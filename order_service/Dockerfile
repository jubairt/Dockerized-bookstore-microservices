FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency list and install first (for Docker cache efficiency)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project (app code, logs folder, .env)
COPY . .

# Expose the correct port for this service
EXPOSE 8003


# Start FastAPI app after a 10-second delay
CMD ["sh", "-c", "sleep 10 && uvicorn app.main:app --host 0.0.0.0 --port 8003"]