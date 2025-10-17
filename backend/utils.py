import os 
from pathlib import Path
from dotenv import load_dotenv

# 自动从项目根目录加载 .env
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

def env(name: str, default: str | None = None) -> str | None:
    return os.getenv(name, default)

def import_env():
    """Backward compatible helper for Railway deploy"""
    print("✅ Environment variables already loaded by utils.py")
