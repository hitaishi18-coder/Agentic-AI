from dotenv import load_dotenv
from openai import OpenAI
import requests
from pydantic import BaseModel, Field
from typing import Optional
import json
import os

load_dotenv()

client = OpenAI()

def run_command(cmd: str):
    result = os.system(cmd)
    return result


available_tools = {
    "run_command": run_command
}

SYSTEM_PROMPT = """
    You are an expert AI Assistant resolving user queries using a Chain of Thought approach.
    You operate using START, PLAN, TOOL, and OUTPUT steps.
    
    Workflow:
    1. First, PLAN what needs to be done. You can have multiple PLAN steps to break down complex tasks.
    2. If you need to interact with the system or create files, you MUST output a TOOL step.
    3. Wait for the OBSERVE step (which contains the tool's output) before proceeding.
    4. Once all necessary steps are completed and verified via OBSERVE, provide the final OUTPUT.

    Rules & Constraints:
    - STRICT JSON FORMAT: Every response must strictly follow the defined JSON format.
    - ONE STEP AT A TIME: Output only one JSON object per turn.
    - ANTI-HALLUCINATION: NEVER output an OUTPUT step claiming a task is done unless you have actually executed the TOOL step and received a successful OBSERVE step.
    - OS CONTEXT: You are running in a stateless Windows cmd.exe environment. Do NOT use 'cd' to change directories, as it will reset immediately. Always use full relative paths (e.g., folder_name/file.ext).
    
    🔥 FILE CREATION PROTOCOL (CRITICAL) 🔥:
    Windows CMD cannot handle standard echo or powershell commands for code files due to special characters (<, >) and nested quotes.
    To create files, you MUST use this exact Python one-liner syntax:
    python -c "open('PATH_TO_FILE', 'w', encoding='utf-8').write('''[YOUR CONTENT HERE]''')"
    
    🚫 THE DOUBLE QUOTE BAN (CRITICAL) 🚫:
    Because the python command itself is wrapped in double quotes (python -c "..."), Windows CMD will CRASH if you use ANY double quotes (") inside your file content.
    You MUST write your entire HTML, CSS, JavaScript, or any other code using ONLY single quotes (').
    
    Correct Example (Single quotes inside):
    python -c "open('todo/index.html', 'w', encoding='utf-8').write('''<h1 class='title'>Hello World</h1>''')"
    
    CRASHES (Double quotes inside):
    python -c "open('todo/index.html', 'w', encoding='utf-8').write('''<h1 class="title">Hello World</h1>''')"

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string", "tool": "string", "input": "string" }

    Available Tools:
    - run_command(cmd: str): Takes a Windows cmd or python -c command as a string, executes it on the user's system, and returns the output.
    
    Example Execution:
    START: What is the weather of Delhi?
    PLAN: { "step": "PLAN", "content": "The user wants the weather for Delhi." }
    PLAN: { "step": "PLAN", "content": "I will check available tools and use get_weather." }
    TOOL: { "step": "TOOL", "tool": "get_weather", "input": "delhi" }
    OBSERVE: { "step": "OBSERVE", "tool": "get_weather", "output": "The temp of delhi is cloudy with 20 C" }
    PLAN: { "step": "PLAN", "content": "I have the weather info, now I can output it." }
    OUTPUT: { "step": "OUTPUT", "content": "The current weather in Delhi is 20 C with cloudy skies." }
"""

print("\n\n\n")

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None, description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call.")
    input: Optional[str] = Field(None, description="The input params for the tool")

message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]

while True:
    user_query = input("👉🏻 ")
    message_history.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.parse(
            model="gpt-4.1-nano",
            response_format=MyOutputFormat,
            messages=message_history
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result})
        
        parsed_result = response.choices[0].message.parsed

        if parsed_result.step == "START":
            print("🔥", parsed_result.content)
            continue

        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            print(f"🛠️: {tool_to_call} ({tool_input})")

            tool_response = available_tools[tool_to_call](tool_input)
            print(f"🛠️: {tool_to_call} ({tool_input}) = {tool_response}")
            message_history.append({ "role": "developer", "content": json.dumps(
                { "step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response}
            ) })
            continue



        if parsed_result.step == "PLAN":
            print("🧠", parsed_result.content)
            continue

        if parsed_result.step == "OUTPUT":
            print("🤖", parsed_result.content)
            break

print("\n\n\n")