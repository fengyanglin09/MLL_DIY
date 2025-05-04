# Updated System Architecture Description

This document describes the updated system architecture diagram for a conversational AI application, such as a customer support chatbot. The architecture addresses the requirements: **Prompt Engineering**, **Retrieval-Augmented Generation (RAG)**, **Guardrails for Tone and Hallucination**, **PII Redaction**, **Retrieval (e.g., FAQs, order history)**, and **Escalation Routing**. The diagram has been clarified to highlight the distinct roles of the **Retrieval Service** (structured data queries) and the **RAG Module**’s connection to the **Vector DB** within **Data Storage** for semantic retrieval.

## System Architecture Overview

The architecture is a modular, scalable system designed to handle user queries efficiently. Each component addresses specific requirements, ensuring security, accuracy, and user-friendliness. The flow starts with user input, processes through specialized services, and delivers a response or escalates to human support. The updated diagram clarifies the **Retrieval Service**’s focus on structured data and the **RAG Module**’s use of a vector database for semantic searches.

## Components and Their Roles

1. **User Interface (UI)**

   - **Role**: The front-end (web/mobile app) where users submit queries.
   - **Contribution**: Provides an accessible entry point for user interactions.
   - **Meets Requirements**: Facilitates all user-driven interactions (e.g., FAQs, order history).

2. **API Gateway**

   - **Role**: Handles request routing, authentication, and load balancing.
   - **Contribution**: Ensures secure and efficient request processing.
   - **Meets Requirements**: Supports secure access for private/sensitive data and escalation routing.

3. **Prompt Engineering Service**

   - **Role**: Optimizes queries into effective prompts for the LLM, incorporating context.
   - **Contribution**: Enhances LLM performance for relevant, accurate responses.
   - **Meets Requirements**: Addresses **Prompt Engineering** for complex queries.

4. **RAG Module (Retrieval-Augmented Generation)**

   - **Role**: Retrieves unstructured context (e.g., FAQs, knowledge base) from a vector database using embeddings and injects it into the LLM prompt.
   - **Contribution**: Provides contextually grounded responses, reducing hallucinations.
   - **Meets Requirements**: Implements **RAG** and supports **Retrieval** for unstructured data.
   - **Clarification**: Connects to the **Vector DB** in **Data Storage** for semantic, similarity-based searches (eigne.g., finding relevant FAQs for “return policy”).

5. **Retrieval Service**

   - **Role**: Queries structured databases (e.g., FAQ database, order history DB) for specific, deterministic data.
   - **Contribution**: Provides precise retrieval for user-specific or predefined queries.
   - **Meets Requirements**: Supports **Retrieval** for structured data (e.g., order status, FAQ lookups).
   - **Clarification**: Handles structured queries (e.g., SQL-based) for exact matches, such as fetching “Order #123 status” from the order history database, complementing the RAG Module’s semantic retrieval.

6. **Guardrails Layer**

   - **Role**: Validates LLM responses for tone, factual accuracy, and appropriateness.
   - **Contribution**: Ensures responses align with brand voice and avoid incorrect or harmful content.
   - **Meets Requirements**: Addresses **Guardrails for Tone and Hallucination** by enforcing response quality.

7. **PII Redaction Service**

   - **Role**: Detects and masks sensitive information (e.g., names, credit card numbers).
   - **Contribution**: Protects user privacy and ensures compliance (e.g., GDPR, CCPA).
   - **Meets Requirements**: Handles **Private/Sensitive Info** by redacting PII.

8. **LLM Core**

   - **Role**: The core language model that processes prompts and generates responses.
   - **Contribution**: Powers conversational capabilities.
   - **Meets Requirements**: Central to all requirements, generating responses for RAG, retrieval, and escalation.

9. **Escalation Service**

   - **Role**: Evaluates LLM confidence and routes queries to human agents based on rules.
   - **Contribution**: Ensures complex queries are handled by humans.
   - **Meets Requirements**: Implements **Escalation Routing** for human handoff.

10. **Human Support System**

    - **Role**: A ticketing system for customer support agents to handle escalated queries.
    - **Contribution**: Provides a fallback for unresolved queries.
    - **Meets Requirements**: Supports **Escalation Routing**.

