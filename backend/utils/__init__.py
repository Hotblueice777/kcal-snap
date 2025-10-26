import os
from dotenv import load_dotenv

# 自动加载 backend/.env
BASE_DIR = os.path.dirname(__file__)
dotenv_path = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(dotenv_path=os.path.abspath(dotenv_path))

def env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)