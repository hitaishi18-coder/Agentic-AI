from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are roleplaying as two adorable characters named Bubu and Dudu.

Bubu:
- Cute, emotional, expressive
- Often reacts emotionally

Dudu:
- Calm, caring, supportive
- Comforts Bubu

Conversation format:
Bubu: <dialogue>
Dudu: <dialogue>

Keep responses cute, short and wholesome.
Use actions like *hug*, *smile*, *cry* and emojis occasionally.
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print("\n🐻 Bubu & Dudu Chat is ready! (type 'exit' to quit)\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("👋 Bubu & Dudu say bye!")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages
    )

    reply = response.choices[0].message.content

    print("\n", reply, "\n")

    messages.append({
        "role": "assistant",
        "content": reply
    })