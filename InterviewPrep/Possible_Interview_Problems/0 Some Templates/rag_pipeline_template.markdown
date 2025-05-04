# RAG Pipeline with Memory and Guardrails Template

This template provides a reusable structure for implementing a Retrieval-Augmented Generation (RAG) pipeline with memory and guardrails in a Python-based AI system. It is designed for a FastAPI backend but can be adapted to other frameworks.

---

## Overview

The RAG pipeline retrieves relevant documents, generates embeddings, queries a vector database, augments the results with a language model, retains conversation memory for context, and applies guardrails to ensure safe and accurate responses. It meets the following requirements:

- **Semantic Search**: Retrieves documents based on query embeddings.
- **Context Retention**: Uses memory to maintain conversation context.
- **Safety and Accuracy**: Applies guardrails to prevent hallucinations and ensure appropriate responses.

---

## Template Code

### Prerequisites
- Python 3.9+
- Dependencies: `fastapi`, `langchain`, `google-cloud-aiplatform`, `sentence-transformers`, `firebase-admin`, `pinecone-client`
- GCP services: Vertex AI (for Foundational Model), Firestore (for memory), Pinecone (vector DB)

### Code Structure

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import VertexAI
from langchain.prompts import PromptTemplate
from typing import List, Dict, Optional
import pinecone
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize FastAPI app
app = FastAPI()

# Initialize Firebase for memory storage
cred = credentials.Certificate("path/to/firebase-service-account.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Pinecone for vector storage
pinecone.init(api_key="your-pinecone-api-key", environment="your-pinecone-env")
index = pinecone.Index("knowledge-assistant-index")

# Initialize embeddings and LLM
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = Pinecone(index=index, embedding_function=embeddings.embed_query, text_key="text")
llm = VertexAI(model_name="text-bison", temperature=0.7)

# Pydantic model for request
class SearchRequest(BaseModel):
    query: str
    user_id: str
    session_id: str

# Memory management
def get_conversation_history(user_id: str, session_id: str) -> List[Dict[str, str]]:
    doc_ref = db.collection("conversations").document(user_id).collection("sessions").document(session_id)
    doc = doc_ref.get()
    return doc.to_dict().get("history", []) if doc.exists else []

def save_conversation_history(user_id: str, session_id: str, history: List[Dict[str, str]]):
    doc_ref = db.collection("conversations").document(user_id).collection("sessions").document(session_id)
    doc_ref.set({"history": history})

# Guardrails
def apply_guardrails(response: str) -> tuple[bool, str]:
    # Basic guardrails: Check for inappropriate content, length, and coherence
    inappropriate_keywords = ["offensive", "inappropriate", "harmful"]
    if any(keyword in response.lower() for keyword in inappropriate_keywords):
        return False, "Response contains inappropriate content."
    if len(response) > 2000:
        return False, "Response is too long."
    if len(response.split()) < 5:
        return False, "Response is too short or incoherent."
    return True, response

# RAG Pipeline endpoint
@app.post("/search")
async def search(request: SearchRequest):
    # Step 1: Retrieve conversation history (memory)
    history = get_conversation_history(request.user_id, request.session_id)
    context = "\n".join([f"User: {item['query']}\nAssistant: {item['response']}" for item in history[-3:]])

    # Step 2: Generate query embedding and retrieve documents
    query_embedding = embeddings.embed_query(request.query)
    docs = vector_store.similarity_search_by_vector(query_embedding, k=5)

    # Step 3: Prepare prompt with memory and retrieved documents
    prompt_template = PromptTemplate(
        input_variables=["context", "docs", "query"],
        template="Conversation History:\n{context}\n\nRetrieved Documents:\n{docs}\n\nQuery: {query}\nAnswer:"
    )
    docs_text = "\n".join([doc.page_content for doc in docs])
    prompt = prompt_template.format(context=context, docs=docs_text, query=request.query)

    # Step 4: Generate response using Foundational Model
    response = llm(prompt)

    # Step 5: Apply guardrails
    is_valid, response_or_error = apply_guardrails(response)
    if not is_valid:
        raise HTTPException(status_code=400, detail=response_or_error)

    # Step 6: Update conversation history
    history.append({"query": request.query, "response": response})
    save_conversation_history(request.user_id, request.session_id, history)

    return {"answer": response, "documents": [doc.page_content for doc in docs]}
```

---

## How It Works

1. **Memory (Conversation History)**:
   - Uses Firestore to store and retrieve conversation history for each user and session.
   - Limits history to the last 3 exchanges to maintain context without overwhelming the prompt.
2. **Retrieval (RAG)**:
   - Uses `HuggingFaceEmbeddings` to generate embeddings for the query.
   - Queries Pinecone (vector DB) to retrieve the top 5 relevant documents.
3. **Augmentation (Generation)**:
   - Combines conversation history, retrieved documents, and the query into a prompt using `PromptTemplate`.
   - Sends the prompt to Vertex AI’s Foundational Model (`text-bison`) to generate a response.
4. **Guardrails**:
   - Applies basic checks for inappropriate content, response length, and coherence.
   - Returns an error if the response fails guardrail checks.
5. **Response**:
   - Saves the updated conversation history to Firestore.
   - Returns the generated answer and document snippets to the client.

---

## Customization Points

- **Embedding Model**: Replace `sentence-transformers/all-MiniLM-L6-v2` with a more powerful model (e.g., `text-embedding-gecko` on Vertex AI).
- **Vector DB**: Swap Pinecone for Firestore or another vector store like FAISS.
- **Guardrails**: Add more sophisticated checks (e.g., toxicity detection using `detoxify`).
- **Memory**: Adjust the history window (e.g., last 5 exchanges) or add summarization for longer contexts.

---

## Why This Template?

- **Modularity**: Separates memory, retrieval, generation, and guardrails for easy modification.
- **Scalability**: Uses managed services (Vertex AI, Pinecone, Firestore) for scalability.
- **Safety**: Guardrails ensure responses are appropriate and coherent.
- **Context Awareness**: Memory retention makes the system conversational and context-aware.

This template is ideal for demonstrating your understanding of RAG pipelines, memory management, and safety in AI systems during an interview.