# 10 - Memory Agent: Persistent User Personalization 🧠

This module introduces **Mem0**, a self-improving memory layer for LLM applications. It allows your AI agent to remember user preferences, past interactions, and context across different sessions, making it feel truly personal.

---

## 📘 Theory: What is Mem0?

Standard LLMs are "stateless"—they forget everything as soon as the conversation ends. **Mem0** provides a persistent "memory" that stores information about the user and retrieves it when needed.

### Why use Memory?
1.  **Personalization**: The agent remembers your name, likes, dislikes, and past tasks.
2.  **Continuity**: You don't have to repeat yourself in every new chat.
3.  **Self-Correction**: The agent can learn from its mistakes and improve over time.

### How it Works:
- **Embedder**: Converts text into vectors (numbers) to understand "meaning."
- **Vector Store (Qdrant)**: A specialized database that stores these vectors and allows for "similarity search."
- **LLM**: Uses the retrieved "memories" as context to generate personalized responses.

---

## 🛠️ Imports & Libraries

- `mem0`: The core library for managing agent memory.
- `openai`: Used to communicate with the LLM (OpenAI or OpenRouter).
- `dotenv`: To securely load API keys from a `.env` file.
- `qdrant-client`: To connect to the Qdrant vector database.

```python
from mem0 import Memory
from openai import OpenAI
from dotenv import load_dotenv
```

---

## 💻 Code Explanation (Simplified)

### 1. Configuration ⚙️
We define how the memory should behave. We tell it to use **OpenAI** for embeddings and **Qdrant** (running on `localhost:6333`) to store information.
```python
config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {"host": "localhost", "port": 6333}
    }
}
memory_client = Memory.from_config(config)
```

### 2. Searching Memory 🔍
Before answering, the agent looks for anything it already knows about the user (`user_id="hitaishi"`).
```python
search_memory = memory_client.search(query=user_query, user_id="hitaishi")
```

### 3. Personalizing the Prompt 📝
The retrieved memories are added to the **System Prompt**. This gives the LLM the "context" it needs to be smart.
```python
SYSTEM_PROMPT = f"Here is the context about the user: {memories}"
```

### 4. Updating Memory 💾
After the conversation, the agent saves the new interaction so it can remember it next time.
```python
memory_client.add(user_query, user_id="hitaishi")
```

---

## 📜 Full Code Listing: `memory.py`

```python
from dotenv import load_dotenv
from mem0 import Memory
import os
from openai import OpenAI
import json

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenRouter-compatible client
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=os.getenv("OPENAI_BASE_URL")
)

# configuration for mem0
config = {
    "version" : "v1.1",
    "embedder" : {
        "provider": "openai",
        "config" : { 
            "api_key" : OPENAI_API_KEY, 
            "model" : "text-embedding-3-small"
        }
    },
    "llm" : {
        "provider" : "openai",
        "config" : { 
            "api_key" : OPENAI_API_KEY, 
            "model" : "gpt-4.1-mini"   
        }
    },
    "vector_store" : {
        "provider" : "qdrant",
        "config" : {
            "host": "localhost",
            "port": 6333
        }
    }
}

# creating a memory client 
memory_client = Memory.from_config(config)

while True:
    user_query = input(" > ")

    # search relevant memories 
    search_memory = memory_client.search(query=user_query, user_id="hitaishi")   

    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}" 
        for mem in search_memory.get("results")
    ]

    print("Memories retrieved: ", len(memories))

    SYSTEM_PROMPT = f"""
        Here is the context about the user:
        {json.dumps(memories)}
        
        Answer the user's query based on this context.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system","content": SYSTEM_PROMPT},
            {"role":"user", "content": user_query}
        ],
    )
    
    ai_response = response.choices[0].message.content
    print("\nAI Response:", ai_response)

    # Save today's conversation for tomorrow
    memory_client.add(user_query, user_id="hitaishi")
    print("\n[System: Memory saved!]\n")
```

---

## 🚀 How to Run

1.  **Start the Vector Database**:
    This project uses **Qdrant**. Start it using Docker:
    ```bash
    docker compose up -d
    ```
    *Or use:* `docker run -p 6333:6333 qdrant/qdrant`

2.  **Install dependencies**:
    ```bash
    pip install mem0ai openai python-dotenv qdrant-client
    ```

3.  **Setup your `.env`**:
    Add your `OPENAI_API_KEY` and `OPENAI_BASE_URL` (if using OpenRouter).

4.  **Run the script**:
    ```bash
    python memory.py
    ```

---

## 🎯 Summary
By integrating **Mem0** and **Qdrant**, we've transformed a generic chatbot into a **Persistent Memory Agent**. It doesn't just process text; it learns about the user over time, leading to a much more natural and helpful user experience.


## output
<img width="649" height="381" alt="Screenshot 2026-03-25 002309" src="https://github.com/user-attachments/assets/61c312bc-d11b-4dd0-927b-35d794be254a" />

<img width="1920" height="1080" alt="Screenshot 2026-03-25 002322" src="https://github.com/user-attachments/assets/1b5d6d33-24d9-4b3f-af82-85e8549c6c0a" />
