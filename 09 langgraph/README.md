# 09 - LangGraph: Building Stateful Agents 🕸️

This module introduces **LangGraph**, a library for building stateful, multi-actor applications with LLMs. It is built on top of LangChain and adds the ability to create **circular flows** (cycles) and maintain **complex state**.

---

## 📘 Theory: Why use LangGraph?

While standard LangChain chains are "Directed Acyclic Graphs" (DAGs) — meaning they flow in one direction — real-world agents often need to **loop** (e.g., try a tool, see if it worked, try again).

### Key Concepts:
1.  **State**: A central shared object (usually a dictionary) that all nodes can read and write to.
2.  **Nodes**: Python functions that represent a step in your logic. They take the current `State` as input and return an update to it.
3.  **Edges**: Define the "path" from one node to another.
    -   **Normal Edges**: A direct link between nodes.
    -   **Conditional Edges**: Decision points (e.g., "If the LLM wants to call a tool, go to the tool node; otherwise, go to END").
4.  **Reducers**: Functions that define *how* to update the state. For example, `add_messages` tells LangGraph to **append** new messages to the existing list instead of overwriting them.
5.  **Checkpointers**: Persistence layers (like MongoDB) that allow the agent to "remember" conversations across different sessions using a `thread_id`.

---

## 🛠️ Imports & Libraries

- `langgraph`: Core library for graphs (`StateGraph`, `START`, `END`).
- `langchain_groq` / `langchain_openai`: LLM providers.
- `typing_extensions`: To define the `State` using `TypedDict`.
- `MongoDBSaver`: For persistent memory (Checkpoints).

```python
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated
```

---

## 💻 Code Explanation (Simplified)

### 1. Defining the State
We define a `TypedDict` where `messages` is a list of messages. The `Annotated` part with `add_messages` is a **reducer**. It ensures that whenever a node returns `{"messages": ["hi"]}`, LangGraph **adds** it to the list instead of replacing the whole list.
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
```

### 2. Creating a Node
A node is just a function. It gets the current state, does something (like calling an LLM), and returns the *diff* to apply to the state.
```python
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

### 3. Building the Graph
We connect the pieces using `add_node` and `add_edge`.
```python
builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile()
```

### 4. Persistence with MongoDB (`chat_checkpoints.py`)
To make the agent "smart" across restarts, we use a checkpointer. A `thread_id` acts like a session ID.
```python
with MongoDBSaver.from_conn_string("mongodb://localhost:27017") as checkpointer:
    app = builder.compile(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "user_123"}}
    app.invoke({"messages": [HumanMessage(content="Hi!")]}, config)
```

---

## 📜 Full Code Listing: `chat.py` (Basic Graph)

```python
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated

class State(TypedDict):
    messages: Annotated[list, add_messages]

def node_one(state: State):
    return {"messages": ["Message from Node 1"]}

def node_two(state: State):
    return {"messages": ["Message from Node 2"]}

builder = StateGraph(State)
builder.add_node("n1", node_one)
builder.add_node("n2", node_two)

builder.add_edge(START, "n1")
builder.add_edge("n1", "n2")
builder.add_edge("n2", END)

graph = builder.compile()
print(graph.invoke({"messages": ["Initial Message"]}))
```

---

## 🚀 How to Run

1.  **Start MongoDB** (For persistence examples):
    ```bash
    docker compose up -d
    ```
    *(Uses the `docker-compose.yml` file in the directory)*
2.  **Install dependencies**:
    ```bash
    pip install langgraph langchain-openai langchain-groq langgraph-checkpoint-mongodb python-dotenv
    ```
3.  **Run the script**:
    ```bash
    python chat_checkpoints.py
    ```

---

## 🎯 Summary
LangGraph turns LLMs into **reliable agents** by giving them a structured "brain" (State) and a "nervous system" (Edges). With **Checkpointers**, these agents gain long-term memory, making them suitable for production-grade chatbots and automation tools.
