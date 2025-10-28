# backend/main.py
from __future__ import annotations
import io, json
import logging
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from PIL import Image, ExifTags
from cachetools import TTLCache

from utils import env
from rate_limit import RateLimiter
from nutrition import NutritionRepo, NutriCache, calc_totals

app = FastAPI(title="KcalSnap API", version="0.1.0")

# CORS
origins = [o.strip() for o in (env("ALLOWED_ORIGINS","*") or "*").split(",")]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)
# Rate limit
app.middleware("http")(RateLimiter(max_per_min=60))

# Nutrition data
repo = NutritionRepo("backend/data/mapping.csv", "backend/data/addons.csv")
nutri_cache = NutriCache()

# --- Schemas ---
class TopKItem(BaseModel):
    label: str
    score: float

class PredictResponse(BaseModel):
    topk: List[TopKItem]
    chosen: str

class NutritionResponse(BaseModel):
    totals: dict
    range: dict
    source: str = "local-mapping-v1"
    cached: bool = False

# --- Helpers ---
def _fix_orientation(img: Image.Image) -> Image.Image:
    try:
      for orientation in ExifTags.TAGS.keys():
          if ExifTags.TAGS[orientation]=='Orientation':
              break
      exif=dict(img._getexif().items()) if hasattr(img, "_getexif") and img._getexif() else {}  # type: ignore
      o = exif.get(orientation)
      if o == 3: img = img.rotate(180, expand=True)
      elif o == 6: img = img.rotate(270, expand=True)
      elif o == 8: img = img.rotate(90, expand=True)
    except Exception:
      pass
    return img

async def azure_predict(image_bytes: bytes) -> list[TopKItem]:
    endpoint = env("AZURE_CV_ENDPOINT")
    project_id = env("AZURE_CV_PROJECT_ID")
    published_name = env("AZURE_CV_PUBLISHED_NAME")
    key = env("AZURE_CV_PREDICTION_KEY")
    if not (endpoint and project_id and published_name and key):
        return [TopKItem(label="burger", score=0.82),
                TopKItem(label="sandwich", score=0.11),
                TopKItem(label="steak", score=0.07)]
    url = f"{endpoint.rstrip('/')}/customvision/v3.0/Prediction/{project_id}/classify/iterations/{published_name}/image"
    headers = {"Prediction-Key": key, "Content-Type": "application/octet-stream"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, headers=headers, content=image_bytes)
        r.raise_for_status()
        data = r.json()
    preds = []
    for p in data.get("predictions", [])[:3]:
        preds.append(TopKItem(label=p["tagName"], score=p["probability"]))
    return preds

# --- Routes ---
@app.post("/api/predict", response_model=PredictResponse)
async def predict(image: UploadFile = File(...)):

    if image.content_type not in ("image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"):
        raise HTTPException(400, "Unsupported image type")

    # Resize to a maximum dimension of 512 & apply rotation correction
    raw = await image.read()
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    img = _fix_orientation(img)
    w, h = img.size
    max_side = max(w, h)
    if max_side > 512:
        scale = 512 / max_side
        img = img.resize((int(w * scale), int(h * scale)))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=80)
    jpeg_bytes = buf.getvalue()

    topk = await azure_predict(jpeg_bytes)
    chosen = topk[0].label if topk else repo.find_label_by_keyword(image.filename or "") or "unknown"
    return PredictResponse(topk=topk, chosen=chosen)


@app.get("/api/addons")
async def get_addons(label: str):
    
    """Return a list of optional add-on ingredients for the specified food label"""
    try:
        addons = repo.get_addons_for_label(label)
        return addons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nutrition", response_model=NutritionResponse)
async def nutrition(label: str, grams: int = 180, addons: Optional[str] = ""):
    base = repo.get_base(label)
    if not base:
        raise HTTPException(404, f"Unknown label: {label}")

    addon_ids = [a for a in (addons or "").split(",") if a]
    # Retrieve add-on details from the CSV
    addon_rows = []
    for aid in addon_ids:
        row = repo.addons[repo.addons["addon"] == aid]
        if not row.empty: addon_rows.append(row.iloc[0].to_dict())

    cached = nutri_cache.get(label, grams, addon_ids)
    if cached:
        return NutritionResponse(**cached, cached=True)

    result = calc_totals(base, grams, addon_rows)
    payload = {"totals": result["totals"], "range": result["range"], "source": "local-mapping-v1"}
    nutri_cache.set(label, grams, addon_ids, payload)
    return NutritionResponse(**payload)

# Import Azure assistant API module
from assistant_api import app as assistant_app
app.mount("/assistant", assistant_app)

# Healthcheck Root----for Railway deploy
@app.get("/")
async def root():
    return {"status": "ok", "message": "KcalSnap backend running successfully"}

logger = logging.getLogger("uvicorn")
logger.info("✅ FastAPI main app started successfully!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

