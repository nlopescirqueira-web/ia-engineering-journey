import os

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from agent import process_voice_command
from db import init_db, log_interaction

app = FastAPI(title="Voice Agent")

API_KEY = os.environ.get("AGENT_API_KEY")


class VoiceRequest(BaseModel):
    text: str


class VoiceResponse(BaseModel):
    action: str
    title: str | None = None
    due_date: str | None = None
    notes: str | None = None
    reply: str


@app.on_event("startup")
def on_startup() -> None:
    init_db()


def check_api_key(x_api_key: str | None) -> None:
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida")


@app.post("/voice", response_model=VoiceResponse)
def voice_endpoint(
    payload: VoiceRequest, x_api_key: str | None = Header(default=None)
) -> dict:
    check_api_key(x_api_key)

    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Texto vazio")

    result = process_voice_command(payload.text)

    log_interaction(
        input_text=payload.text,
        action=result["action"],
        title=result.get("title"),
        due_date=result.get("due_date"),
        notes=result.get("notes"),
        reply=result["reply"],
    )

    return result


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
