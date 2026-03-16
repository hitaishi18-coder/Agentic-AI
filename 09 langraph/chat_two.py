
# Load environment variables (.env file)
from dotenv import load_dotenv

# TypedDict allows us to define the structure of the graph state
from typing_extensions import TypedDict

# Optional means the value can be None
# Literal restricts return values to specific strings
from typing import Optional, Literal

# LangGraph components for building the graph
from langgraph.graph import StateGraph, START, END

# OpenAI client to call the LLM
from openai import OpenAI


# -----------------------------
# Load API Keys from .env
# -----------------------------

load_dotenv()

# Initialize OpenAI client
client = OpenAI()


# -----------------------------
# Define Graph State
# -----------------------------
# State is the shared memory that flows between nodes

class State(TypedDict):

    # User question
    user_query: str

    # LLM response (initially None)
    llm_output: Optional[str]

    # Optional evaluation flag
    is_good: Optional[bool]


# -----------------------------
# NODE 1 : First Chatbot
# -----------------------------
# This node calls a small/cheap model first

def chatbot(state: State):

    print("ChatBot Node", state)

    # Call OpenAI model
    response = client.chat.completions.create(
        model="gpt-4.1-mini",   # smaller cheaper model
        max_tokens=50,          # limit tokens to avoid credit errors
        messages=[
            {
                "role": "user",
                "content": state["user_query"]  # user input from state
            }
        ]
    )

    # Extract the generated text
    state["llm_output"] = response.choices[0].message.content

    # Return updated state
    return state


# -----------------------------
# NODE 2 : Evaluate Response
# -----------------------------
# This node decides which node to execute next

def evaluate_response(state: State) -> Literal["chatbot_gemini", "endnode"]:

    print("Evaluate Node", state)

    # Example evaluation logic
    # If correct answer contains "4", end the workflow
    if "4" in state["llm_output"]:
        return "endnode"

    # Otherwise send to stronger model
    return "chatbot_gemini"


# -----------------------------
# NODE 3 : Stronger Chatbot
# -----------------------------
# This node runs a more powerful model if needed

def chatbot_gemini(state: State):

    print("chatbot_gemini Node", state)

    response = client.chat.completions.create(
        model="gpt-4.1",   # stronger model
        max_tokens=50,
        messages=[
            {
                "role": "user",
                "content": state["user_query"]
            }
        ]
    )

    # Save improved response
    state["llm_output"] = response.choices[0].message.content

    return state


# -----------------------------
# NODE 4 : End Node
# -----------------------------
# Final node before finishing the graph

def endnode(state: State):

    print("End Node", state)

    # Simply return the final state
    return state


# -----------------------------
# Create Graph Builder
# -----------------------------
# StateGraph manages the workflow execution

graph_builder = StateGraph(State)


# -----------------------------
# Register Nodes
# -----------------------------

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)


# -----------------------------
# Define Graph Flow
# -----------------------------

# Graph starts at chatbot node
graph_builder.add_edge(START, "chatbot")

# After chatbot runs, use conditional routing
graph_builder.add_conditional_edges(
    "chatbot",
    evaluate_response
)

# If chatbot_gemini runs → go to endnode
graph_builder.add_edge("chatbot_gemini", "endnode")

# endnode → graph finishes
graph_builder.add_edge("endnode", END)


# -----------------------------
# Compile the Graph
# -----------------------------
# Converts graph structure into executable workflow

graph = graph_builder.compile()


# -----------------------------
# Execute the Graph
# -----------------------------
# Provide initial state input

updated_state = graph.invoke({
    "user_query": "Hey, What is 2 + 2?"
})


# -----------------------------
# Print Final Result
# -----------------------------

print("\nFinal State:\n", updated_state)