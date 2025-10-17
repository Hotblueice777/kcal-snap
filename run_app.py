import os
import subprocess
import threading

def run_fastapi():
    # FastAPI 后端监听内部端口（比如 8000），只供 Streamlit 调用
    subprocess.run([
        "uvicorn", 
        "backend.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ], check=True)

def run_streamlit():
    # Streamlit 主进程，监听 Railway 自动分配的公开端口
    port = os.getenv("PORT", "8501")
    subprocess.run([
        "streamlit", 
        "run", "streamlit_client/app.py",
        "--server.port", port,
        "--server.address", "0.0.0.0"
    ], check=True)

if __name__ == "__main__":
    # 后端放后台线程
    t1 = threading.Thread(target=run_fastapi, daemon=True)
    t1.start()

    # 前端作为主服务启动（对应 Railway 公开端口）
    run_streamlit()
