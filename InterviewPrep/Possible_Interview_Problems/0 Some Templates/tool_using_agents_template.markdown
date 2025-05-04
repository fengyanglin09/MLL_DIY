# Tool-Using Agents Template

This template provides a reusable structure for implementing tool-using agents in a Python-based AI system using FastAPI. Tool-using agents leverage external tools (e.g., APIs, databases, utilities) to perform tasks like fetching data, running computations, or triggering workflows.

---

## Overview

The tool-using agents module enables the AI system to delegate tasks to external tools, such as querying a database, calling an API, or running a computation. It meets the following requirements:

- **Task Delegation**: Offloads specific tasks to appropriate tools.
- **Error Handling**: Manages failures and timeouts gracefully.
- **Extensibility**: Supports adding new tools easily.

---

## Template Code

### Prerequisites
- Python 3.9+
- Dependencies: `fastapi`, `pydantic`, `requests`, `google-cloud-bigquery`, `apache-commons-math`
- External service: Google BigQuery (for database queries)

### Code Structure

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import bigquery
from google.api_core import retry
import requests
from typing import Dict, Any
from apachecommonsmath import ApacheCommonsMath  # Custom wrapper for Apache Commons Math

# Initialize FastAPI app
app = FastAPI()

# Initialize BigQuery client
bigquery_client = bigquery.Client()

# Tool definitions
class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register_tool(self, name: str, func):
        self.tools[name] = func

    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        if tool_name not in self.tools:
            raise HTTPException(status_code=400, detail=f"Tool '{tool_name}' not found.")
        return await self.tools[tool_name](params)

# Initialize tool registry
tools = ToolRegistry()

# Tool 1: BigQuery query tool
@retry.Retry(predicate=retry.if_transient_error)
async def query_bigquery(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    query = params.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required.")
    try:
        query_job = bigquery_client.query(query)
        results = query_job.result()
        return [dict(row) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BigQuery error: {str(e)}")

# Tool 2: API call tool
async def call_external_api(params: Dict[str, Any]) -> Dict[str, Any]:
    url = params.get("url")
    headers = params.get("headers", {})
    if not url:
        raise HTTPException(status_code=400, detail="URL parameter is required.")
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API call error: {str(e)}")

# Tool 3: Statistical computation tool
async def compute_statistics(params: Dict[str, Any]) -> Dict[str, Any]:
    data = params.get("data")
    if not data or not isinstance(data, list):
        raise HTTPException(status_code=400, detail="Data parameter must be a non-empty list.")
    try:
        stats = ApacheCommonsMath()
        return {
            "mean": stats.mean(data),
            "median": stats.median(data),
            "std_dev": stats.standard_deviation(data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Statistics error: {str(e)}")

# Register tools
tools.register_tool("bigquery_query", query_bigquery)
tools.register_tool("call_api", call_external_api)
tools.register_tool("compute_stats", compute_statistics)

# Pydantic model for tool request
class ToolRequest(BaseModel):
    tool_name: str
    params: Dict[str, Any]

# Tool execution endpoint
@app.post("/execute_tool")
async def execute_tool(request: ToolRequest):
    result = await tools.execute_tool(request.tool_name, request.params)
    return {"result": result}
```

---

## How It Works

1. **Tool Registry**:
   - The `ToolRegistry` class manages a collection of tools, allowing dynamic registration and execution.
2. **Tool Definitions**:
   - **BigQuery Query Tool**: Queries Google BigQuery for structured data, with retry logic for transient errors.
   - **API Call Tool**: Makes HTTP requests to external APIs, with timeout and error handling.
   - **Statistical Computation Tool**: Uses Apache Commons Math (a Java library wrapped for Python) to compute statistics like mean, median, and standard deviation.
3. **Execution**:
   - The `/execute_tool` endpoint receives a tool name and parameters, delegates the task to the appropriate tool, and returns the result.
4. **Error Handling**:
   - Each tool includes validation and exception handling to ensure robust operation.

---

## Customization Points

- **New Tools**: Add more tools by defining new functions and registering them with `tools.register_tool`.
- **Tool Parameters**: Extend the `params` dictionary to support more complex inputs.
- **Error Handling**: Add more sophisticated retry logic or logging.
- **Tool Integration**: Replace BigQuery with another database (e.g., PostgreSQL) or add more APIs.

---

## Why This Template?

- **Extensibility**: The `ToolRegistry` makes it easy to add new tools without modifying the core logic.
- **Robustness**: Includes retry logic, timeouts, and error handling for reliable operation.
- **Versatility**: Supports a variety of tasks (database queries, API calls, computations) relevant to AI systems.
- **Clarity**: Demonstrates a clean, modular approach to tool integration.

This template showcases your ability to design and implement tool-using agents, a key skill in AI software engineering.