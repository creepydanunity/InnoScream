from pydantic import BaseModel
from typing import List
import logging

logger = logging.getLogger("app_fastapi.schemas")

class CreateScreamResponse(BaseModel):
    status: str
    scream_id: int

    def __repr__(self):
        logger.debug(f"CreateScreamResponse representation: status={self.status}, scream_id={self.scream_id}")
        return f"<CreateScreamResponse(status={self.status}, scream_id={self.scream_id})>"

class CreateAdminResponse(BaseModel):
    status: str

    def __repr__(self):
        logger.debug(f"CreateAdminResponse representation: status={self.status}")
        return f"<CreateAdminResponse(status={self.status})>"

class GetMyIdResponse(BaseModel):
    user_id: str

    def __repr__(self):
        logger.debug(f"GetMyIdResponse representation: user_id={self.user_id[:5]}...")
        return f"<GetMyIdResponse(user={self.user_id[:5]}...)>"

class ReactionResponse(BaseModel):
    status: str

    def __repr__(self):
        logger.debug(f"ReactionResponse representation: status={self.status}")
        return f"<ReactionResponse(status={self.status})>"

class TopScreamItem(BaseModel):
    id: int
    content: str
    votes: int
    meme_url: str

    def __repr__(self):
        logger.debug(f"TopScreamItem representation: id={self.id}, votes={self.votes}")
        return f"<TopScreamItem(id={self.id}, votes={self.votes})>"

class TopScreamsResponse(BaseModel):
    posts: List[TopScreamItem]

    def __repr__(self):
        logger.debug(f"TopScreamsResponse representation: posts_count={len(self.posts)}")
        return f"<TopScreamsResponse(posts={len(self.posts)})>"

class ArchivedWeeksResponse(BaseModel):
    weeks: List[int]

class UserStatsResponse(BaseModel):
    screams_posted: int
    reactions_given: int
    reactions_got: int
    chart_url: str
    reaction_chart_url: str

    def __repr__(self):
        logger.debug(f"UserStatsResponse representation: screams={self.screams_posted}, reactions={self.reactions_got}")
        return f"<UserStatsResponse(screams={self.screams_posted}, reactions={self.reactions_got})>"

class DeleteResponse(BaseModel):
    status: str

    def __repr__(self):
        logger.debug(f"DeleteResponse representation: status={self.status}")
        return f"<DeleteResponse(status={self.status})>"

class StressStatsResponse(BaseModel):
    chart_url: str

    def __repr__(self):
        logger.debug("StressStatsResponse representation")
        return "<StressStatsResponse>"

class ScreamResponse(BaseModel):
    scream_id: int
    content: str

    def __repr__(self):
        logger.debug(f"ScreamResponse representation: scream_id={self.scream_id}")
        return f"<ScreamResponse(scream_id={self.scream_id})>"