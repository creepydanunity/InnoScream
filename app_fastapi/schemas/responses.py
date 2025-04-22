from pydantic import BaseModel
from typing import List


class CreateScreamResponse(BaseModel):
    status: str
    scream_id: int


class CreateAdminResponse(BaseModel):
    status: str


class GetMyIdResponse(BaseModel):
    user_id: str


class ReactionResponse(BaseModel):
    status: str


class TopScreamItem(BaseModel):
    id: int
    content: str
    votes: int
    meme_url: str


class TopScreamsResponse(BaseModel):
    posts: List[TopScreamItem]


class UserStatsResponse(BaseModel):
    screams_posted: int
    reactions_given: int
    reactions_got: int
    chart_url: str
    reaction_chart_url: str


class DeleteResponse(BaseModel):
    status: str


class StressStatsResponse(BaseModel):
    chart_url: str


class ScreamResponse(BaseModel):
    scream_id: int
    content: str