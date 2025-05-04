
# Conversational AI Implementation Plan

This document provides a streamlined implementation plan for a conversational AI system on Google Cloud Platform (GCP), using Python (FastAPI) for the backend and Angular for the frontend. The system meets requirements: Prompt Engineering, Retrieval-Augmented Generation (RAG), Guardrails for Tone and Hallucination, PII Redaction, Retrieval (FAQs, order history), and Escalation Routing.

## Overview

The architecture is a modular, cloud-native application leveraging GCP for scalability, Python for backend logic, and Angular for user interaction. Each component is designed for security, accuracy, and usability, aligning with requirements and developer familiarity (Python, Angular).

## Components and Implementation

### 1. User Interface
- **Purpose**: Web interface for query submission and response display.
- **Tools**:
  - Angular 11: Reactive frontend.
  - PrimeNG: UI components (tables, dialogs).
  - TypeScript: Type-safe development.
  - Tailwind CSS: Responsive styling.
- **GCP Services**:
  - Cloud Run: Hosts containerized Angular app.
  - Cloud CDN: Caches static assets.
- **Implementation**:
  - Create Angular project: `npx create-nx-workspace@11 conversational-ai`.
  - Build query input (`<p-inputText>`) and response display (`<p-table>`).
  - Use `HttpClient` for API Gateway communication.
  - Deploy: `gcloud run deploy ui-service --image gcr.io/[PROJECT_ID]/ui --region us-central1`.
- **Why It Works**:
  - Angular ensures robust input handling.
  - PrimeNG accelerates UI development.
  - Cloud Run and CDN provide scalability and low latency.

### 2. API Gateway
- **Purpose**: Routes requests, authenticates users, balances load.
- **Tools**:
  - FastAPI: High-performance API.
  - OAuth2: User authentication.
  - Pydantic: Request validation.
- **GCP Services**:
  - Cloud Endpoints: API routing.
  - Identity-Aware Proxy (IAP): OAuth2 security.
  - Cloud Load Balancing: Traffic distribution.
- **Implementation**:
  - Develop FastAPI endpoint: `/query`.
  - Validate requests with Pydantic models.
  - Configure Cloud Endpoints with OpenAPI spec.
  - Enable IAP for authentication.
  - Deploy: `gcloud run deploy api-gateway --image gcr.io/[PROJECT_ID]/api --region us-central1`.
- **Why It Works**:
  - FastAPI handles high request volumes.
  - Cloud Endpoints and IAP ensure secure access.
  - Load Balancing scales with traffic.

### 3. Prompt Engineering Service
- **Purpose**: Optimizes queries into LLM prompts.
- **Tools**:
  - FastAPI: Service endpoint.
  - LangChain: Prompt templating.
- **Foundation Model**:
  - Gemini 1.5 Flash (Vertex AI): Intent analysis.
- **GCP Services**:
  - Vertex AI: Hosts Gemini.
  - Cloud Run: Deploys service.
- **Implementation**:
  - Create endpoint: `/optimize-prompt`.
  - Use LangChain `PromptTemplate` for prompt structure.
  - Call Gemini for intent detection.
  - Deploy: `gcloud run deploy prompt-service --image gcr.io/[PROJECT_ID]/prompt --region us-central1`.
- **Why It Works**:
  - Gemini provides fast intent analysis.
  - LangChain simplifies prompt crafting.
  - Cloud Run scales dynamically.

### 4. RAG Module
- **Purpose**: Retrieves unstructured context (e.g., FAQs) via vector search.
- **Tools**:
  - FastAPI: Retrieval endpoint.
  - LangChain: Embedding and search.
  - Sentence Transformers: Embeddings (`all-MiniLM-L6-v2`).
- **Foundation Model**:
  - Text Embedding Gecko (Vertex AI): Query/document embeddings.
- **GCP Services**:
  - Vertex AI: Hosts Gecko.
  - Cloud Firestore: Stores vector embeddings.
  - Cloud Run: Deploys service.
- **Implementation**:
  - Create endpoint: `/retrieve-context`.
  - Generate embeddings with Gecko.
  - Store FAQ embeddings in Firestore.
  - Perform cosine similarity search.
  - Inject context with LangChain.
  - Deploy: `gcloud run deploy rag-service --image gcr.io/[PROJECT_ID]/rag --region us-central1`.
- **Why It Works**:
  - Gecko ensures accurate semantic retrieval.
  - Firestore enables fast vector search.
  - LangChain grounds responses, reducing hallucinations.

### 5. Retrieval Service
- **Purpose**: Queries structured data (e.g., order history).
- **Tools**:
  - FastAPI: Retrieval endpoint.
  - SQLAlchemy: SQL interactions.
