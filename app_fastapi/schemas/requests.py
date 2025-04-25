from pydantic import BaseModel, constr
from typing_extensions import Annotated


class CreateScreamRequest(BaseModel):

    """
    Request model for creating a new scream.

    Attributes:
        content (str): Text of the scream, limited to 1–280 characters.
        user_id (str): ID of the user creating the scream.
    """

    content: Annotated[str, constr(min_length=1, max_length=280)]
    user_id: str


class CreateAdminRequest(BaseModel):

    """
    Request model for promoting a user to admin.

    Attributes:
        user_id_to_admin (str): ID of the user to be granted admin rights.
        user_id (str): ID of the requester.
    """

    user_id_to_admin: str
    user_id: str


class GetIdRequest(BaseModel):

    """
    Request model for retrieving the current user's ID.

    Attributes:
        user_id (str): ID of the user.
    """

    user_id: str


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


class DeleteRequest(BaseModel):

    """
    Request model for deleting a scream.

    Attributes:
        scream_id (int): ID of the scream to delete.
        user_id (str): ID of the requester.
    """

    scream_id: int
    user_id: str

class UserRequest(BaseModel):

    """
    Simple request model containing a user ID.

    Attributes:
        user_id (str): ID of the user.
    """

    user_id: str