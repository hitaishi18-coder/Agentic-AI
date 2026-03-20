# 02 - LLM Basics: Connecting to the Brain 🧠

This module explores the different SDKs (Software Development Kits) to interact with leading Large Language Models (LLMs) like GPT-4 (OpenAI) and Gemini (Google).

---

## 📘 Theory: How SDKs Work

An LLM is just a powerful model running on remote servers. To use it in our Python code, we use **SDKs** provided by the companies (OpenAI, Google) which handle the HTTP requests, API keys, and responses for us.

### Key Concepts:
1.  **API Keys**: A secret token used to authenticate your requests. Never share these publicly!
2.  **Base URL**: The web address where the API is hosted. OpenAI defaults to its own servers, but you can change this to use other APIs that "look" like OpenAI.
3.  **Roles**:
    - `system`: Tells the model WHO it is and HOW to behave.
    - `user`: What the actual human input is.
    - `assistant`: The response from the AI.
4.  **Temperature**: A setting (usually 0 to 1) that controls "creativity". Low temperature = deterministic/focused, High = random/creative.

---

## 🛠️ Imports & Libraries

We use two main libraries:
- `openai`: To interact with GPT models (and Gemini via an OpenAI-compatible endpoint).
- `google-genai`: The official Google SDK for Gemini.
- `python-dotenv`: To safely load our secret API keys from a `.env` file.

```python
from openai import OpenAI
from google import genai
from dotenv import load_dotenv
```

---

## 💻 Code Explanation (Simplified)

### 1. Using OpenAI SDK (`main.py`)
We create a `client` and pass our messages. The `Messages` list is a conversation history.
```python
client = OpenAI() # Uses OPENAI_API_KEY from .env
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role":"system", "content":"you are an expert in Maths"},
        {"role":"user", "content":"solve a + b whole square"}
    ]
)
```

### 2. Using Google GenAI SDK (`gemini_hello.py`)
Google uses a slightly different format for their dedicated SDK.
```python
client = genai.Client(api_key="YOUR_API_KEY")
response = client.models.generate_content(
    model="gemini-1.5-flash", content="explain how ai works"
)
```

### 3. Gemini models via OpenAI SDK (`gemini_openai.py`)
Google's Gemini API is compatible with the OpenAI format if you change the `base_url`. This is powerful for switching models easily!
```python
client = OpenAI(
    api_key="YOUR_GEMINI_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
```

---

## 📜 Full Code Examples

### `main.py` (OpenAI)
```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI() 

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 2+2?"}
    ]
)
print(response.choices[0].message.content)
```

### `gemini_hello.py` (Google SDK)
```python
from google import genai

client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model="gemini-1.5-flash", 
    content="What is Gemini?"
)
print(response.text)
```

---

## 🚀 How to Run

1.  **Preparation**:
    - Create a `.env` file with your keys (see `.env.example`).
    - `OPENAI_API_KEY=your_key_here`
2.  **Install dependencies**:
    ```bash
    pip install openai google-genai python-dotenv
    ```
3.  **Run scripts**:
    ```bash
    python main.py
    python gemini_hello.py
    ```

---

## 🎯 Summary
In this module, we learned that we can interact with LLMs using **official SDKs** or use **OpenAI-compatible endpoints** to switch between different models like GPT and Gemini seamlessly. Always keep your API keys safe in a `.env` file!