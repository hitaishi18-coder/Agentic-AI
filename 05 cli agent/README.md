# 05 - CLI Agent: The System Operator 💻

This module demonstrates a powerful (and potentially dangerous) AI Agent that can directly interact with your computer's operating system using the **Command Line Interface (CLI)**.

---

## 📘 Theory: System-Interfacing Agents

While the Weather Agent could talk to an API, a **CLI Agent** can talk to your **Operating System**. It can create files, run scripts, check system stats, and more.

### Key Concepts:
1.  **System Calls**: Using Python's `os` or `subprocess` modules to execute shell commands.
2.  **Autonomous Execution**: The ability of an agent to decide *which* command to run based on a user's high-level request (e.g., "Create a new react project").
3.  **Risk & Safety**: Agents with system access can accidentally delete files or run harmful code. In a real-world scenario, these should be run in a **sandbox** (like Docker).

---

## 🛠️ Imports & Libraries

- `os`: Used to interact with the OS and run commands via `os.system`.
- `json`: To format the tool outputs before feeding them back to the LLM.
- `pydantic`: For structured data validation.
- `openai`: Specifically the `.parse()` method for model-native JSON support.

```python
import os
import json
from openai import OpenAI
from pydantic import BaseModel
```

---

## 💻 Code Explanation (Simplified)

### 1. The Power Tool: `run_command`
This simple function takes a string (the command) and executes it on your machine.
```python
def run_command(cmd: str):
    result = os.system(cmd) # Runs the command in your shell!
    return result
```

### 2. The Thought Process (CoT)
The agent follows a strict loop defined in its `SYSTEM_PROMPT`:
1.  **PLAN**: "I need to list the files in this directory to see what's inside."
2.  **TOOL**: Calls `run_command` with input `dir` (Windows) or `ls` (Mac/Linux).
3.  **OBSERVE**: Receives the list of files.
4.  **OUTPUT**: Tells the user what it found.

### 3. Structured Communication
We use a `Pydantic` model to ensure the AI always gives us a `step`, `content`, `tool`, and `input`. If it doesn't, the code will throw an error, preventing "hallucinations" of the format.

---

## 📜 Full Code Listing: `main.py` (Logic)

```python
class MyOutputFormat(BaseModel):
    step: str
    content: Optional[str]
    tool: Optional[str]
    input: Optional[str]

# The Reasoning Loop
while True:
    response = client.chat.completions.parse(
        model="gpt-4o",
        response_format=MyOutputFormat,
        messages=message_history
    )
    parsed_result = response.choices[0].message.parsed

    if parsed_result.step == "TOOL":
        # DANGEROUS: Executes the command provided by the AI
        output = run_command(parsed_result.input)
        # Feed the result back to the AI as a 'developer' role
        message_history.append({"role": "developer", "content": json.dumps({"output": output})})
```

---

## 🚀 How to Run

1.  **Preparation**:
    - Ensure your `.env` file has your `OPENAI_API_KEY`.
2.  **Install dependencies**:
    ```bash
    pip install openai pydantic python-dotenv requests
    ```
3.  **Run the CLI Agent**:
    ```bash
    python main.py
    ```
    *Input example: "Create a folder named 'test_from_ai' and then list all files here."*

---

## ⚠️ Safety Warning
This agent has the power to run commands on your machine. **Use with caution.** Never give a CLI agent access to production servers or sensitive folders without strict supervision or a sandboxed environment.

---

## 🎯 Summary
We've successfully built an agent that bridges the gap between **natural language** and **system automation**. This is the foundation of tools like "Open Interpreter" or "Devin".