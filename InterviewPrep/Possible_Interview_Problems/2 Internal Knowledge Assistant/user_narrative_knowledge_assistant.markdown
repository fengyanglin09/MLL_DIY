# User Narrative: Using the Internal Knowledge Assistant

This narrative follows Sarah, an employee at a tech company, as she uses the Internal Knowledge Assistant to find recent project updates across Confluence, Google Drive, and Slack. It illustrates how the system’s components—Angular Frontend, FastAPI Backend, and GCP Infrastructure with a Foundational Model—work together to meet the requirements of semantic search with Retrieval-Augmented Generation (RAG), secure user authentication with role-based access control (RBAC), multi-source document indexing, and temporal relevance.

---

## Sarah’s Experience with the Internal Knowledge Assistant

### Logging In and Authentication
Sarah starts her day by opening her browser and navigating to the Internal Knowledge Assistant, a web app hosted on Firebase Hosting. The app’s interface, built with **Angular**, greets her with a clean login page featuring a “Sign in with Google” button. Sarah clicks it, and behind the scenes, **Firebase Authentication** (a GCP service) handles her login. Since her company uses Google Workspace, her Google account seamlessly authenticates her.

- **How It Works**:
  - The Angular frontend integrates with Firebase Authentication’s client-side SDK to initiate Google SSO.
  - Firebase verifies Sarah’s identity and issues a JWT token, which Angular stores in local storage for subsequent API requests.
  - Firebase also checks Sarah’s role (stored in Firestore or custom claims) to determine her access level—Sarah is a project manager, so she has access to most project-related documents but not HR files.
- **Requirement Met**: **User Authentication and RBAC**—Firebase ensures secure authentication, and RBAC restricts Sarah’s access based on her role.

### Searching for Recent Project Updates
After logging in, Sarah sees the main search interface, a sleek Angular component styled with Angular Material. She types her query into the search bar: “recent project updates for Q1 2025.” The Angular frontend sends this query to the **FastAPI Backend** via a REST API call, including Sarah’s JWT token in the request headers.

- **How It Works**:
  - **Angular Frontend**: Uses `HttpClient` to send a POST request to the FastAPI `/search` endpoint with the query and Sarah’s JWT token.
  - **FastAPI Backend**: Receives the request and verifies the JWT token using Firebase Authentication’s Admin SDK to confirm Sarah’s identity and fetch her role/permissions.
  - **GCP Infrastructure (Firestore)**: FastAPI queries Firestore to retrieve Sarah’s permissions, ensuring only documents she has access to are included in the search results.
- **Requirement Met**: **User Authentication and RBAC**—The system ensures Sarah only sees documents she’s authorized to access.

### Semantic Search with RAG and Foundational Model
The FastAPI backend processes Sarah’s query using the RAG pipeline, leveraging the **Foundational Model** hosted on **Vertex AI**. It first generates an embedding for her query (“recent project updates for Q1 2025”) using the Foundational Model’s embedding capabilities (e.g., `text-embedding-gecko`). This embedding is then used to search for relevant documents in the vector database.

- **How It Works**:
  - **FastAPI Backend**: Sends the query to the Foundational Model on Vertex AI to generate an embedding, a numerical representation capturing the query’s semantic meaning.
  - **GCP Infrastructure (Firestore/Pinecone)**: FastAPI queries the vector database (Firestore or Pinecone) for the top-k documents whose embeddings are most similar to the query’s embedding. The search filters out documents Sarah doesn’t have permission to access (e.g., HR files).
  - **Temporal Relevance**: The backend applies a recency boost to the search results. Documents are scored using a hybrid formula: `score = semantic_similarity + recency_weight * (current_timestamp - last_modified)`. This ensures recent documents (e.g., a Confluence page updated last week) are prioritized over older ones (e.g., a Slack message from 2023).
  - **RAG Pipeline with Foundational Model**: The top-k documents—say, a Confluence page titled “Q1 2025 Project Plan,” a Google Drive document with meeting notes, and a recent Slack thread—are passed to the Foundational Model (e.g., PaLM 2) on Vertex AI. The Foundational Model generates a natural language answer: “The Q1 2025 project updates include a new timeline discussed in a Confluence page last updated on April 15, 2025, and action items assigned in a Slack thread from April 18, 2025.”
  - **FastAPI Backend**: Returns the Foundational Model’s answer and document snippets (with metadata like source and last modified date) to the Angular frontend.
- **Requirements Met**:
  - **RAG with Vector DBs**: Semantic search using embeddings and the Foundational Model’s natural language generation provide accurate, context-aware results.
  - **Temporal Relevance**: The recency boost ensures Sarah sees the most recent updates first.

### Displaying Results
Back on Sarah’s screen, the Angular frontend receives the response from FastAPI and renders the results. The interface displays:
- A natural language summary at the top: “The Q1 2025 project updates include a new timeline discussed in a Confluence page last updated on April 15, 2025, and action items assigned in a Slack thread from April 18, 2025,” generated by the Foundational Model.
- A list of document snippets below, each shown in an Angular Material card with metadata:
  - “Q1 2025 Project Plan” (Confluence, last modified April 15, 2025)
  - “Meeting Notes Q1 2025” (Google Drive, last modified April 10, 2025)
  - “Slack Thread: Action Items” (Slack, posted April 18, 2025)

