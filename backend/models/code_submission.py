from pydantic import BaseModel

class CodeSubmission(BaseModel):
    language: str  # e.g., "python", "javascript"
    code: str
    user_id: str = "anonymous"
