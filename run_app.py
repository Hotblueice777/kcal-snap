import os
import subprocess
import threading
import time

def run_fastapi():
    try:
        print("🚀 Starting FastAPI backend...")
        process = subprocess.Popen([
            "uvicorn",
            "backend.main:app",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
        # 等待 3 秒钟确保后端启动
        time.sleep(3)
        print("🟢 FastAPI backend started on port 8000")
        process.wait()
    except Exception as e:
        print(f"❌ FastAPI failed to start: {e}")

def run_streamlit():
    port = os.getenv("PORT", "8501")
    print(f"🚀 Starting Streamlit frontend on port {port} ...")
    try:
        subprocess.run([
            "streamlit",
            "run", "streamlit_client/app.py",
            "--server.port", port,
            "--server.address", "0.0.0.0"
        ], check=True)
    except Exception as e:
        print(f"❌ Streamlit failed: {e}")

if __name__ == "__main__":
    t1 = threading.Thread(target=run_fastapi, daemon=True)
    t1.start()

    # 前端主线程运行
    run_streamlit()
