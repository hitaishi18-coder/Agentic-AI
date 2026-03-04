# 06 Retrieval-Augmented Generation (RAG)

This directory contains a complete, working implementation of a Retrieval-Augmented Generation (RAG) pipeline. RAG allows Large Language Models (LLMs) to access and utilize external, custom data to answer questions accurately without hallucinating. 

In this specific example, the AI is grounded using a local PDF document about Node.js (`nodejs.pdf`).

## Overview

The RAG pipeline is broken down into two main phases, represented by the two Python scripts:
1.  **Data Ingestion & Indexing (`index.py`)**: Reading the document, breaking it into smaller pieces, converting those pieces into numbers (embeddings), and storing them in a database.
2.  **Retrieval & Generation (`chat.py`)**: Taking a user's question, finding the most relevant pieces of information from the database, and passing both the question and the retrieved context to the LLM to generate an answer.

## Architecture & Files

* **`docker-compose.yaml`**: Sets up a local instance of **Qdrant**, a high-performance open-source vector search engine, exposed on port `6333`.
* **`index.py`**: The ingestion script. It uses LangChain to:
    * Load the `nodejs.pdf` file using `PyPDFLoader`.
    * Split the document into manageable 1000-character chunks with a 400-character overlap using `RecursiveCharacterTextSplitter` to maintain context.
    * Convert the text chunks into vector embeddings using OpenAI's `text-embedding-3-large` model.
    * Store the resulting vectors in the local Qdrant database under the collection name `learning-rag`.
* **`chat.py`**: The interactive chat script. When a user asks a question, it:
    * Performs a similarity search against the Qdrant vector database to find the most relevant chunks.
    * Constructs a system prompt containing the retrieved context, page numbers, and file locations.
    * Sends the enriched prompt to `gpt-3.5-turbo` to generate a grounded response, explicitly instructing the AI to tell the user which page to check for more information.

## Prerequisites

1.  **Docker Desktop** must be installed and running.
2.  Install the required Python packages (ensure your virtual environment is active):
    ```bash
    pip install langchain-openai langchain-qdrant langchain-community langchain-text-splitters openai python-dotenv pypdf
    ```
3.  Ensure your `.env` file contains your `OPENAI_API_KEY`.

## Usage

Follow these steps strictly in order:

1.  **Start the Vector Database:**
    Open your terminal in this directory and start Qdrant in detached mode:
    ```bash
    docker-compose up -d
    ```

2.  **Index the Document:**
    Run the ingestion script to process the PDF and populate the database. *You only need to run this once.*
    ```bash
    python index.py
    ```
    You should see the output: `indexing of documents done...`

3.  **Chat with your Data:**
    Run the chat script to ask questions about the Node.js PDF:
    ```bash
    python chat.py
    ```
    Ask a question like: *"What is Node.js?"* or *"How do I install Node?"*

4.  **Cleanup (Optional):**
    When you are done, you can stop the vector database container:
    ```bash
    docker-compose down
    ```