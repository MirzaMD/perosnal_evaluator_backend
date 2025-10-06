from pydantic import BaseModel, Field
from typing import List
class ANSOBJ(BaseModel):
    q: str = Field(...)
    a: str = Field(...)

class MainSchema(BaseModel):
    info: List[ANSOBJ] = Field(...)
    personality_summary: str = Field(default="You have a delightful personality")