- **GCP Services**:
  - Cloud SQL (PostgreSQL): Structured data storage.
  - Cloud Run: Deploys service.
- **Implementation**:
  - Create endpoint: `/fetch-data`.
  - Query Cloud SQL with SQLAlchemy.
  - Cache queries in Cloud Memorystore (Redis).
  - Deploy: `gcloud run deploy retrieval-service --image gcr.io/[PROJECT_ID]/retrieval --region us-central1`.
- **Why It Works**:
  - Cloud SQL ensures reliable storage.
  - SQLAlchemy simplifies queries.
  - Memorystore reduces latency.

### 6. Guardrails Layer
- **Purpose**: Validates responses for tone, accuracy, and appropriateness.
- **Tools**:
  - FastAPI: Validation endpoint.
  - Sentence Transformers: Similarity checks.
  - Hugging Face Transformers: Toxicity detection.
  - spaCy: Claim extraction.
- **Foundation Model**:
  - Gemini 1.5 Pro (Vertex AI): Tone and hallucination detection.
- **GCP Services**:
  - Vertex AI: Hosts Gemini.
  - Cloud Run: Deploys service.
- **Implementation**:
  - Create endpoint: `/validate-response`.
  - Analyze tone with Gemini.
  - Check accuracy with Sentence Transformers.
  - Extract claims with spaCy; flag ungrounded claims.
  - Filter toxicity with Hugging Face.
  - Deploy: `gcloud run deploy guardrails-service --image gcr.io/[PROJECT_ID]/guardrails --region us-central1`.
- **Why It Works**:
  - Gemini ensures robust validation.
  - Sentence Transformers and spaCy scale checks.
  - Cloud Run handles response volumes.

### 7. PII Redaction Service
- **Purpose**: Masks sensitive information.
- **Tools**:
  - FastAPI: Redaction endpoint.
  - presidio: PII detection.
- **GCP Services**:
  - Cloud Data Loss Prevention (DLP): PII detection.
  - Cloud Run: Deploys service.
  - Cloud Storage: Logs redacted data.
- **Implementation**:
  - Create endpoint: `/redact-pii`.
  - Use presidio and Cloud DLP for PII detection.
  - Mask PII (e.g., “[REDACTED]”).
  - Log to Cloud Storage.
  - Deploy: `gcloud run deploy pii-service --image gcr.io/[PROJECT_ID]/pii --region us-central1`.
- **Why It Works**:
  - Cloud DLP ensures compliance.
  - presidio provides lightweight redaction.
  - Cloud Storage supports secure logging.

### 8. LLM Core
- **Purpose**: Generates responses from prompts.
- **Tools**:
  - FastAPI: Generation endpoint.
  - LangChain: Model integration.
- **Foundation Model**:
  - Gemini 1.5 Pro (Vertex AI): Response generation.
- **GCP Services**:
  - Vertex AI: Hosts Gemini.
  - Cloud Run: Deploys service.
- **Implementation**:
  - Create endpoint: `/generate-response`.
  - Call Gemini with LangChain.
  - Deploy: `gcloud run deploy llm-service --image gcr.io/[PROJECT_ID]/llm --region us-central1`.
- **Why It Works**:
  - Gemini ensures high-quality responses.
  - LangChain streamlines integration.
  - Vertex AI scales inference.

### 9. Escalation Service
- **Purpose**: Routes queries to human agents.
- **Tools**:
  - FastAPI: Escalation endpoint.
  - Pydantic: Request validation.
- **GCP Services**:
  - Cloud Pub/Sub: Queues requests.
  - Cloud Functions: Triggers handoff.
  - Cloud Run: Deploys service.
- **Implementation**:
  - Create endpoint: `/escalate`.
  - Use rules (e.g., confidence < 0.7).
  - Publish to Cloud Pub/Sub.
  - Deploy: `gcloud run deploy escalation-service --image gcr.io/[PROJECT_ID]/escalation --region us-central1`.
- **Why It Works**:
  - Cloud Pub/Sub ensures reliable escalation.
  - Cloud Functions automate workflows.
  - FastAPI simplifies development.

### 10. Human Support System
- **Purpose**: Handles escalated queries.
- **Tools**:
  - Zendesk: Ticketing system.
  - FastAPI: Integration endpoints.
- **GCP Services**:
  - Cloud Functions: Integrates with Zendesk.
  - Cloud Run: Deploys endpoints.
