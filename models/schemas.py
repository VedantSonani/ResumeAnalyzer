from pydantic import BaseModel, Field

class Prompt(BaseModel):
    msg : str = Field(..., min_length=1)