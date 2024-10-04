# Retrieval Augmented Generation - System

## Overview

- This project implements a Retrieval-Augmented Generation (RAG) system using Python and a frontend built with Nextjs - TypeScript, and advanced retrieval strategies: Multi-Query, RAG Fusion It leverages Qdrant and uses streaming responses to delivery queries to the frontend. The system allows documents to be uploaded to the system, as they are uploaded they are embedded and stored in the vector database.

## Project Structure

### rag-system-be - backend server application

- **`ebeddings.py`**

  - Generates embeddings for documents when they get updated
  - Splits documents into smaller chunks to index phrases.

- **`main.py`**

  - Setsup the Fastapi backend

- **`retrieval.py`**

  - Retrieves relevent parts of the document based upon user queries.
  - Handles retrieval strategies:
    - MultiQuery
    - RAG Fusion
  - Extracts user metadata

- **`storage.py`**

  - Handles storing and grabbing our embedding model, with Qdrant

- **`router.py`**
  - Holds our routes for the Fastapi server:
    - Streaming endpoint for making queries
    -

### rag-system-fe - frontend application (nextjs)

- Generic Nextjs app structure (App router + src directory)

## Running the application

1. **Setup environment variables**

   1. Ensure at the root of the directory, create a .env file and create a values:
      `OPENAI_API_KEY=YOURAPIKEY`
      `GUARDRAILS_API_KEY=YOURAPIKEY`


2. **Build the application**

   Ensure youre at the root directory of the project

   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. **Accessing the application**

   The frontend application is being hosted locally on port 3000:
   http://localhost:3000

4. **Storing Documents**
   - Uploading a document to the frontend automatically generates embeddings for us.

## Additions

- **Qdrant dashboard**
  - Check your qdrant data is populated after server start up here: http://localhost:6333/dashboard
