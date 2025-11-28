import time
import re
import pandas as pd
from .fetcher import fetch_page
from .utils import extract_question
from .models import SubmitPayload
from .config import EMAIL, SECRET, TIME_LIMIT_SECONDS
from .utils import submit_answer

async def solve_quiz(initial_url: str):
    start = time.time()
    url = initial_url

    while True:
        if time.time() - start > TIME_LIMIT_SECONDS:
            return {"error": "Timeout exceeded"}

        html = await fetch_page(url)
        qdata = await extract_question(html)
        raw = qdata["raw_text"]

        # --- SIMPLE PATTERN SOLVER (extendable) ---
        answer = None

        if "sum" in raw.lower() and "value" in raw.lower():
            m = re.search(r'https[^ ]+\.csv', raw)
            if m:
                df = pd.read_csv(m.group(0))
                if "value" in df.columns:
                    answer = df["value"].sum()

        # Fallback
        if answer is None:
            answer = "UNABLE TO PARSE QUESTION"

        payload = SubmitPayload(
            email=EMAIL,
            secret=SECRET,
            url=url,
            answer=answer
        )

        result = await submit_answer(payload)

        if "correct" in result and not result.get("url"):
            return {"status": "quiz_completed", "final": result}

        if "url" in result:
            url = result["url"]
        else:
            return {"status": "terminated", "response": result}
