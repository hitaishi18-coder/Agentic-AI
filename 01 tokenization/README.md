# 01 - Tokenization: The Language of LLMs 🗨️

This module covers the fundamental process of **tokenization**, which is how Large Language Models (LLMs) turn text into things they can actually process: **numbers**.

---

## 📘 Theory: What is Tokenization?

Large Language Models (LLMs) like GPT-4 don't read text letter-by-letter like humans do. They process text in chunks called **tokens**.

### Key Concepts:
1.  **Tokens**: A token can be a word (e.g., "hello"), a part of a word (e.g., "ing"), or even a single character.
2.  **Encoding**: The process of converting text (strings) into a list of integers (tokens).
3.  **Decoding**: The reverse process—converting a list of integers back into human-readable text.
4.  **Vocab Size**: The total number of unique tokens the model knows. For `gpt-4o`, this is around 100k+ unique tokens.

### Why do we need it?
- **Efficiency**: Instead of processing every single character, LLMs process chunks, saving memory and compute.
- **Context Window**: LLMs have a limit on the number of tokens they can handle at once (tokens, not characters).

---

## 🛠️ Imports & Libraries

We use **tiktoken**, OpenAI's open-source library for tokenization.

```python
import tiktoken
```

---

## 💻 Code Explanation (Simplified)

### 1. Selecting the Model Encoding
Each LLM (GPT-3.5, GPT-4, GPT-4o) might use a different tokenization scheme. We specify the one we want.
```python
enc = tiktoken.encoding_for_model("gpt-4o")
```

### 2. Encoding Text
We take a human string and convert it into a list of integers.
```python
txt = "hey there! i am hitaishi "
tokens = enc.encode(txt)
```

### 3. Decoding Tokens
We take the list of integers and convert it back into a string to verify it worked.
```python
decoded = enc.decode(tokens)
```

---

## 📜 Full Code Listing: `main.py`

```python
import tiktoken

# 1. Choose the model encoding (GPT-4o)
enc = tiktoken.encoding_for_model("gpt-4o")

# 2. Text input
txt = "hey there! i am hitaishi "

# 3. Text to Tokens (Encoding)
tokens = enc.encode(txt)
print(f"Text: '{txt}'")
print(f"Encoded Tokens: {tokens}")

# Example tokens for "hey there! i am hitaishi "
# [48467, 1354, 0, 575, 939, 167343, 24597, 220]

# 4. Tokens to Text (Decoding)
decoded = enc.decode(tokens)
print(f"Decoded Text: '{decoded}'")
```

---

## 🚀 How to Run

1.  **Install dependencies**:
    ```bash
    pip install tiktoken
    ```
2.  **Run the script**:
    ```bash
    python main.py
    ```

### 🎯 Summary
In this module, we've seen how `tiktoken` bridges the gap between **human language** (strings) and **machine understanding** (arrays of integers). Understanding tokenization is key to managing cost and context limits in LLM-based applications.