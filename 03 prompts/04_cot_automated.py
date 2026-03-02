from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI() 

SYSTEM_PROMPT="""
You are an expert AI Assistant in resolving user queries using chain of thought. 

You work on START, PLAN, and OUTPUT steps. 
You need to first PLAN what needs to be done. The PLAN can take multiple steps.
Once you think enough PLAN has been done, finally you can give the OUTPUT.

Rules:
- Strictly follow the given JSON output format.
- Only run one step at a time per response.
- The sequence of steps is START (where user gives an input), PLAN (can be multiple times), and finally the OUTPUT.

Output JSON Format:
{"step": "START" | "PLAN" | "OUTPUT", "content": "your thought or final response here"}

Example conversation flow:
User: can you solve 2 + 3 * 5 / 10
Assistant: {"step": "PLAN", "content": "seems like user is interested in a maths problem"}
Assistant: {"step": "PLAN", "content": "looking at the problem, we should solve this using BODMAS method"}
Assistant: {"step": "PLAN", "content": "first, we must multiply 3 * 5 which is 15"}
Assistant: {"step": "PLAN", "content": "the new equation is 2 + 15 / 10"}
Assistant: {"step": "PLAN", "content": "we must perform divide that is 15/10 = 1.5"}
Assistant: {"step": "PLAN", "content": "now the equation is 2 + 1.5"}
Assistant: {"step": "PLAN", "content": "now finally lets perform the add to get 3.5"}
Assistant: {"step": "OUTPUT", "content": "The answer is 3.5"}
"""

print("\n\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

user_query = input("👉 ")
message_history.append({"role": "user", "content": user_query})

while True:
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano", # Note: Ensure this model supports json_object on OpenRouter
            response_format={"type": "json_object"},
            messages=message_history
        )
        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result})
        
        parsed_result = json.loads(raw_result)

        step_type = parsed_result.get("step")
        content = parsed_result.get("content")

        if step_type == "START":
            print("🔥", content)
        elif step_type == "PLAN":
            print("🧠", content)
        elif step_type == "OUTPUT":
            print("🤖", content)
            break
        else:
            print("⚠️ Unknown step:", parsed_result)
            break
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parsing Error: {e}\nRaw output was: {raw_result}")
        break
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        break

print("\n\n\n")