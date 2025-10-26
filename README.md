**# 🥗 KcalSnap**

**## 🌟 Overview**

- **\*KcalSnap\*\*** is an AI-driven calorie estimation app that allows users to take a photo of their food and instantly get estimated nutrition information (Calories, Protein, Fat, Carbs).

It integrates:

- 🍳 **\*Azure Custom Vision\*\*** for image recognition
- ⚡ **\*FastAPI\*\*** backend for nutrition logic
- 🎨 **\*Streamlit\*\*** frontend for an interactive demo
  Built as a full-stack AI + data project for the Azure AI Engineering Capstone.

---

**## 🧠 Features**

✅ Upload or capture a food image (JPEG / PNG / WEBP)
✅ AI recognition of food type (via Azure Custom Vision API)
✅ Dynamic portion size adjustment (grams slider)
✅ Add / remove toppings and extra ingredients
✅ Real-time nutrition estimation (Calories, Protein, Fat, Carbs)
✅ Caching for faster repeated predictions

---

**## 🧱 Tech Stack**
| Layer       | Technology                                                         |
| ----------- | ------------------------------------------------------------------ |
| Frontend    | Streamlit                                                          |
| Backend     | FastAPI                                                            |
| AI Model    | Azure Custom Vision                                                |
| Data Source | CSV mapping for base food & addons                                 |
| Language    | Python 3.10+                                                       |
| Libraries   | `pandas`, `requests`, `httpx`, `Pillow`, `cachetools`, `streamlit` |

---

**## 🗂️ Project Structure**

kcal-snap/
├─ backend/
│ ├─ main.py # FastAPI app (prediction + nutrition endpoints)
│ ├─ nutrition.py # CSV data loading and nutrition logic
│ ├─ data/
│ │ ├─ mapping.csv # Base food nutrition data
│ │ ├─ addons.csv # Add-on items (cheese, bacon, etc.)
│ └─ requirements.txt # Backend dependencies
│
├─ streamlit_client/
│ ├─ app.py # Streamlit frontend
│ └─ requirements.txt # Frontend dependencies
│
├─ .gitignore
├─ README.md
└─ docs/

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

Joey Qi
🎨 Artist | 💻 Full-Stack Developer | 🤖 AI Engineer
📍 Calgary, Canada

GitHub: @Hotblueice777

🪪 License
MIT License — free to use and modify with attribution.

“You are what you eat — now with AI precision.”
— KcalSnap

```
