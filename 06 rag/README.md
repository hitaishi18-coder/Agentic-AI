# 06 - RAG: Chatting with your Documents 📚

This module implements **Retrieval Augmented Generation (RAG)**, a technique that gives LLMs access to private or data-intensive files (like a 100-page PDF) without training a new model.

---

## 📘 Theory: What is RAG?

LLMs have a knowledge cutoff and can't see your private files. RAG solves this by "retrieving" relevant parts of your document and "augmenting" the prompt with that information.

### The RAG Pipeline:
1.  **Index (The Library)**:
    - **Load**: Read the PDF (e.g., `nodejs.pdf`).
    - **Split (Chunking)**: Break the text into smaller, overlapping chunks (e.g., 1000 characters).
    - **Embed**: Convert those text chunks into numbers (vectors) using an **Embedding Model**.
    - **Store**: Save these vectors in a **Vector Database** (Qdrant, Pinecone, Chroma).
2.  **Chat (The Librarian)**:
    - **Retrieve**: The user asks a question. We convert the question into a vector and find the "most similar" chunks in our Vector DB.
    - **Augment**: Send the question + the retrieved chunks as "context" to the LLM.
    - **Generate**: The LLM answers based *only* on the provided context.

---

## 🛠️ Imports & Libraries

- `langchain`: A framework for building LLM apps.
- `PyPDFLoader`: To extract text from PDF files.
- `RecursiveCharacterTextSplitter`: To intelligently break down large documents.
- `OpenAIEmbeddings`: To convert text into 1536-dimensional (or more) vectors.
- `QdrantVectorStore`: To store and search through vectors.
- `qdrant-client`: The client to connect to the Qdrant database.

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
```

---

## 💻 Code Explanation (Simplified)

### 1. Indexing (`index.py`)
This script prepares our data. It reads the `nodejs.pdf`, splits it into chunks of 1000 characters, and stores them in **Qdrant** (running on localhost:6333).
```python
# Create the index
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning-rag"
)
```

### 2. Chatting (`chat.py`)
When you ask a question, this script looks for the top 4 most relevant chunks from Qdrant, styles them as a "Context", and asks the LLM to answer using *that* context.
```python
# Similarity search
search_results = vector_db.similarity_search(query=user_query)

# Combine results into context
context = "\n\n".join([r.page_content for r in search_results])

# Send to LLM with the context
SYSTEM_PROMPT = f"Answer based on this context: {context}"
```

---

## 📜 Full Code Listing: `index.py` (Snippet)

```python
# loading pdf
loader = PyPDFLoader(file_path="nodejs.pdf")
docs = loader.load()

# splitting
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)

# indexing
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
    url="http://localhost:6333",
    collection_name="learning-rag"
)
```

---

## 🚀 How to Run

1.  **Start the Vector Database**:
    You need **Qdrant** running. Use Docker:
    ```bash
    docker run -p 6333:6333 qdrant/qdrant
    ```
2.  **Install dependencies**:
    ```bash
    pip install langchain-openai langchain-community langchain-qdrant pypdf qdrant-client python-dotenv
    ```
3.  **Prepare the Data**:
    ```bash
    python index.py
    ```
4.  **Start Chatting**:
    ```bash
    python chat.py
    ```

---

## ⚠️ Important Notes
- **Qdrant**: Ensure your Qdrant container is running before executing the scripts.
- **Matching Collections**: Make sure the `collection_name` in `index.py` and `chat.py` match exactly (e.g., both use `learning-rag`).
- **Model Names**: In `chat.py`, ensure the `model="gpt-4o"` (or another valid model name) is used.

---

## 🎯 Summary
RAG is the "standard" way to build enterprise AI applications. It allows us to give AI "domain-specific knowledge" without the high cost of fine-tuning or training.
