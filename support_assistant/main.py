import os
from typing import TypedDict, List

import chromadb
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from langgraph.graph import StateGraph

# ------------------------------------
# Pydantic Models
# ------------------------------------

class AskRequest(BaseModel):
    query: str

class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

# ------------------------------------
# Mock LLM
# ------------------------------------

MOCK_LLM = os.getenv("MOCK_LLM", "1")

# ------------------------------------
# Chroma DB Setup
# ------------------------------------

embedder = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    "zepto_collection"
)

# ------------------------------------
# Load Documents
# ------------------------------------

if collection.count() == 0:

    for file_name in os.listdir("docs"):

        if file_name.endswith(".txt"):

            path = os.path.join(
                "docs",
                file_name
            )

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                text = f.read()

            embedding = embedder.encode(
                text
            ).tolist()

            collection.add(

                ids=[file_name],

                documents=[text],

                embeddings=[embedding]

            )

print("Documents Loaded")

# ------------------------------------
# LangGraph State
# ------------------------------------

class SupportState(TypedDict):

    query: str

    intent: str

    answer: str

    sources: list

# ------------------------------------
# Node 1
# classify_intent
# ------------------------------------

def classify_intent(state):

    query = state["query"].lower()

    keywords = [

        "delivery",

        "return",

        "refund",

        "membership",

        "tracking",

        "cancel",

        "gift card",

        "support hours"

    ]

    if any(
        word in query
        for word in keywords
    ):

        state["intent"] = "policy_question"

    else:

        state["intent"] = "general_question"

    return state

# ------------------------------------
# Node 2
# retrieve_and_answer
# ------------------------------------

def retrieve_and_answer(state):

    query = state["query"]

    q_embedding = embedder.encode(
        query
    ).tolist()

    results = collection.query(

        query_embeddings=[q_embedding],

        n_results=3

    )

    docs = results["documents"][0]

    ids = results["ids"][0]

    top_doc = docs[0]

    state["answer"] = (

        "Based on the retrieved context: "

        + top_doc[:200]

    )

    state["sources"] = ids

    return state

# ------------------------------------
# Node 3
# direct_answer
# ------------------------------------

def direct_answer(state):

    state["answer"] = (

        "I can only answer questions about Zepto policies right now."

    )

    state["sources"] = []

    return state

# ------------------------------------
# Router
# ------------------------------------

def route_question(state):

    if state["intent"] == "policy_question":

        return "retrieve"

    return "direct"

# ------------------------------------
# Graph Creation
# ------------------------------------

builder = StateGraph(
    SupportState
)

builder.add_node(
    "classify",
    classify_intent
)

builder.add_node(
    "retrieve",
    retrieve_and_answer
)

builder.add_node(
    "direct",
    direct_answer
)

builder.set_entry_point(
    "classify"
)

builder.add_conditional_edges(

    "classify",

    route_question,

    {

        "retrieve": "retrieve",

        "direct": "direct"

    }

)

builder.set_finish_point(
    "retrieve"
)

builder.set_finish_point(
    "direct"
)

graph = builder.compile()

# ------------------------------------
# FastAPI
# ------------------------------------

app = FastAPI()

@app.post(
    "/ask",
    response_model=AskResponse
)
def ask(request: AskRequest):

    result = graph.invoke(

        {
            "query": request.query
        }

    )

    return AskResponse(

        answer=result["answer"],

        sources=result["sources"],

        confidence=1.0

    )