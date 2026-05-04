from pydantic import BaseModel

class AnalyzeResponse(BaseModel):
    age: int
    gender: str
    confidence: float