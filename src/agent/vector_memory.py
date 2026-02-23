import json
import os
import numpy as np

from openai import OpenAI


client = OpenAI()

MEMORY_FILE = "memory/vector_memory.json"

def get_embedding(text):

    # SAFETY FIX
    if not text or not isinstance(text, str):
        text = "unknown error"

    text = text.strip()

    if text == "":
        text = "unknown error"

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def save_vector_memory(requirement, error, analysis):

    embedding = get_embedding(error)

    entry = {
        "requirement": requirement,
        "error": error,
        "analysis": analysis,
        "embedding": embedding
    }

    if not os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "w") as f:
            json.dump([], f)

    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    data.append(entry)

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("[Agent] Vector memory saved.")


def search_similar_errors(error, threshold=0.8):
    if not error:
        return []

    query_embedding = get_embedding(error)

    if not os.path.exists(MEMORY_FILE):
        return []

    query_embedding = get_embedding(error)

    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    results = []

    for entry in data:

        sim = cosine_similarity(query_embedding, entry["embedding"])

        if sim >= threshold:
            results.append({
                "similarity": sim,
                "error": entry["error"],
                "analysis": entry["analysis"]
            })

    return sorted(results, key=lambda x: x["similarity"], reverse=True)