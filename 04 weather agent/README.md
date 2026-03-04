# 04 Weather Agent (Tool Calling & Agents)

This directory demonstrates how to bridge the gap between a standard conversational LLM and an "Agent" capable of interacting with the outside world. Specifically, it shows how to build an AI assistant that can fetch real-time weather data using external APIs.

## Overview

The scripts in this folder illustrate a clear progression from a basic chat script to a fully autonomous, reasoning agent:
* **Baseline LLM**: A simple chat completion loop.
* **Heuristic Tool Calling**: Hardcoded logic that triggers an API call based on keywords.
* **Agentic Tool Calling (Chain of Thought)**: An advanced setup where the LLM autonomously decides *when* to use a tool, *how* to use it, and *what* to do with the result.

## Files & Architectures

* **`main.py`**: The baseline script. It takes user input and passes it directly to `gpt-4o` without any external tools. It cannot answer real-time weather questions accurately.
* **`agent_one.py`**: Demonstrates **Hardcoded Routing**. It intercepts the user's input and checks if the word "weather" is present. If it is, it parses the city name and directly calls the Open-Meteo API using a custom `get_weather` function. If not, it falls back to a standard OpenAI chat completion.
* **`agent_two(cot).py`**: Demonstrates a **ReAct / Chain of Thought Agent**. The system prompt instructs the LLM to output its thought process in JSON format using steps (`START`, `PLAN`, `TOOL`, `OBSERVE`, `OUTPUT`). The script parses this JSON, dynamically executes the `get_weather` tool when requested by the LLM, and feeds the observation back into the context window so the LLM can formulate a final answer.

## How the Weather Tool Works
Both agents utilize the free **Open-Meteo API**. The `get_weather(city)` function works in two steps:
1. Calls the Geocoding API to convert the city name into latitude and longitude coordinates.
2. Calls the Weather Forecast API using those coordinates to fetch the current temperature and wind speed.

## Prerequisites

1. Install the required dependencies:
   ```bash
   pip install requests openai python-dotenv pydantic
Ensure your .env file contains your OPENAI_API_KEY.

Usage
Run any of the agents from your terminal:

Bash
# Run the basic heuristic agent
python agent_one.py

# Run the advanced Chain of Thought agent
python "agent_two(cot).py"