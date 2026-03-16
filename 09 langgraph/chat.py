from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END


# -----------------------------
# Define the STATE of the graph
# -----------------------------
# State is a dictionary-like structure that flows through all nodes

class State(TypedDict):
    
    # messages is a list
    # add_messages automatically APPENDS new messages returned by nodes
    messages: Annotated[list, add_messages]


# -----------------------------
# Create NODE 1
# -----------------------------
# Every node is just a Python function

def chatbot(state: State):

    # Print current state when node runs
    print("\n\n inside chatbot state", state)

    # Return new messages
    # Because we used add_messages, this message will be appended
    return {
        "messages": ["hii, this is a message from chatbot node !"]
    }


# -----------------------------
# Create NODE 2
# -----------------------------

def samplenode(state: State):

    # Print the state received by this node
    print("\n\n inside sample node state", state)

    # Return another message
    return {
        "messages": ["hii, sample message appended !"]
    }


# -----------------------------
# Create the GRAPH BUILDER
# -----------------------------
# StateGraph tells LangGraph what the structure of the state is

graph_builder = StateGraph(State)


# -----------------------------
# Register Nodes
# -----------------------------
# Add nodes to the graph

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)


# -----------------------------
# Define Graph Flow (Edges)
# -----------------------------

# START → chatbot
graph_builder.add_edge(START, "chatbot")

# chatbot → samplenode
graph_builder.add_edge("chatbot", "samplenode")

# samplenode → END
graph_builder.add_edge("samplenode", END)


# -----------------------------
# Compile the graph
# -----------------------------
# This prepares the graph for execution

graph = graph_builder.compile()


# -----------------------------
# Run the graph
# -----------------------------
# Initial state passed to graph

updated_state = graph.invoke({
    "messages": ["hii, my name is hitaishi"]
})


# -----------------------------
# Print final state
# -----------------------------
print("\n\n updated state ", updated_state)



# -----------------------------------------
# GRAPH FLOW EXPLANATION
# -----------------------------------------

# (START) → chatbot → samplenode → (END)

# Initial state:
# state = { messages: ["Hey there"] }

# Step 1:
# chatbot runs
# state becomes:
# { messages: ["Hey there",
#              "Hi, This is a message from ChatBot Node"] }

# Step 2:
# samplenode runs
# state becomes:
# { messages: ["Hey there",
#              "Hi, This is a message from ChatBot Node",
#              "Hi, sample message appended"] }

# Final output:
# updated_state = final state after all nodes execute