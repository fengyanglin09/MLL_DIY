# System Architecture

| Layer       | Service                          | Notes                                   |
|-------------|----------------------------------|-----------------------------------------|
| Frontend    | Cloud Run or Cloud Storage + CDN | Serve static Angular app                |
| Backend     | Cloud Run                        | Containerized API service               |
| Database    | Cloud SQL (PostgreSQL)           | Managed relational DB                   |
| Auth        | Azure Entra ID                   | Federated SSO with JWT                  |
| Secrets     | Secret Manager                   | Store API keys, DB creds securely       |
| Domain      | Cloud DNS                        | Custom domain mapping                   |
| HTTPS       | Cloud Load Balancer (optional)   | Unified HTTPS w/ path routing           |


# Build & Deployment
### Docker + Cloud Build 

- Angular Dockerfile
```markdown
FROM nginx:alpine
COPY dist/your-app /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

- FastApi
```markdown
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```