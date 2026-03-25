from dotenv import load_dotenv
from mem0 import Memory
import os
from openai import OpenAI
import json

#  Fix for Python 3.13 deadlock
import openai.resources.chat

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

# OpenRouter-compatible client
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

# configuration
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "text-embedding-3-small"
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "openai/gpt-4o-mini",
            "max_tokens": 100
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "neo4j+s://a862b4e7.databases.neo4j.io",
            "username": "a862b4e7",
            "password": "teoRu669QLsRnk8skt8z9fyGmED8zSZ22YJvaGqZ0j4"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

# creating a memory client
memory_client = Memory.from_config(config)

while True:
    # input from user
    user_query = input(" > ")

    search_memory = memory_client.search(
        query=user_query,
        user_id="hitaishi"
    )

    #  FIXED quotes + safe fallback
    memories = [
        f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}"
        for mem in search_memory.get("results", [])
    ]

    print("memories found ", memories)

    SYSTEM_PROMPT = f"""
    Here is the context about the user:
    {json.dumps(memories)}
    """

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ],
        max_tokens=100,
    )

    # ai response
    ai_response = response.choices[0].message.content
    print("ai response", ai_response)

    memory_client.add(
        user_id="hitaishi",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response}
        ],
    )

    print("memory is saved!")