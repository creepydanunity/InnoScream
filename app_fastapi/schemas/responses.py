from pydantic import BaseModel
from typing import List
import logging

logger = logging.getLogger("app_fastapi.schemas")

class CreateScreamResponse(BaseModel):
    """
    Response model for scream creation endpoint.

    Attributes:
        status (str): Operation status, e.g., "ok".
        scream_id (int): ID of the newly created scream.

    Methods:
        __repr__(): Return a debug representation of the response.
    """
    status: str
    scream_id: int

    def __repr__(self):
        logger.debug(f"CreateScreamResponse representation: status={self.status}, scream_id={self.scream_id}")
        return f"<CreateScreamResponse(status={self.status}, scream_id={self.scream_id})>"

class CreateAdminResponse(BaseModel):
    """
    Response model for admin creation request.

    Attributes:
        status (str): Status of the operation ("ok", "already_admin").

    Methods:
        __repr__(): Return a debug representation of the response.
    """
    status: str

    def __repr__(self):
        logger.debug(f"CreateAdminResponse representation: status={self.status}")
        return f"<CreateAdminResponse(status={self.status})>"

class GetMyIdResponse(BaseModel):
    """
    Response model for retrieving the current user's ID.

    Attributes:
        user_id (str): The external user ID provided in the request.

    Methods:
        __repr__(): Return a debug representation of the response.
    """
    user_id: str

    def __repr__(self):
        logger.debug(f"GetMyIdResponse representation: user_id={self.user_id[:5]}...")
        return f"<GetMyIdResponse(user={self.user_id[:5]}...)>"

class ReactionResponse(BaseModel):
    """
    Response model for reaction endpoint.

    Attributes:
        status (str): Operation status, e.g., "ok".

    Methods:
        __repr__(): Return a debug representation of the response.
    """
    status: str

    def __repr__(self):
        logger.debug(f"ReactionResponse representation: status={self.status}")
        return f"<ReactionResponse(status={self.status})>"

class TopScreamItem(BaseModel):
    """
    Schema for a single top scream item in the top screams list.

    Attributes:
        id (int): Scream ID.
        content (str): Text content of the scream.
        votes (int): Number of positive reactions.
        meme_url (str): URL to the associated meme image.

    Methods:
        __repr__(): Return a debug representation of the item.
    """
    id: int
    content: str
    votes: int
    meme_url: str

    def __repr__(self):
        logger.debug(f"TopScreamItem representation: id={self.id}, votes={self.votes}")
        return f"<TopScreamItem(id={self.id}, votes={self.votes})>"

class TopScreamsResponse(BaseModel):
    """
    Response model for the top screams endpoint.

    Attributes:
        posts (List[TopScreamItem]): List of top scream items.

    Methods:
        __repr__(): Return a debug representation including post count.
    """
    posts: List[TopScreamItem]

    def __repr__(self):
        logger.debug(f"TopScreamsResponse representation: posts_count={len(self.posts)}")
        return f"<TopScreamsResponse(posts={len(self.posts)})>"

class ArchivedWeeksResponse(BaseModel):
    """
    Response model listing available archived weeks.

    Attributes:
        weeks (List[int]): Identifiers for archived weeks.
    """
    weeks: List[int]

class UserStatsResponse(BaseModel):
    """
    Response model for user statistics endpoint.

    Attributes:
        screams_posted (int): Total number of screams posted by the user.
        reactions_given (int): Total reactions the user has given.
        reactions_got (int): Total reactions received on the user's screams.
        chart_url (str): URL to a bar chart of daily screams over the past week.
        reaction_chart_url (str): URL to a pie chart of reaction distribution.

    Methods:
        __repr__(): Return a debug representation including counts.
    """
    screams_posted: int
    reactions_given: int
    reactions_got: int
    chart_url: str
    reaction_chart_url: str

    def __repr__(self):
        logger.debug(f"UserStatsResponse representation: screams={self.screams_posted}, reactions={self.reactions_got}")
        return f"<UserStatsResponse(screams={self.screams_posted}, reactions={self.reactions_got})>"

class DeleteResponse(BaseModel):
    """
    Response model returned after a scream deletion request.

    Attributes:
        status (str): Status of the operation ("deleted").

    Methods:
        __repr__(): Return a debug representation of the response.
    """
    status: str

    def __repr__(self):
        logger.debug(f"DeleteResponse representation: status={self.status}")
        return f"<DeleteResponse(status={self.status})>"

class StressStatsResponse(BaseModel):
    """
    Response model for weekly stress (scream count) statistics.

    Attributes:
        chart_url (str): URL to a bar chart of daily scream counts over the past week.

    Methods:
        __repr__(): Return a debug representation of the response.
    """
    chart_url: str

    def __repr__(self):
        logger.debug("StressStatsResponse representation")
        return "<StressStatsResponse>"

class ScreamResponse(BaseModel):
    """
    Response model for a single scream in the user's feed.

    Attributes:
        scream_id (int): ID of the scream.
        content (str): Text content of the scream.

    Methods:
        __repr__(): Return a debug representation of the response.
    """
    scream_id: int
    content: str

    def __repr__(self):
        logger.debug(f"ScreamResponse representation: scream_id={self.scream_id}")
        return f"<ScreamResponse(scream_id={self.scream_id})>"