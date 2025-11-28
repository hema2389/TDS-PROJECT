import time
import re
import json
import httpx
import pandas as pd
from .browser import render_page
from .utils import extract_question, submit_answer
from .models import SubmitPayload
from .config import EMAIL, SECRET, TIME_LIMIT_SECONDS

async def solve_quiz(initial_url: str):
    """
    Main solver loop: Visit a URL → detect question → solve → submit → repeat.
    """
    start = time.time()
    url = initial_url

    while True:
        # Check timeout
        if time.time() - start > TIME_LIMIT_SECONDS:
            return {"error": "Timeout exceeded"}

        # Render page (JS executed)
        html = await render_page(url)
        qdata = await extract_question(html)
        raw = qdata["raw_text"]

        print("QUESTION DETECTED:")
        print(raw[:400], "...")

        # === YOUR LOGIC HERE ===
        # You must code flexible logic that detects the task dynamically.
        # For now we implement generic demo logic for:
        # "sum of value column on page X"
        answer = None

        # Example pattern
        if "sum" in raw.lower() and "value" in raw.lower():
            # detect downloadable link
            m = re.search(r'https[^ ]+\.csv', raw)
            if m:
                csv_url = m.group(0)
                df = pd.read_csv(csv_url)
                if "value" in df.columns:
                    answer = df["value"].sum()

        # Fallback (placeholder)
        if answer is None:
            answer = "Unable to parse question (placeholder)."

        # Submit result
        payload = SubmitPayload(
            email=EMAIL,
            secret=SECRET,
            url=url,
            answer=answer
        )

        result = await submit_answer(payload)
        print("SUBMISSION RESPONSE:", result)

        # End condition
        if "correct" in result and result.get("url") is None:
            return {"status": "quiz_completed", "final": result}

        # Next URL
        if "url" in result:
            url = result["url"]
        else:
            return {"status": "terminated", "response": result}
