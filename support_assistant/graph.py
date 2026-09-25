import os
import chromadb

from typing import TypedDict

from sentence_transformers import (
    SentenceTransformer
)

from langgraph.graph import (
    StateGraph
)

MOCK_LLM = os.getenv(
    "MOCK_LLM",
    "1"
)

class SupportState(TypedDict):

    query: str

    intent: str

    answer: str

    sources: list

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    "zepto_collection"
)

embedder = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

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
        kw in query
        for kw in keywords
    ):
        state["intent"] = \
            "policy_question"
    else:
        state["intent"] = \
            "general_question"

    return state

def retrieve_and_answer(state):

    query = state["query"]

    q_emb = embedder.encode(
        query
    ).tolist()

    results = collection.query(

        query_embeddings=[q_emb],

        n_results=3

    )

    docs = results["documents"][0]

    ids = results["ids"][0]

    top_doc = docs[0]

    answer = \
        f"Based on the retrieved context: {top_doc[:200]}"

    state["answer"] = answer

    state["sources"] = ids

    return state

def direct_answer(state):

    state["answer"] = \
        "I can only answer questions about Zepto policies right now."

    state["sources"] = []

    return state

def route(state):

    if state["intent"] == \
        "policy_question":

        return "retrieve"

    return "direct"

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

    route,

    {
        "retrieve":
        "retrieve",

        "direct":
        "direct"
    }
)

builder.set_finish_point(
    "retrieve"
)

builder.set_finish_point(
    "direct"
)

graph = builder.compile()

