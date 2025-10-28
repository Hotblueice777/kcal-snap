**# 🥗 KcalSnap**

**## 🌟 Overview**

- **\*KcalSnap\*\*** is an AI-driven calorie estimation app that allows users to take a photo of their food and instantly get estimated nutrition information (Calories, Protein, Fat, Carbs).
- <img width="600" alt="image" src="https://github.com/user-attachments/assets/28914c48-f65e-4cde-8b4d-81d5e0d733b7" />
  <img width="600" alt="image" src="https://github.com/user-attachments/assets/782d4d07-d938-47de-9dbe-58e021f87bf3" />
  <img width="400" alt="image" src="https://github.com/user-attachments/assets/80032194-aae7-4a13-a3d3-61949a15b91f" />
  <img width="600" alt="image" src="https://github.com/user-attachments/assets/1632261a-0780-4c91-a200-890a8ca74552" />
  <img width="600"  alt="image" src="https://github.com/user-attachments/assets/5a41552b-2434-42a1-8d9e-43087c384991" />
  <img width="600"  alt="image" src="https://github.com/user-attachments/assets/e2a49e6f-12e1-4e8f-bd4f-5191346575a6" />

---

It integrates:

- 🍳 **Azure Custom Vision** for food image recognition
- 🎙️ **Azure Speech Service** for voice input and transcription
- 💬 **Azure Language Service (RAG QnA)** for intelligent nutrition and health Q&A
- 🧠 **Azure OpenAI Service** as a fallback conversational layer
- ⚡ **FastAPI** backend for prediction and nutrition data processing
- 🎨 **Streamlit** frontend for an interactive user experience

Built as a full-stack AI + data project for the **Azure AI Engineering Capstone**.

---

## 🧠 Features

✅ Upload or capture a food image (JPEG / PNG / WEBP)  
✅ AI recognition of food type (via Azure Custom Vision API)  
✅ Real-time nutrition estimation (Calories, Protein, Fat, Carbs)  
✅ Dynamic portion size adjustment (grams slider)  
✅ Add / remove toppings and extra ingredients  
✅ Daily meal summary and total nutrition tracking  
✅ Voice-based input and interaction (Azure Speech Service)  
✅ Intelligent Q&A assistant powered by RAG (Azure Language Service)  
✅ Fallback conversational mode via Azure OpenAI API  
✅ Local caching for faster repeated predictions  
✅ Ready for third-party nutrition API integration in future versions

---

## 🧱 Tech Stack

| Layer       | Technology                                                                                                |
| ----------- | --------------------------------------------------------------------------------------------------------- |
| Frontend    | **Streamlit** — Interactive UI for food recognition and AI assistant                                      |
| Backend     | **FastAPI** — RESTful API for prediction, nutrition logic, and RAG                                        |
| AI Services | **Azure Custom Vision**, **Azure Speech Service**, **Azure Language Service (RAG QnA)**, **Azure OpenAI** |
| Data Source | Local **CSV mapping** for base food items and add-ons (expandable to API)                                 |
| Language    | **Python 3.10+**                                                                                          |
| Libraries   | `pandas`, `requests`, `httpx`, `Pillow`, `cachetools`, `streamlit`, `fastapi`                             |
| Deployment  | Azure / Render (for API & Streamlit deployment)                                                           |

---

**## 🗂️ Project Structure**

```
kcal-snap/
├── backend/
│ ├── main.py
│ ├── nutrition.py
│ ├── assistant_api.py
│ ├── assistant_rag.py
│ ├── rate_limit.py
│ ├── utils/
│ ├── faiss_index.bin
│ ├── faiss_texts.txt
│ ├── data/
│ │ ├── mapping.csv
│ │ ├── addons.csv
│ ├── requirements.txt
│ └── .env.example
│
├── streamlit_client/
│ ├── app.py
│ ├── scan_page.py
│ ├── meal_page.py
│ ├── assistant_page.py
│ ├── components/
│ │ └── voice_recorder/
│ ├── .streamlit/
│ │ ├── config.toml
│ │ └── secrets.toml
│ ├── requirements.txt
│ └── README.md
│
├── runtime.txt
├── README.md
└── .gitignore
```

---

**## ⚙️ Installation**

**### 1️⃣ Clone the Repository**

```bash

git clone https://github.com/Hotblueice777/kcal-snap.git
cd kcal-snap

2️⃣ Set Up Backend (FastAPI)
cd backend
python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
Run the backend:
uvicorn main:app --reload --port 8000
Backend will start at http://localhost:8000

3️⃣ Set Up Frontend (Streamlit)
Open a new terminal:
cd streamlit_client
python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate
pip install -r requirements.txt
Run the Streamlit app:
streamlit run app.py
Frontend will open at http://localhost:8501

🧩 Configuration
Add a .env file in backend/ with your Azure keys:
AZURE_CV_ENDPOINT=<your-endpoint>
AZURE_CV_PROJECT_ID=<your-project-id>
AZURE_CV_PUBLISHED_NAME=Iteration1
AZURE_CV_PREDICTION_KEY=<your-prediction-key>
ALLOWED_ORIGINS=http://localhost:8501
If no Azure credentials are provided,
the app will automatically switch to mock data mode for local testing.

🧾 Example Screenshots
Upload & Predict    Nutrition Breakdown

🚀 Deployment

Option 1 — Deploy Backend to Azure App Service
az webapp up --name kcal-snap-backend --resource-group <your-group> --runtime "PYTHON:3.10"

Option 2 — Deploy Frontend to Streamlit Cloud
Push the repo to GitHub
Go to streamlit.io/cloud
Select your repo and deploy the /streamlit_client/app.py entry

🧑‍💻 Author

Joey
🎨 Artist | 💻 Full-Stack Developer | 🤖 AI Engineer
📍 Calgary, Canada

GitHub: @Hotblueice777

🪪 License
MIT License — free to use and modify with attribution.

“You are what you eat — now with AI precision.”
— KcalSnap

```
