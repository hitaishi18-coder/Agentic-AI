# checkpoints are used to store the state


# Import environment variables from .env file
from dotenv import load_dotenv

# TypedDict helps define the structure of the graph state
from typing_extensions import TypedDict

# Annotated allows us to attach metadata (like message reducers)
from typing import Annotated

# add_messages is a reducer that automatically appends new messages
from langgraph.graph.message import add_messages

# Core LangGraph components
from langgraph.graph import StateGraph, START, END

# MongoDB checkpointer to store conversation memory
from langgraph.checkpoint.mongodb import MongoDBSaver

# LangChain message format (REQUIRED for chat models)
from langchain_core.messages import HumanMessage

# Groq FREE LLM
from langchain_groq import ChatGroq


# Load environment variables
load_dotenv()


# Initialize the LLM
# Using GROQ free model instead of OpenAI
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)


# Define the structure of the graph state
class State(TypedDict):

    # messages list will store conversation history
    # add_messages automatically appends new messages
    messages: Annotated[list, add_messages]


# Chatbot Node
def chatbot(state: State):

    # Send the conversation history to the LLM
    response = llm.invoke(state.get("messages"))

    # Return the new AI response
    # LangGraph automatically merges it with previous messages
    return { "messages": [response] }


# Create a graph builder with State schema
graph_builder = StateGraph(State)


# Add chatbot node to graph
graph_builder.add_node("chatbot", chatbot)


# Define graph flow
# START -> chatbot
graph_builder.add_edge(START, "chatbot")

# chatbot -> END
graph_builder.add_edge("chatbot", END)


# Compile graph normally (without memory)
graph = graph_builder.compile()


# Function to compile graph WITH MongoDB checkpointer
def compile_graph_with_checkpointer(checkpointer):

    # This enables conversation memory
    return graph_builder.compile(checkpointer=checkpointer)


# MongoDB connection string
DB_URI = "mongodb://localhost:27017"


# Initialize MongoDB checkpointer
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:

    # Compile graph with memory support
    graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer=checkpointer)

    # Configuration for memory thread
    # thread_id acts like user_id
    config = {
        "configurable": {
            "thread_id": "hitaishi"  # conversation memory key
        }
    }


    # Start graph execution
    for chunk in graph_with_checkpointer.stream(

        # Initial state
        # We pass the first user message
        State({
            "messages": [HumanMessage(content="what is my name? you know that i m learning langgraph")]
        }),

        # Config with thread_id
        config,

        # Stream values after each node
        stream_mode="values"

        ):

            # Print the last message (AI response)
            chunk["messages"][-1].pretty_print()



# Graph Flow
# (START) -> chatbot -> (END)



# Example State
# state = { messages: ["Hey there"] }

# chatbot node receives:
# chatbot(state)

# chatbot sends messages to LLM

# LLM response returned

# state becomes:
# { messages: ["Hey there", "Hello! How can I help you?"] }



# MongoDB Checkpointer Memory Example

# thread_id = "hitaishi"

# Stored conversation:
# Human: what is my name?
# AI: I don't know your name yet.

# Next question:
# Human: My name is Hitaishi

# Future question:
# Human: what is my name?

# AI will remember using MongoDB memory.