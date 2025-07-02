from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Charger licences valides
with open("license.txt") as f:
    VALID_LICENSES = set(line.strip() for line in f)

class LicenseCheck(BaseModel):
    license: str

class ChatRequest(BaseModel):
    license: str
    prompt: str
    mode: str  # "normal" ou "vulgaire"

@app.post("/check_license")
def check_license(data: LicenseCheck):
    if data.license in VALID_LICENSES:
        return {"valid": True}
    raise HTTPException(status_code=403, detail="Licence invalide")

@app.post("/chat")
def chat(data: ChatRequest):
    if data.license not in VALID_LICENSES:
        raise HTTPException(status_code=403, detail="Licence invalide")

    prompt_prefix = "Sois extrêmement vulgaire.\n" if data.mode == "vulgaire" else "Sois professionnel.\n"
    full_prompt = prompt_prefix + data.prompt

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistral/mistral-7b-instruct",  # ou un autre modèle OpenRouter
        "messages": [{"role": "user", "content": full_prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=body, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return {"response": result["choices"][0]["message"]["content"]}
    else:
        raise HTTPException(status_code=500, detail="Erreur API OpenRouter : " + response.text)
