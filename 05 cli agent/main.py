from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import re

load_dotenv()

# ---------------- GROQ CLIENT ----------------

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- TOOL ----------------

def run_command(cmd: str):
    try:
        output = os.popen(cmd).read()
        return output.strip() if output.strip() else "Command executed successfully."
    except Exception as e:
        return str(e)

available_tools = {
    "run_command": run_command
}

# ---------------- SYSTEM PROMPT ----------------

SYSTEM_PROMPT = """
You are a CLI AI Agent.

STRICT RULES:
- Follow: START → PLAN → TOOL → OBSERVE → PLAN → OUTPUT
- Return ONLY valid JSON.
- Do NOT return explanations.
- Do NOT wrap JSON in markdown.
- Only ONE step at a time.

JSON FORMAT:

{
  "step": "START" | "PLAN" | "TOOL" | "OUTPUT",
  "content": "string",
  "tool": "string",
  "input": "string"
}
"""

# ---------------- JSON EXTRACTOR ----------------

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group(0)
    return None

# ---------------- MESSAGE HISTORY ----------------

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

# ---------------- MAIN LOOP ----------------

while True:
    user_query = input("💻 CLI Agent 👉🏻 ")
    message_history.append({"role": "user", "content": user_query})

    retry_count = 0
    MAX_RETRY = 5

    while True:
        # FIX 1: Use a valid Groq model ID (e.g., llama3-70b-8192, mixtral-8x7b-32768, or qwen-2.5-32b)
        response = client.chat.completions.create(
            model="llama3-70b-8192", 
            messages=message_history,
            temperature=0
        )

        raw_output = response.choices[0].message.content

        json_string = extract_json(raw_output)

        if not json_string:
            retry_count += 1
            print("❌ No JSON found. Retrying...")
            if retry_count >= MAX_RETRY:
                print("⚠ Too many failures. Aborting.")
                break
            continue

        try:
            parsed = json.loads(json_string)
        except json.JSONDecodeError:
            retry_count += 1
            print("❌ Broken JSON. Retrying...")
            if retry_count >= MAX_RETRY:
                print("⚠ Too many failures. Aborting.")
                break
            continue

        message_history.append({"role": "assistant", "content": json_string})

        step = parsed.get("step")

        # FIX 2: Added the START step handler so the loop doesn't silently skip it
        # ---------------- START ----------------
        if step == "START":
            print("🔥", parsed.get("content"))
            continue

        # ---------------- PLAN ----------------
        if step == "PLAN":
            print("🧠", parsed.get("content"))
            continue

        # ---------------- TOOL ----------------
        if step == "TOOL":
            tool_name = parsed.get("tool")
            tool_input = parsed.get("input")

            if tool_name not in available_tools:
                print("❌ Unknown tool")
                break

            print(f"🛠 Running: {tool_input}")

            tool_response = available_tools[tool_name](tool_input)

            print(f"🛠 Result: {tool_response}")

            # FIX 3: Changed role from "developer" to "system" as Groq doesn't support "developer"
            message_history.append({
                "role": "system", 
                "content": json.dumps({
                    "step": "OBSERVE",
                    "tool": tool_name,
                    "input": tool_input,
                    "output": tool_response
                })
            })
            continue

        # ---------------- OUTPUT ----------------
        if step == "OUTPUT":
            print("🤖", parsed.get("content"))
            break