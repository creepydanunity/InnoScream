# Standard library
import logging

# Third‑party
from pydantic import BaseModel, constr
from typing_extensions import Annotated


logger = logging.getLogger("app_fastapi.schemas")

class CreateScreamRequest(BaseModel):

    """
    Request model for creating a new scream.

    Attributes:
        content (str): Text of the scream, limited to 1–280 characters.
        user_id (str): ID of the user creating the scream.
    """

    content: Annotated[str, constr(min_length=1, max_length=280)]
    user_id: str

    def __repr__(self):
        logger.debug(f"CreateScreamRequest representation: user_id={self.user_id[:5]}...")
        return f"<CreateScreamRequest(user={self.user_id[:5]}...)>"

class CreateAdminRequest(BaseModel):

    """
    Request model for promoting a user to admin.

    Attributes:
        user_id_to_admin (str): ID of the user to be granted admin rights.
        user_id (str): ID of the requester.
    """

    user_id_to_admin: str
    user_id: str

    def __repr__(self):
        logger.debug(f"CreateAdminRequest representation: user_id={self.user_id[:5]}..., to_admin={self.user_id_to_admin[:5]}...")
        return f"<CreateAdminRequest(from={self.user_id[:5]}..., to={self.user_id_to_admin[:5]}...)>"

class GetIdRequest(BaseModel):

    """
    Request model for retrieving the current user's ID.

    Attributes:
        user_id (str): ID of the user.
    """

    user_id: str

    def __repr__(self):
        logger.debug(f"GetIdRequest representation: user_id={self.user_id[:5]}...")
        return f"<GetIdRequest(user={self.user_id[:5]}...)>"

class ReactionRequest(BaseModel):

    """
    Request model for reacting to a scream.

    Attributes:
        scream_id (int): ID of the scream to react to.
        emoji (str): Emoji reaction.
        user_id (str): ID of the user reacting.
    """

    scream_id: int
    emoji: str
    user_id: str

    def __repr__(self):
        logger.debug(f"ReactionRequest representation: user_id={self.user_id[:5]}..., scream_id={self.scream_id}")
        return f"<ReactionRequest(user={self.user_id[:5]}..., scream={self.scream_id}, emoji={self.emoji})>"

class DeleteRequest(BaseModel):

    """
    Request model for deleting a scream.

    Attributes:
        scream_id (int): ID of the scream to delete.
        user_id (str): ID of the requester.
    """

    scream_id: int
    user_id: str

    def __repr__(self):
        logger.debug(f"DeleteRequest representation: user_id={self.user_id[:5]}..., scream_id={self.scream_id}")
        return f"<DeleteRequest(user={self.user_id[:5]}..., scream={self.scream_id})>"

class UserRequest(BaseModel):

    """
    Simple request model containing a user ID.

    Attributes:
        user_id (str): ID of the user.
    """

    user_id: str

    def __repr__(self):
        logger.debug(f"UserRequest representation: user_id={self.user_id[:5]}...")
        return f"<UserRequest(user={self.user_id[:5]}...)>"