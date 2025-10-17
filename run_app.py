import os
import subprocess
import threading

def run_fastapi():
    port = os.getenv("PORT", "8000")  # Railway 自动分配 PORT
    subprocess.run([
        "uvicorn", 
        "backend.main:app", 
        "--host", "0.0.0.0", 
        "--port", port
    ], check=True)

def run_streamlit():
    subprocess.run([
        "streamlit", 
        "run", "streamlit_client/app.py", 
        "--server.port", "8501", 
        "--server.address", "0.0.0.0"
    ], check=True)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_fastapi)
    t2 = threading.Thread(target=run_streamlit)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
