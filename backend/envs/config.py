from pydantic_settings import BaseSettings, SettingsConfigDict
import os

# Get current directory of this file (backend/)
current_directory = os.path.dirname(os.path.realpath(__file__))

# Get ENV value (e.g., "dev", "prod"), default to "dev"
ENV = os.getenv("ENV", "dev")

# Build the full path to the .env.{ENV} file inside the 'envs' folder
env_file_path = os.path.join(current_directory, '..', 'envs', f'.env.{ENV}')

# Print the path to verify
print(f"[CONFIG] ENV={ENV}, loading environment file: {env_file_path}")

# Settings class using Pydantic
class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: str = ""
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_file_encoding="utf-8"
    )

# Instantiate settings

def get_settings():
    return Settings()

# Debug print
print(f"[CONFIG] DATABASE_URL: {get_settings().DATABASE_URL}")
print(f"[CONFIG] DEBUG: {get_settings().DEBUG}")
