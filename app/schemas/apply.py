from pydantic import BaseModel
from typing import List

class ApplyRequest(BaseModel):
    command: str
    prompt: str

class ApplyResponse(BaseModel):
    id: int
    command: str
    status: str