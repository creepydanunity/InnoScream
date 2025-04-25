from pydantic import BaseModel
from typing import List


class CreateScreamResponse(BaseModel):
    status: str
    scream_id: int


class CreateAdminResponse(BaseModel):

    """
    Response model for admin creation request.

    Attributes:
        status (str): Status of the operation ("ok", "already_admin").
    """

    status: str


class GetMyIdResponse(BaseModel):

    """
    Response model for returning the current user's ID.

    Attributes:
        user_id (str): ID of the user.
    """

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

    """
    Response model returned after a scream is deleted.

    Attributes:
        status (str): Status of the operation ("deleted").
    """

    status: str


class StressStatsResponse(BaseModel):
    chart_url: str


class ScreamResponse(BaseModel):
    scream_id: int
    content: str