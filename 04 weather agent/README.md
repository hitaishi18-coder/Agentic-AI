# 04 - Weather Agent: Agents & Tool Use 🌦️

This module takes LLMs to the next level by giving them the ability to **interact with the real world** using tools (APIs).

---

## 📘 Theory: What is an AI Agent?

An AI Agent is more than just a chatbot. It is an LLM equipped with **tools** and a **reasoning loop**. Instead of just talking, the agent can:
1.  **Reason**: Figure out what needs to be done.
2.  **Act**: Call a tool (like a weather API).
3.  **Observe**: Look at the results of the tool.
4.  **Repeat**: Decide if more steps are needed or if it can give the final answer.

### Key Concepts:
-   **Tool/Function Calling**: Providing the LLM with a list of functions it can use.
-   **Structured Output**: Forcing the LLM to reply in a specific format (like JSON) so our code can parse it.
-   **ReAct Pattern**: (Reason + Act) A popular framework where agents alternate between planning and taking actions.

---

## 🛠️ Imports & Libraries

- `requests`: To make actual HTTP calls to the Open-Meteo weather API.
- `pydantic`: To define the `MyOutputFormat` schema for structured responses.
- `openai`: To use the `.parse()` method for guaranteed JSON structure.

---

## 💻 Code Explanation (Simplified)

### 1. The Tool (`get_weather`)
A standard Python function that calls a real-world API to get latitude, longitude, and then the current temperature of a city.
```python
def get_weather(city: str):
    # 1. Get Lat/Lon (Geocoding)
    # 2. Get Weather (Forecast API)
    return f"The weather in {city} is 25°C"
```

### 2. Simple Routing (`agent_one.py`)
Uses basic Python `if "weather" in user_query:` logic to decide when to call the tool. This is a "pseudo-agent".

### 3. Reasoning Loop (`agent_two(cot).py`)
This is a **real AI Agent**. It uses a `while True` loop and a `SYSTEM_PROMPT` that tells the AI to follow these steps:
- **PLAN**: Think about what to do.
- **TOOL**: If it needs weather, it outputs a JSON asking to call `get_weather`.
- **OBSERVE**: Our code runs the tool and feeds the result back to the AI.
- **OUTPUT**: Once it has the info, it gives the final answer.

---

## 📜 Full Code Listing: `agent_two(cot).py` (Core Loop)

```python
while True:
    response = client.chat.completions.parse(
        model="gpt-4o",
        response_format=MyOutputFormat, # Structured output!
        messages=message_history
    )
    parsed_result = response.choices[0].message.parsed

    if parsed_result.step == "TOOL":
        # Call the Python function manually
        result = get_weather(parsed_result.input)
        # Feed the result back to the AI
        message_history.append({"role": "developer", "content": result})
        
    if parsed_result.step == "OUTPUT":
        print("Final Answer:", parsed_result.content)
        break
```

---

## 🚀 How to Run

1.  **Preparation**:
    - Ensure your `.env` file has your `OPENAI_API_KEY`.
2.  **Install dependencies**:
    ```bash
    pip install openai requests pydantic python-dotenv
    ```
3.  **Run the Agent**:
    ```bash
    python "agent_two(cot).py"
    ```
    *Input example: "What is the weather in Mumbai?"*

---

## 🎯 Summary
We've moved from static chat to **dynamic agents**. By combining **Structured Outputs (Pydantic)** with a **Reasoning Loop**, we've built a system that can understand intent, fetch real-world data, and answer complex questions.