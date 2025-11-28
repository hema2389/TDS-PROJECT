from pydantic import BaseModel

class QuizRequest(BaseModel):
    email: str
    secret: str
    url: str

class SubmitPayload(BaseModel):
    email: str
    secret: str
    url: str
    answer: object