- **Implementation**:
  - Create endpoint: `/human-support`.
  - Use Zendesk APIs for ticket creation.
  - Deploy: `gcloud run deploy human-service --image gcr.io/[PROJECT_ID]/human --region us-central1`.
- **Why It Works**:
  - Zendesk ensures efficient handoff.
  - Cloud Functions integrate with Pub/Sub.
  - FastAPI enables quick APIs.

### 11. Data Storage
- **Purpose**: Stores data, logs, and knowledge bases.
- **Tools**:
  - SQLAlchemy: Structured data.
  - firebase-admin: Firestore interactions.
- **GCP Services**:
  - Cloud SQL (PostgreSQL): Structured data.
  - Cloud Firestore: Vector embeddings.
  - Cloud Storage: Logs.
- **Implementation**:
  - Set up Cloud SQL tables (e.g., `orders`).
  - Configure Firestore for embeddings.
  - Use Cloud Storage for logs.
  - Integrate with SQLAlchemy and firebase-admin.
- **Why It Works**:
  - Cloud SQL and Firestore scale storage.
  - Cloud Storage ensures compliant logging.
  - Tools align with Python workflows.

## Workflow

1. User submits query via Angular UI to API Gateway.
2. Prompt Engineering Service crafts prompt with Gemini 1.5 Flash.
3. RAG Module retrieves context from Firestore; Retrieval Service fetches data from Cloud SQL.
4. LLM Core (Gemini 1.5 Pro) generates response.
5. Guardrails Layer validates response; PII Redaction Service masks sensitive data.
6. Escalation Service routes low-confidence queries to Zendesk via Cloud Pub/Sub.
7. Data and logs stored in Cloud SQL, Firestore, and Cloud Storage.

## Why It Works

- **Modularity**: FastAPI services on Cloud Run enable independent scaling.
- **Scalability**: GCP services auto-scale with demand.
- **Security**: IAP and Cloud DLP protect PII.
- **Accuracy**: RAG, Retrieval, and Guardrails ensure reliable responses.
- **User Experience**: Angular and Zendesk provide a polished interface and handoff.

## Setup

### Prerequisites
- GCP project: `gcloud projects create [PROJECT_ID]`.
- Enable APIs: Vertex AI, Cloud Run, Cloud SQL, Firestore, Cloud Storage, Cloud DLP, Pub/Sub, Functions.
- Install Python 3.9+, Node.js 14+, Angular CLI 11, GCP SDK, Docker.

### Project Structure
```markdown
conversational-ai/
├── ui/                     # Angular frontend
├── api-gateway/            # FastAPI API Gateway
├── prompt-service/         # Prompt Engineering
├── rag-service/            # RAG Module
├── retrieval-service/      # Retrieval Service
├── guardrails-service/     # Guardrails Layer
├── pii-service/            # PII Redaction
├── llm-service/            # LLM Core
├── escalation-service/     # Escalation Service
├── human-service/          # Human Support
└── scripts/                # Deployment scripts
```

### Deployment
- Build Docker images: `docker build -t gcr.io/[PROJECT_ID]/[SERVICE] .`.
- Deploy: `gcloud run deploy ...`.

## Code Snippets

### API Gateway
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    user_id: str
    query_text: str

@app.post("/query")
async def handle_query(request: QueryRequest):
    return {"status": "routed"}
```

### RAG Module
```python
from fastapi import FastAPI
from langchain.embeddings import VertexAIEmbeddings
from google.cloud import firestore

app = FastAPI()
embeddings = VertexAIEmbeddings(model="text-embedding-gecko")
db = firestore.Client()

@app.post("/retrieve-context")
async def retrieve_context(query: str):
    query_embedding = embeddings.embed_query(query)
    docs = db.collection("faqs").order_by("embedding", direction="COSINE").limit(5).get()
    return {"context": [doc.to_dict()["content"] for doc in docs]}
```

### Guardrails Layer
```python
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer, util

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

@app.post("/validate-response")
async def validate_response(response: str, context: list[str]):
    response_embedding = model.encode(response)
    context_embedding = model.encode(context)
    similarity = util.cos_sim(response_embedding, context_embedding).max()
    if similarity < 0.7:
        return {"status": "hallucination_detected"}
    return {"status": "valid"}
```

## Notes

- **Cost Management**: Monitor costs with Cloud Billing; use preemptible instances for savings.
- **Monitoring**: Use Cloud Monitoring and Logging for performance.
- **Testing**: Test with `pytest` (FastAPI) and `Jest` (Angular); use Cloud Build for CI/CD.
```

**Instructions to Download**:
1. Copy the content above (from ` ```markdown` to the closing ` ``` `).
2. Paste into a text editor (