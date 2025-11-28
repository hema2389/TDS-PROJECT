from fastapi import FastAPI, HTTPException
from .models import QuizRequest
from .config import SECRET
from .solver import solve_quiz

app = FastAPI()

@app.post("/")
async def root(req: QuizRequest):
    # Invalid JSON automatically handled
    if req.secret != SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")

    result = await solve_quiz(req.url)
    return result
