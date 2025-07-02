from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI()
API_KEY = os.getenv("OPENROUTER_API_KEY")

with open("license.txt") as f:
    VALID_LICENSES = set(line.strip() for line in f)

class LicenseCheck(BaseModel):
    license: str

class ChatRequest(BaseModel):
    license: str
    prompt: str
