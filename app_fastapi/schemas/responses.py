# Standard library
import logging
from typing import List

# Third-party
from pydantic import BaseModel


logger = logging.getLogger("app_fastapi.schemas")


class CreateScreamResponse(BaseModel):
    """Response model for scream creation endpoint.

    Attributes:
        status: Operation status like "ok"
        scream_id: ID of newly created scream
    """

    status: str
    scream_id: int

    def __repr__(self):
        log_msg = (
            f"CreateScreamResponse representation: "
            f"status={self.status}, scream_id={self.scream_id}"
        )
        logger.debug(log_msg)
        return f"<CreateScreamResponse({self.status}, {self.scream_id})>"


class CreateAdminResponse(BaseModel):
    """Response model for admin creation request.

    Attributes:
        status: Operation status ("ok", "already_admin")
    """

    status: str

    def __repr__(self):
        logger.debug(f"CreateAdminResponse status={self.status}")
        return f"<CreateAdminResponse({self.status})>"


class GetMyIdResponse(BaseModel):
    """Response model for retrieving user ID.

    Attributes:
        user_id: External user ID from request
    """

    user_id: str

    def __repr__(self):
        logger.debug(f"GetMyIdResponse user={self.user_id[:5]}...")
        return f"<GetMyIdResponse({self.user_id[:5]}...)>"


class ReactionResponse(BaseModel):
    """Response model for reaction endpoint.

    Attributes:
        status: Operation status like "ok"
    """

    status: str

    def __repr__(self):
        logger.debug(f"ReactionResponse status={self.status}")
        return f"<ReactionResponse({self.status})>"


class TopScreamItem(BaseModel):
    """Schema for single top scream item.

    Attributes:
        id: Scream ID
        content: Text content
        votes: Number of positive reactions
        meme_url: URL to meme image
    """

    id: int
    content: str
    votes: int
    meme_url: str

    def __repr__(self):
        logger.debug(f"TopScreamItem id={self.id}, votes={self.votes}")
        return f"<TopScreamItem({self.id}, {self.votes})>"


class TopScreamsResponse(BaseModel):
    """Response model for top screams endpoint.

    Attributes:
        posts: List of top scream items
    """

    posts: List[TopScreamItem]

    def __repr__(self):
        logger.debug(f"TopScreamsResponse posts={len(self.posts)}")
        return f"<TopScreamsResponse({len(self.posts)} posts)>"


class ArchivedWeeksResponse(BaseModel):
    """Response model listing archived weeks.

    Attributes:
        weeks: Identifiers for archived weeks
    """

    weeks: List[int]


class UserStatsResponse(BaseModel):
    """Response model for user statistics.

    Attributes:
        screams_posted: Total user screams
        reactions_given: Reactions given by user
        reactions_got: Reactions received
        chart_url: Weekly screams chart URL
        reaction_chart_url: Reactions pie chart URL
    """

    screams_posted: int
    reactions_given: int
    reactions_got: int
    chart_url: str
    reaction_chart_url: str

    def __repr__(self):
        log_msg = (
            f"UserStatsResponse screams={self.screams_posted} "
            f"reactions={self.reactions_got}"
        )
        logger.debug(log_msg)
        return (
            f"<UserStatsResponse({self.screams_posted}, "
            f"{self.reactions_got})>"
        )


class DeleteResponse(BaseModel):
    """Response model for scream deletion.

    Attributes:
        status: Operation status ("deleted")
    """

    status: str

    def __repr__(self):
        logger.debug(f"DeleteResponse status={self.status}")
        return f"<DeleteResponse({self.status})>"


class StressStatsResponse(BaseModel):
    """Response model for weekly stress stats.

    Attributes:
        chart_url: Weekly scream counts chart URL
    """

    chart_url: str

    def __repr__(self):
        logger.debug("StressStatsResponse representation")
        return "<StressStatsResponse>"


class ScreamResponse(BaseModel):
    """Response model for single feed scream.

    Attributes:
        scream_id: Scream ID
        content: Text content
    """

    scream_id: int
    content: str

    def __repr__(self):
        logger.debug(f"ScreamResponse id={self.scream_id}")
        return f"<ScreamResponse({self.scream_id})>"
