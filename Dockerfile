# Use the official Playwright Docker image as the base
FROM mcr.microsoft.com/playwright/python:v1.59.0-jammy

WORKDIR /app

# Install dependencies as root to avoid permission errors
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Hugging Face requires running as UID 1000. 
# The Playwright image already has a user with UID 1000 built-in (named 'pwuser').
# We give this user ownership of our app folder, then switch to it.
RUN chown -R 1000:1000 /app
USER 1000

# Expose port 7860 (Hugging Face standard)
EXPOSE 7860

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
