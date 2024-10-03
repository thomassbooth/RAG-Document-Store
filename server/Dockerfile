FROM python:3.11-slim

# Install curl and git
RUN apt-get update && apt-get install -y curl git

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Setup Guardrails with the environment variable
ARG GUARDRAILS_API_KEY
RUN guardrails configure --token ${GUARDRAILS_API_KEY} --disable-metrics --disable-remote-inferencing

#install the different guardrails dependencies
RUN guardrails hub install hub://guardrails/toxic_language

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Run the FastAPI app using uvicorn with hot reloading
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