Sarah notices the Slack thread is the most recent and clicks to view the full message, which opens a link to Slack in a new tab.

- **How It Works**:
  - **Angular Frontend**: Uses Angular Material components (`mat-card`, `mat-list`) to display the Foundational Model’s answer and document snippets. Metadata like the last modified date is formatted using Angular pipes (`date:'medium'`).
  - **Temporal Relevance**: The frontend highlights the most recent document (the Slack thread) based on the backend’s recency score, making it easy for Sarah to focus on the latest updates.
- **Requirement Met**: **Temporal Relevance**—The interface prioritizes and clearly displays recent information.

### Behind the Scenes: Document Indexing
While Sarah uses the system, the backend ensures the data she’s searching is up-to-date. Overnight, **Cloud Scheduler** (a GCP service) triggers an indexing job by calling the FastAPI `/index` endpoint. This keeps the vector database current with the latest documents from Confluence, Google Drive, and Slack.

- **How It Works**:
  - **GCP Infrastructure (Cloud Scheduler)**: Runs a scheduled job at midnight to invoke the `/index` endpoint.
  - **FastAPI Backend**: Fetches new or updated content using APIs:
    - **Confluence**: Atlassian REST API retrieves pages and attachments.
    - **Google Drive**: Google Drive API fetches files (Docs, Sheets, PDFs).
    - **Slack**: Slack API retrieves messages and files from channels Sarah has access to.
  - **Document Processing**: FastAPI extracts text from documents (e.g., using `PyPDF2` for PDFs or Google Cloud Document AI for complex files).
  - **Embedding Generation with Foundational Model**: FastAPI generates embeddings for the documents using the Foundational Model on Vertex AI and stores them in the vector database (Firestore or Pinecone) along with metadata (e.g., `last_modified`, `permissions`).
  - **GCP Infrastructure (Secret Manager)**: FastAPI retrieves API credentials securely from Secret Manager to authenticate with Confluence, Google Drive, and Slack.
  - **GCP Infrastructure (Cloud Storage)**: Optionally stores raw documents (e.g., PDFs) for backup or further processing.
- **Requirement Met**: **Multi-Source Document Indexing**—The system continuously indexes content from multiple sources, ensuring Sarah has access to the latest information.

### Security and Access Control
As Sarah searches, the system ensures she only sees documents she’s authorized to access. For example, a Slack channel for HR discussions isn’t included in her results because her role doesn’t grant access.

- **How It Works**:
  - **FastAPI Backend**: During the search, FastAPI checks Sarah’s permissions (stored in Firestore) against each document’s access control list (e.g., Confluence space permissions, Google Drive ACLs, Slack channel memberships).
  - **GCP Infrastructure (Firestore)**: Stores document permissions, allowing FastAPI to filter results dynamically.
  - **GCP Infrastructure (Firebase Authentication)**: Ensures Sarah’s identity is verified with every request via her JWT token.
- **Requirement Met**: **User Authentication and RBAC**—The system enforces secure access, protecting sensitive data.

### System Maintenance
While Sarah works, the system is monitored for performance. **Cloud Monitoring and Logging** track API latency, indexing errors, Foundational Model inference times, and user activity, ensuring the system runs smoothly.

- **How It Works**:
  - **GCP Infrastructure (Cloud Monitoring/Logging)**: Logs FastAPI requests, Foundational Model inference metrics, and errors, providing visibility into system health. Alerts are set up for issues like high error rates.
  - **GCP Infrastructure (Cloud Run)**: Auto-scales the FastAPI backend to handle increased user load, ensuring responsiveness.
- **Support for Requirements**: Ensures the system remains reliable, supporting all requirements by maintaining uptime and performance.

---

## How Components Work Together

1. **User Interaction**:
   - Sarah interacts with the **Angular Frontend**, which provides a seamless UI for login and search.
   - **Firebase Authentication** (GCP) handles her login and enforces RBAC, ensuring secure access.

2. **Search and RAG**:
   - The Angular frontend sends Sarah’s query to the **FastAPI Backend**.
   - FastAPI uses the **Foundational Model** on **Vertex AI** (GCP) to generate embeddings and query the vector database (**Firestore** or **Pinecone**), filtering by Sarah’s permissions.
   - Temporal relevance is applied by boosting recent documents, and the Foundational Model generates a natural language answer.
   - FastAPI returns the results to Angular, which displays them with metadata.

3. **Indexing**:
   - **Cloud Scheduler** (GCP) triggers nightly indexing via FastAPI.
   - FastAPI fetches content from Confluence, Google Drive, and Slack, using credentials from **Secret Manager** (GCP).
   - Documents are processed, embedded using the Foundational Model, and stored in the vector database, ensuring Sarah always has access to the latest data.

4. **Security and Monitoring**:
   - **Firebase Authentication** and **Firestore** enforce RBAC throughout the process.
   - **Cloud Monitoring/Logging** and **Cloud Run** (GCP) ensure the system is performant and reliable, including Foundational Model inference.

---

## Conclusion

From Sarah’s perspective, the Internal Knowledge Assistant is a seamless tool that quickly finds relevant, recent project updates while ensuring she only sees authorized content. Behind the scenes, the Angular frontend, FastAPI backend, and GCP infrastructure with the Foundational Model work in harmony to deliver a secure, efficient, and up-to-date search experience, meeting all requirements effectively.