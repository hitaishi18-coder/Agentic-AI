# 03 - Prompting: Talking to the Machine 💬

Prompting is the art and science of giving instructions to an LLM to get the desired result. This module covers essential prompting techniques.

---

## 📘 Theory: Types of Prompts

Prompting isn't just "asking a question". There are several techniques used to improve LLM performance:

### 1. **Zero-Shot Prompting**
Ask a question without any examples.
*Example: "What is the capital of France?"*

### 2. **Few-Shot Prompting**
Provide a few examples (1-5) to guide the model on how to format the answer or solve the problem.
*Example: "Apple -> Fruit, Carrot -> Vegetable, Banana -> ?"*

### 3. **Chain of Thought (CoT)**
Tell the model to "explain its reasoning" or "think step-by-step". This is crucial for math and logic!
*Example: "Let's think step by step. First, we add... then we..."*

### 4. **Persona Prompting**
Give the model a specific role (e.g., "You are an expert mathematician", "You are a coding mentor"). This affects the tone and technicality of the response.

---

## 🛠️ Imports & Libraries

We continue to use `openai` and `python-dotenv` for local storage of credentials.

```python
from openai import OpenAI
from dotenv import load_dotenv
```

---

## 💻 Code Explanation (Simplified)

### 1. Zero-Shot (`01_zero.py`)
Straightforward request—no guidance provided.
```python
messages=[
    {"role": "user", "content": "Tell me a joke about AI."}
]
```

### 2. Few-Shot (`02_few.py`)
We give a few examples of input/output to "train" the model in-context.
```python
messages=[
    {"role": "user", "content": "Happy: 😀"},
    {"role": "user", "content": "Sad: 😢"},
    {"role": "user", "content": "Excited: ?"}
]
```

### 3. Chain of Thought (`03_cot.py`)
We explicitly ask the model to reason first.
```python
messages=[
    {"role": "user", "content": "Solve this: 2+2*2. Show your reasoning."}
]
```

### 4. Persona Prompting (`05_persona.py`)
Using the `system` message to define its role.
```python
messages=[
    {"role": "system", "content": "You are a professional pirate. Reply only in pirate slang."},
    {"role": "user", "content": "Where is the treasure?"}
]
```

### 5. Advanced Character Roleplay (`bubu_dudu_persona.py`)
This script uses a complex prompt to create a dual-character experience. It tells the AI to roleplay as two characters, **Bubu** and **Dudu**, following specific tone, style rules, and formatting (e.g., using emojis and action tags like `*hugs*`).

---

## 📜 Full Code Listing: `03_cot.py` (Snippet)

```python
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that thinks step-by-step."},
        {"role": "user", "content": "If I have 3 apples and I buy 2 more, but give 1 to a friend, how many do I have? Explain each step."}
    ]
)
print(response.choices[0].message.content)
```

---

## 🚀 How to Run

1.  **Preparation**:
    - Ensure your `.env` file has your `OPENAI_API_KEY`.
2.  **Install dependencies**:
    ```bash
    pip install openai python-dotenv
    ```
3.  **Run any example script**:
    ```bash
    python 01_zero.py
    python 03_cot.py
    ```

---

## 🎯 Summary
In this module, we've explored how different prompting techniques can significantly change the output quality. **Chain of Thought** is especially powerful for complex tasks, while **Few-Shot** is perfect for specific formatting needs.