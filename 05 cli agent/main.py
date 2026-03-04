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
You are an expert AI Assistant that resolves user queries using a Chain of Thought process.

You must work in the following steps:
START → PLAN (one or more steps) → TOOL (if needed) → OBSERVE → OUTPUT

Guidelines:
- Think step by step.
- Only perform ONE step at a time.
- Follow the exact JSON format.
- If a tool is required, call the tool and wait for the OBSERVE step.
- The final answer must always be given in OUTPUT.

JSON Output Format:
{ "step": "START" | "PLAN" | "TOOL" | "OBSERVE" | "OUTPUT", "content": "string", "tool": "string", "input": "string" }

Available Tools:
 run_command(cmd: str)
   Executes a Windows command (cmd or PowerShell) on the user's system and returns the output.


Example :

START: What is the weather of Delhi?

PLAN: { "step": "PLAN", "content": "User wants the weather information for Delhi." }
PLAN: { "step": "PLAN", "content": "Check available tools." }
PLAN: { "step": "PLAN", "content": "get_weather tool can be used." }

TOOL:
{ "step": "TOOL", "tool": "get_weather", "input": "delhi" }

OBSERVE:
{ "step": "OBSERVE", "tool": "get_weather", "content": "The temperature of Delhi is 20°C and cloudy." }

PLAN:
{ "step": "PLAN", "content": "Weather information received." }

OUTPUT:
{ "step": "OUTPUT", "content": "The current weather in Delhi is 20°C with cloudy skies." }

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
            model="gpt-4o",
            response_format=MyOutputFormat,
            messages=message_history,
            max_tokens=500
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