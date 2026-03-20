# 00 - FastAPI: Building Modern APIs ⚡

This module introduces **FastAPI**, a high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints.

## 📘 Theory: What is FastAPI?

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python. It is built on top of **Starlette** (for the web parts) and **Pydantic** (for the data parts).

### Key Concepts:
1.  **REST API**: A Representational State Transfer API that uses HTTP requests to GET, PUT, POST, and DELETE data.
2.  **Pydantic (BaseModel)**: Used for data validation and settings management. It ensures that the data sent to or from the API follows a specific schema.
3.  **Decorators**: FastAPI uses Python decorators (like `@app.get("/")`) to bind URL paths to specific functions.
4.  **Uvicorn**: An ASGI (Asynchronous Server Gateway Interface) server implementation, used to run the FastAPI application.

---

## 🛠️ Imports & Libraries

In `main.py`, we use:
- `FastAPI`: The core class to create our web application.
- `BaseModel`: From `pydantic`, used to define our data structure (schema).
- `List`: From `typing`, to handle collections of data.

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
```

---

## 💻 Code Explanation (Simplified)

### 1. The Data Schema
We define what a "Tea" looks like using `Pydantic`. Every tea must have an `id` (integer), `name` (string), and `origin` (string).
```python
class Tea(BaseModel):
    id: int
    name: str 
    origin: str 
```

### 2. The Database (In-Memory)
We use a simple Python list to store our teas. Note that this resets every time the server restarts!
```python
teas : List[Tea] = []
```

### 3. API Endpoints
- **GET `/`**: Returns a simple welcome message.
- **GET `/teas`**: Returns the list of all teas.
- **POST `/teas`**: Adds a new tea to our list.
- **PUT `/teas/{tea_id}`**: Finds a tea by ID and updates its details.
- **DELETE `/teas/{tea_id}`**: Removes a tea from our list.

---

## 📜 Full Code Listing: `main.py`

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Tea(BaseModel):
    id: int
    name: str 
    origin: str 

teas : List[Tea] = []

@app.get("/")
def read_root():
    return {"message": "welcome to tea house!"}

@app.get("/teas")
def get_teas():
    return teas

@app.post("/teas")
def add_tea(tea: Tea):
    teas.append(tea)
    return tea

@app.put("/teas/{tea_id}")
def update_tea(tea_id: int, updated_tea: Tea):
    for index, tea in enumerate(teas):
        if tea.id == tea_id:
            teas[index] = updated_tea
            return updated_tea
    return {"error": "tea not found!"}

@app.delete("/teas/{tea_id}")
def delete_tea(tea_id: int):
    for index, tea in enumerate(teas):
        if tea.id == tea_id:
            deleted = teas.pop(index)
            return deleted
    return {"error": "tea not found"}
```

---

## 🚀 How to Run

1.  **Install dependencies**:
    ```bash
    pip install fastapi uvicorn
    ```
2.  **Run the server**:
    ```bash
    uvicorn main:app --reload
    ```
3.  **Access Documentation**:
    - Interactive Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    - Alternative Docs (Redoc): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🎯 Summary
This project demonstrates the basics of **CRUD** (Create, Read, Update, Delete) operations using FastAPI. It uses **Pydantic** for type safety and **decorators** for routing.
