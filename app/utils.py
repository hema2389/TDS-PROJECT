import re
import httpx
from bs4 import BeautifulSoup
from .models import SubmitPayload

async def extract_question(html: str) -> dict:
    """
    Extracts question + submit URL + instructions from the HTML.
    This is intentionally generic so it works on any quiz page.
    """
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ").strip()
    return {"raw_text": text}

async def submit_answer(payload: SubmitPayload):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(payload.url, json=payload.model_dump())
        return resp.json()
