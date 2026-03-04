# 02 Hello World (LLM Basics)

This directory contains introductory scripts demonstrating how to establish connections and make basic requests to Large Language Models (LLMs) using both the OpenAI and Google GenAI Python SDKs.

## Overview

The scripts in this folder act as a "Hello World" for generative AI APIs. They cover:
* Making a standard chat completion request using OpenAI's API.
* Using the official Google GenAI SDK to call Gemini models.
* Leveraging OpenAI's Python SDK to call Gemini models via Google's OpenAI-compatible endpoint.

## Files

* **`main.py`**: Demonstrates a basic chat completion call using the `openai` library with system and user messages.
* **`gemini_hello.py`**: Uses the `google.genai` client to prompt the `gemini-3-flash-preview` model.
* **`gemini_openai.py`**: Shows how to use the OpenAI SDK with a custom `base_url` (`https://generativelanguage.googleapis.com/v1beta/openai/`) to interact with Gemini models using OpenAI's familiar message formatting.

## Prerequisites

Before running these scripts, you must have your environment variables set up. Ensure you have a `.env` file in your root or working directory containing your API keys, as the scripts use `dotenv` to load them.

*(Note: The `gemini_hello.py` and `gemini_openai.py` currently have hardcoded API keys. It is highly recommended to move these into your `.env` file for security.)*

## Usage

Run any of the scripts individually from your terminal:

```bash
# Run the basic OpenAI example
python main.py

# Run the Google GenAI SDK example
python gemini_hello.py

# Run the OpenAI-compatible Gemini example
python gemini_openai.py