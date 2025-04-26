# Write Actions Template

This template provides a reusable structure for implementing write actions in a Python-based AI system using FastAPI. Write actions allow the system to generate or modify content, such as writing reports or updating documents, and integrate with external systems.

---

## Overview

The write actions module enables the AI system to perform structured content generation or modification tasks, such as generating a summary report or updating a document in a third-party system (e.g., Confluence). It meets the following requirements:

- **Content Generation**: Produces structured outputs (e.g., reports, summaries).
- **External Integration**: Updates or writes to external systems (e.g., Confluence, Google Drive).
- **Error Handling**: Ensures robust operation with retries and validation.

---

## Template Code

### Prerequisites
- Python 3.9+
- Dependencies: `fastapi`, `pydantic`, `atlassian-python-api`, `requests`
- External service: Confluence API (or another system like Google Drive)

### Code Structure

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from atlassian import Confluence
import requests
from typing import Optional
from retry import retry

# Initialize FastAPI app
app = FastAPI()

# Initialize Confluence client
confluence = Confluence(
    url="https://your-confluence-url",
    username="your-username",
    password="your-api-token"
)

# Pydantic model for write request
class WriteRequest(BaseModel):
    user_id: str
    content: str
    space_key: str
    page_title: str
    parent_page_id: Optional[str] = None

# Validation for content
def validate_content(content: str) -> bool:
    if not content or len(content.strip()) < 10:
        raise HTTPException(status_code=400, detail="Content is too short or empty.")
    return True

# Write action with retry logic
@retry(tries=3, delay=2, backoff=2)
def write_to_confluence(space_key: str, title: str, content: str, parent_page_id: Optional[str] = None) -> str:
    try:
        # Check if page exists
        page = confluence.get_page_by_title(space=space_key, title=title)
        if page:
            # Update existing page
            confluence.update_page(
                page_id=page["id"],
                title=title,
                body=content,
                parent_id=parent_page_id
            )
        else:
            # Create new page
            confluence.create_page(
                space=space_key,
                title=title,
                body=content,
                parent_id=parent_page_id
            )
        return f"Successfully wrote to page '{title}' in space '{space_key}'."
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to write to Confluence: {str(e)}")

# Write endpoint
@app.post("/write")
async def write_document(request: WriteRequest):
    # Step 1: Validate content
    validate_content(request.content)

    # Step 2: Perform write action with retry
    result = write_to_confluence(
        space_key=request.space_key,
        title=request.page_title,
        content=request.content,
        parent_page_id=request.parent_page_id
    )

    return {"message": result}
```

---

## How It Works

1. **Request Handling**:
   - The `/write` endpoint receives a request with the user ID, content to write, and Confluence page details (space key, title, parent page ID).
2. **Validation**:
   - The `validate_content` function ensures the content is not empty or too short.
3. **Write Action**:
   - The `write_to_confluence` function uses `atlassian-python-api` to interact with the Confluence API.
   - It checks if the page exists: if it does, it updates the page; if not, it creates a new page.
   - The `@retry` decorator ensures the operation is retried up to 3 times with exponential backoff in case of network errors.
4. **Response**:
   - Returns a success message or raises an HTTP exception if the operation fails.

---

## Customization Points

- **Target System**: Replace Confluence with another system (e.g., Google Drive using `google-api-python-client`).
- **Validation**: Add more validation rules (e.g., content format, size limits).
- **Retry Logic**: Adjust the retry parameters (tries, delay, backoff) based on system needs.
- **Content Generation**: Integrate with an LLM (e.g., Vertex AI) to generate the content before writing.

---

## Why This Template?

- **Robustness**: Includes validation and retry logic for reliable operation.
- **Flexibility**: Easily adaptable to other external systems (e.g., Google Drive, Slack).
- **Structured Output**: Ensures content is written in a structured, predictable manner.
- **Error Handling**: Handles failures gracefully with retries and meaningful error messages.

This template demonstrates your ability to implement write actions in an AI system, a common task in software engineering roles involving content automation.