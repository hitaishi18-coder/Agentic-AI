# 01 Tokenization

This folder contains a simple demonstration of how text tokenization works for Large Language Models (LLMs) using OpenAI's `tiktoken` library. 

## Overview
The project shows how a plain text string is converted into integer tokens that an LLM can understand, and how those tokens can be decoded back into human-readable text. It specifically uses the encoding for the `gpt-4o` model.

## Files
* **`main.py`**: The core script. It encodes the string `"hey there! i am hitaishi "` into tokens and then decodes them back to verify the process.
* **`requirements.txt`**: A list of Python dependencies required for the project, most notably `tiktoken==0.12.0`.

## Setup & Installation

1. **(Optional but recommended)** Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install the dependencies:

Bash
pip install -r requirements.txt
Usage
Run the script from your terminal:

Bash
python main.py
Expected Output
When you run the script, it will display the tokenized array of integers and the reconstructed string:

tokens:- [48467, 1354, 0, 575, 939, 167343, 24597, 220]
decoded:- hey there! i am hitaishi