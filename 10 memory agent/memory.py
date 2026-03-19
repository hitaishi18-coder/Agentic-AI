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

# configuration very important ... it tells what to connect how to connect 
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
            "model" : "openai/gpt-4o-mini"   
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
    # input from user 
    user_query = input(" > ")

    search_memory = memory_client.search(query=user_query, user_id="hitaishi")   # only find relevant memories 

    memories = [
        f"ID: {mem.get("id")}\nMemory: {mem.get("memory")}" 
        for mem in search_memory.get("results")
    ]

    print("memories found ", memories)

    SYSTEM_PROMPT = f"""
        Here is the context about the user:
        {json.dumps(memories)}
    """


    response = client.chat.completions.create(
    model="openai/gpt-4o-mini",  
    messages=[
        {"role":"system","content": SYSTEM_PROMPT},
        {"role":"user", "content": user_query}
    ],
    max_tokens=30,
    temperature=0.7
    )

    # ai response 
    ai_response = response.choices[0].message.content
    print("ai response", ai_response)

    memory_client.add(
    user_id="hitaishi",
    messages=[
        {"role":"user","content":user_query},
        {"role":"assistant","content":ai_response}
    ],
    
    )

    print("memory is saved!")