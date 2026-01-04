from pydantic import BaseModel

class ScamRequest(BaseModel):
    message: str
    amount: int
    sender_type: str
