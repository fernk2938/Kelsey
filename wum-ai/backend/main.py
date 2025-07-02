from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI()

with open("license.txt") as f:
    VALID_LICENSES = set(line.strip() for line in f)

class LicenseCheck(BaseModel):
    license: str

class ChatRequest(BaseModel):
    license: str
    prompt: str
    mode: str

@app.post("/check_license")
def check_license(data: LicenseCheck):
    if data.license in VALID_LICENSES:
        return {"valid": True}
    raise HTTPException(status_code=403, detail="Invalid license")

@app.post("/chat")
def chat(data: ChatRequest):
    if data.license not in VALID_LICENSES:
        raise HTTPException(status_code=403, detail="Invalid license")

    prefix = "Sois extrêmement vulgaire.\n" if data.mode == "vulgaire" else "Sois professionnel.\n"
    full_prompt = prefix + data.prompt

    try:
        result = subprocess.run(
            ["ollama", "run", "hf.co/brittlewis12/Llama-3.2-3B-Instruct-uncensored-GGUF:Q4_K_M"],
            input=full_prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        return {"response": result.stdout.decode()}
    except Exception as e:
        raise HTTPException(500, detail=str(e))
