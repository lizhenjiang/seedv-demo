from pydantic import BaseModel
from typing import Optional, List

from app.schemas.apply import ApplyResponse


class ProcessResponse(BaseModel):
    id: int
    type: str
    status: str
    sequence: int
    result: Optional[str] = None

class ApplyDetailedResponse(ApplyResponse):
    processes: List[ProcessResponse]
