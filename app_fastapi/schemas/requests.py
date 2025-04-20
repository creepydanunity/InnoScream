from pydantic import BaseModel, constr
from typing_extensions import Annotated


class CreateScreamRequest(BaseModel):
    content: Annotated[str, constr(min_length=1, max_length=280)]
    user_id: str


class ReactionRequest(BaseModel):
    scream_id: int
    emoji: str
    user_id: str
