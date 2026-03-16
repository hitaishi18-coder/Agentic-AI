
from typing_extensions import TypedDict
from typing import Annotated

from dotenv import load_dotenv

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage


# -----------------------------
# Load Environment Variables
# -----------------------------

load_dotenv()


# -----------------------------
# Initialize LLM
# -----------------------------

llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai",
    max_tokens=50
)


# -----------------------------
# Define STATE
# -----------------------------

class State(TypedDict):

    # messages will store conversation history
    messages: Annotated[list, add_messages]


# -----------------------------
# Chatbot Node (LLM Node)
# -----------------------------

def chatbot(state: State):

    # Get messages from state
    messages = state["messages"]

    # Call LLM
    response = llm.invoke(messages)

    # Return LLM response
    return {
        "messages": [response]
    }


# -----------------------------
# Sample Node
# -----------------------------

def samplenode(state: State):

    print("\nInside sample node state:", state)

    return {
        "messages": ["This message was added by sample node"]
    }


# -----------------------------
# Build Graph
# -----------------------------

graph_builder = StateGraph(State)


# Add nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)


# Define flow
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)


# Compile graph
graph = graph_builder.compile()


# -----------------------------
# Run Graph
# -----------------------------

updated_state = graph.invoke({
    "messages": [HumanMessage(content="Hi, my name is Hitaishi")]
})


# -----------------------------
# Print Final State
# -----------------------------

print("\n\nUpdated State:\n", updated_state)