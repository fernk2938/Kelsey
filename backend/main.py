from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Chemin absolu du dossier courant (où se trouve ce fichier)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Charger les licences valides depuis license.txt
with open(os.path.join(BASE_DIR, "license.txt")) as f:
    VALID_LICENSES = set(line.strip() for line in f)

class LicenseCheck(BaseModel):
    license: str

class ChatRequest(BaseModel):
    license: str
    prompt: str
    mode: str  # "normal" ou "vulgaire"

# Route API racine (pour test, tu peux la supprimer si tu veux que frontend soit à la racine)
@app.get("/api")
async def root():
    return {"message": "API is up and running"}

@app.post("/api/check_license")
async def check_license(data: LicenseCheck):
    if data.license in VALID_LICENSES:
        return {"valid": True}
    raise HTTPException(status_code=403, detail="Licence invalide")

@app.post("/api/chat")
async def chat(data: ChatRequest):
    if data.license not in VALID_LICENSES:
        raise HTTPException(status_code=403, detail="Licence invalide")

    prompt_prefix = "Sois extrêmement vulgaire.\n" if data.mode == "vulgaire" else "Sois professionnel.\n"
    full_prompt = prompt_prefix + data.prompt

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistral/mistral-7b-instruct",  # Remplace par ton modèle
        "messages": [{"role": "user", "content": full_prompt}]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erreur API OpenRouter: {e}")

    data_response = response.json()
    answer = data_response.get("choices", [{}])[0].get("message", {}).get("content", "")

    return {"response": answer}

# Servir le frontend statique depuis / (racine)
app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "frontend"), html=True), name="frontend")
