## Architecture
1. Backend: FastAPI
2. Model/LLM: transformers or OpenAI or llama-cpp-python
3. Frontend: Angular
4. Environment & Dependency Management - conda with a environment.yml

## folder structure
llm-app/
│
├── backend/
│   ├── main.py          # FastAPI app
│   ├── models/          # Model loading & logic
│   ├── api/             # API endpoints
│   └── utils/           # Helper functions
│
├── frontend/            # Angular or React project
│   └── ...
│
├── environment.yml      # Conda env setup
└── README.md

## Deployment
Docker
Cloud