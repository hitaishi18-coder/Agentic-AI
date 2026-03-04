# 03 Prompt Engineering

This directory explores various prompt engineering techniques using the OpenAI Python SDK. These scripts demonstrate how to guide Large Language Models (LLMs) to produce specific, structured, and logical outputs by carefully crafting the system and user prompts.

## Overview

The scripts in this folder cover a progression of prompt engineering strategies, from basic constraints to complex reasoning and persona adoption:
* **Zero-Shot & Few-Shot Prompting**: Teaching the model how to respond with and without examples.
* **Chain of Thought (CoT)**: Forcing the model to "think" step-by-step before outputting a final answer.
* **Persona Adoption**: Instructing the model to take on specific character traits, tones, and knowledge bases.

## Files & Techniques

* **`01_zero.py`**: Demonstrates **Zero-Shot Prompting**. The system prompt explicitly restricts the AI to only answer coding-related questions without providing any prior examples.
* **`02_few.py`**: Demonstrates **Few-Shot Prompting**. The system prompt provides a strict JSON output schema and includes multiple Q&A examples to teach the model exactly how to format its responses.
* **`03_cot.py`**: Demonstrates **Manual Chain of Thought**. Shows how a developer can hardcode the reasoning steps (`START`, `PLAN`, `OUTPUT`) into the message history to simulate step-by-step logic.
* **`04_cot_automated.py`**: Demonstrates **Automated Chain of Thought**. Implements an interactive chat loop where the model autonomously generates its own `PLAN` steps in JSON format before delivering the final `OUTPUT` to the user.
* **`05_persona.py`**: Demonstrates basic **Persona Prompting**. The AI is instructed to act as a 23-year-old tech enthusiast and engineer with specific skills in JS, Python, and GenAI.
* **`bubu_dudu_persona.py` & `auto_bubu_dudu.py`**: Demonstrates **Multi-Character Roleplay**. The AI takes on two distinct personas simultaneously (Bubu and Dudu), complete with emotional reactions, actions, and specific conversational formatting.

## Prerequisites

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
Ensure you have a .env file in your directory containing your OPENAI_API_KEY, as these scripts use dotenv to load environment variables.

Usage
You can run any of these scripts directly from the terminal to see the prompting techniques in action. For the interactive scripts (04_cot_automated.py and auto_bubu_dudu.py), type your messages into the prompt and type exit (or use Ctrl+C) to quit.

Bash
# Example: Run the automated Chain of Thought script
python 04_cot_automated.py