11. **Data Storage**

    - **Role**: Stores user data, logs, knowledge bases, and a vector database.
    - **Contribution**: Central repository for retrieval, logging, and auditing.
    - **Meets Requirements**: Supports **Retrieval** and **PII Redaction**.
    - **Clarification**: Includes a **Vector DB** for RAG’s semantic searches and structured databases for the Retrieval Service’s queries.

## How Components Work Together

1. **User Interaction**
   - A user submits a query (e.g., “Track my order #123”) via the **UI**.
   - The **API Gateway** authenticates and routes it to the **Prompt Engineering Service**.

2. **Prompt Optimization and Context Retrieval**
   - The **Prompt Engineering Service** refines the query into an optimized prompt.
   - It queries the **RAG Module** for unstructured context (e.g., FAQs) from the **Vector DB** in **Data Storage** and the **Retrieval Service** for structured data (e.g., order status) from structured databases.
   - The **RAG Module** embeds context into the prompt.

3. **Response Generation**
   - The prompt is sent to the **LLM Core**, which generates a response (e.g., “Order #123 is shipped”).
   - The response is passed to the **Guardrails Layer**.

4. **Response Validation and Security**
   - The **Guardrails Layer** validates tone, accuracy, and appropriateness, checking for hallucinations by comparing with RAG and Retrieval data.
   - The **PII Redaction Service** masks sensitive information.
   - Redacted data is logged in **Data Storage**.

5. **Escalation Check**
   - The **Escalation Service** evaluates LLM confidence and query complexity.
   - If needed (e.g., “Cancel my account”), the query is routed to the **Human Support System**.
   - Otherwise, the response is sent via the **API Gateway** to the **UI**.

6. **Human Handoff (if needed)**
   - Escalated queries are handled by the **Human Support System**, with outcomes logged in **Data Storage**.
   - The user is updated via the **UI**.

## Why Components Meet Requirements

1. **Prompt Engineering**
   - The **Prompt Engineering Service** crafts precise prompts, ensuring LLM accuracy for complex queries.

2. **RAG**
   - The **RAG Module** fetches unstructured context from the **Vector DB**, grounding responses to reduce hallucinations.

3. **Guardrails for Tone and Hallucination**
   - The **Guardrails Layer** enforces tone and validates responses against RAG and Retrieval data, preventing fabricated information through:
     - **Tone Control**: Uses rules or models to ensure brand-appropriate tone (e.g., formal).
     - **Factual Accuracy**: Cross-references with retrieved data (e.g., order status).
     - **Hallucination Detection**: Flags ungrounded claims (e.g., invented policies) by comparing with context, using similarity scoring or confidence analysis.
     - **Appropriateness**: Filters harmful content with toxicity detection.

4. **Handling Private/Sensitive Info (PII Redaction)**
   - The **PII Redaction Service** masks sensitive data, with logs in **Data Storage** for compliance.

5. **Retrieval (FAQs, Order History)**
   - The **Retrieval Service** handles structured queries (e.g., order status) for precise lookups, while the **RAG Module** retrieves unstructured data (e.g., FAQs) via the **Vector DB**, covering all retrieval needs.

6. **Escalation Routing**
   - The **Escalation Service** routes complex queries to the **Human Support System** based on confidence scores.

## Clarifications on Retrieval Service and RAG

- **Retrieval Service vs. RAG Module**:
  - The **Retrieval Service** focuses on **structured data queries** (e.g., SQL-based lookups for order history or FAQs), providing exact matches for user-specific data.
  - The **RAG Module** performs **semantic retrieval** from the **Vector DB** in **Data Storage**, using embeddings for unstructured data (e.g., knowledge base articles).
  - **Why Both**: Structured queries (Retrieval Service) are faster for exact matches, while semantic searches (RAG) excel for contextual relevance. This ensures comprehensive coverage for all query types.
  - **Interaction**: The **Prompt Engineering Service** determines when to use each, combining their outputs for a cohesive prompt.

## Why This Architecture is Effective

- **Modularity**: Components are specialized, enabling easy maintenance and upgrades.
- **Security**: **PII Redaction Service** and **API Gateway** protect sensitive data.
- **Accuracy**: **RAG**, **Retrieval Service**, and **Guardrails** ensure data-driven, hallucination-free responses.
- **User Experience**: **Prompt Engineering**, **Escalation Service**, and **Human Support System** deliver relevant responses or human handoff.
- **Compliance**: Logging and PII redaction support regulatory requirements.