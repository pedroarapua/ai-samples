import os

from dotenv import load_dotenv


load_dotenv()


OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:8b",
)

MAX_RETRIES = int(
    os.getenv(
        "MAX_RETRIES",
        "2",
    )
)
