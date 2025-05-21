from dotenv import load_dotenv
from pathlib import Path

# Load .env.test from the project root
project_root = Path(__file__).resolve().parent
load_dotenv(dotenv_path=project_root / ".env.test")