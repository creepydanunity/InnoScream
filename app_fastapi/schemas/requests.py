from pydantic import BaseModel, constr
from typing_extensions import Annotated
import logging

logger = logging.getLogger("app_fastapi.schemas")

class CreateScreamRequest(BaseModel):
    content: Annotated[str, constr(min_length=1, max_length=280)]
    user_id: str

    def __repr__(self):
        logger.debug(f"CreateScreamRequest representation: user_id={self.user_id[:5]}...")
        return f"<CreateScreamRequest(user={self.user_id[:5]}...)>"

class CreateAdminRequest(BaseModel):
    user_id_to_admin: str
    user_id: str

    def __repr__(self):
        logger.debug(f"CreateAdminRequest representation: user_id={self.user_id[:5]}..., to_admin={self.user_id_to_admin[:5]}...")
        return f"<CreateAdminRequest(from={self.user_id[:5]}..., to={self.user_id_to_admin[:5]}...)>"

class GetIdRequest(BaseModel):
    user_id: str

    def __repr__(self):
        logger.debug(f"GetIdRequest representation: user_id={self.user_id[:5]}...")
        return f"<GetIdRequest(user={self.user_id[:5]}...)>"

class ReactionRequest(BaseModel):
    scream_id: int
    emoji: str
    user_id: str

    def __repr__(self):
        logger.debug(f"ReactionRequest representation: user_id={self.user_id[:5]}..., scream_id={self.scream_id}")
        return f"<ReactionRequest(user={self.user_id[:5]}..., scream={self.scream_id}, emoji={self.emoji})>"

class DeleteRequest(BaseModel):
    scream_id: int
    user_id: str

    def __repr__(self):
        logger.debug(f"DeleteRequest representation: user_id={self.user_id[:5]}..., scream_id={self.scream_id}")
        return f"<DeleteRequest(user={self.user_id[:5]}..., scream={self.scream_id})>"

class UserRequest(BaseModel):
    user_id: str

    def __repr__(self):
        logger.debug(f"UserRequest representation: user_id={self.user_id[:5]}...")
        return f"<UserRequest(user={self.user_id[:5]}...)>"