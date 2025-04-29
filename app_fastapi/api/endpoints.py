from typing import List
from datetime import timedelta

from app_fastapi.tools.meme import generate_meme_url
from app_fastapi.tools.time import get_bounds, get_week_start
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func, select, update
from app_fastapi.initializers.engine import get_session
from app_fastapi.tools.crypt import hash_user_id
from app_fastapi.models.scream import Scream
from app_fastapi.models.reaction import Reaction
from app_fastapi.models.admin import Admin
from sqlalchemy.ext.asyncio import AsyncSession
from app_fastapi.schemas.responses import (
    CreateScreamResponse,
    ReactionResponse,
    StressStatsResponse,
    TopScreamItem,
    TopScreamsResponse,
    UserStatsResponse,
    DeleteResponse,
    ScreamResponse,
    CreateAdminResponse,
    GetMyIdResponse
)
from app_fastapi.schemas.requests import (
    CreateScreamRequest,
    ReactionRequest,
    DeleteRequest,
    UserRequest,
    CreateAdminRequest,
    GetIdRequest
)
from app_fastapi.middlewares.admin import admin_middleware
import logging


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/scream", response_model=CreateScreamResponse)
async def create_scream(data: CreateScreamRequest, session: AsyncSession = Depends(get_session)):
    user_hash = hash_user_id(data.user_id)
    scream = Scream(content=data.content, user_hash=user_hash)
    session.add(scream)
    await session.commit()
    return {"status": "ok", "scream_id": scream.id}


@router.post("/react", response_model=ReactionResponse)
async def react(data: ReactionRequest, session: AsyncSession = Depends(get_session)):
    scream = await session.get(Scream, data.scream_id)
    if not scream:
        raise HTTPException(status_code=404, detail="Scream not found")

    user_hash = hash_user_id(data.user_id)
    exists = await session.scalar(
        select(Reaction).where(
            Reaction.scream_id == data.scream_id,
            Reaction.user_hash == user_hash
        )
    )
    if exists:
        raise HTTPException(status_code=409, detail="Already reacted")
    
    reaction = Reaction(emoji=data.emoji, scream_id=data.scream_id, user_hash=user_hash)
    session.add(reaction)
    await session.commit()
    return {"status": "ok"}


@router.get("/top", response_model=TopScreamsResponse)
async def get_top_screams(n: int = 3, session: AsyncSession = Depends(get_session)):
    """
    Retrieve the top N screams based on the number of positive reactions.

    Args:
        n (int, optional): The number of top screams to retrieve. Defaults to 3.
        session (AsyncSession, optional): Database session dependency.

    Returns:
        dict: A dictionary with a list of top screams, each containing the scream ID,
              content, vote count, and meme URL. If no screams are found, returns an
              empty list under "posts".

    Notes:
        - This endpoint returns a JSON response.
        - Meme URLs are generated asynchronously and saved back into the database.
    """

    today_start, tomorrow = get_bounds()

    stmt = (
        select(Scream, func.count(Reaction.id).label("votes"))
        .join(Reaction, Scream.id == Reaction.scream_id)
        .where(
            Scream.timestamp >= today_start, 
            Scream.timestamp < tomorrow,
            Reaction.emoji != "❌"
            )
        .group_by(Scream.id)
        .order_by(func.count(Reaction.id).desc())
        .limit(n)
    )

    result = await session.execute(stmt)
    top_n = result.all()

    if not top_n:
        return {"posts": []}

    posts = []
    for scream, votes in top_n:
        if not scream.meme_url:
            try:
                meme_url = await generate_meme_url(scream.content)
            except HTTPException as e:
                #logger.warning(f"Failed to generate meme for scream {scream.id}: {e.detail}")
                continue
            scream.meme_url = meme_url
            await session.execute(
                update(Scream)
                .where(Scream.id == scream.id)
                .values(meme_url=meme_url)
            )
            await session.commit()
        posts.append(
            TopScreamItem(
                id=scream.id,
                content=scream.content,
                votes=votes,
                meme_url=scream.meme_url
            )
        )

    return {"posts": posts}



@router.get("/stats/{user_id}", response_model=UserStatsResponse)
async def get_user_stats(user_id: str, session: AsyncSession = Depends(get_session)):
    """
    Retrieve statistics for a specific user, including post and reaction counts and activity charts.

    Args:
        user_id (str): The external user ID (to be hashed internally).
        session (AsyncSession, optional): Database session dependency.

    Returns:
        dict: A dictionary containing:
            - screams_posted (int): Total number of screams posted by the user.
            - reactions_given (int): Total number of reactions the user has given.
            - reactions_got (int): Total number of reactions received on the user's screams.
            - chart_url (str): URL to a bar chart showing daily post counts over the past 7 days.
            - reaction_chart_url (str): URL to a pie chart showing distribution of received reaction emojis.

    Behavior:
        - Hashes the `user_id` to match internal database storage.
        - Computes the number of posts made each day in the last 7 days.
        - Generates a QuickChart URL for a bar chart of daily posts.
        - Computes total number of screams, reactions given, and reactions received.
        - Generates a QuickChart URL for a pie chart of received reactions.
    """

    import urllib.parse
    from datetime import datetime, timezone, timedelta

    user_hash = hash_user_id(user_id)
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=6)

    daily_counts = [0] * 7
    stmt = (
        select(Scream.timestamp)
        .where(Scream.user_hash == user_hash, Scream.timestamp >= week_ago)
    )
    result = await session.execute(stmt)
    timestamps = result.scalars().all()

    for ts in timestamps:
        ts = ts.astimezone(timezone.utc)
        index = (ts.date() - week_ago.date()).days
        if 0 <= index < 7:
            daily_counts[index] += 1

    labels = [(week_ago + timedelta(days=i)).strftime('%a') for i in range(7)]
    chart_url = urllib.parse.quote(f"https://quickchart.io/chart?c={{type:'bar',data:{{labels:{labels},datasets:[{{label:'Screams',data:{daily_counts}}}]}}}}", safe=':/?=&')
    
    total_posts = await session.scalar(
        select(func.count(Scream.id)).where(Scream.user_hash == user_hash)
    )
    total_reactions_given = await session.scalar(
        select(func.count(Reaction.id)).where(
            Reaction.user_hash == user_hash,
            Reaction.emoji != "❌"
        )
    )
    total_reactions_got = await session.scalar(
        select(func.count(Reaction.id))
        .join(Scream, Scream.id == Reaction.scream_id)
        .where(
            Scream.user_hash == user_hash,
            Reaction.emoji != "❌"
        )
    )
    reaction_counts = await session.execute(
        select(Reaction.emoji, func.count())
        .join(Scream, Scream.id == Reaction.scream_id)
        .where(
            Scream.user_hash == user_hash,
            Reaction.emoji != "❌"
        )
        .group_by(Reaction.emoji)
    )
    emoji_data = reaction_counts.all()
    
    reaction_chart_url = None
    if emoji_data:
        labels = [emoji for emoji, _ in emoji_data]
        values = [count for _, count in emoji_data]
    else:
        labels = ["No reactions"]
        values = [1]

    chart = f"https://quickchart.io/chart?c={{type:'pie',data:{{labels:{labels},datasets:[{{data:{values}}}]}}}}"
    reaction_chart_url = urllib.parse.quote(chart, safe=':/?=&')

    return {
        "screams_posted": total_posts,
        "reactions_given": total_reactions_given,
        "reactions_got": total_reactions_got,
        "chart_url": chart_url,
        "reaction_chart_url": reaction_chart_url
    }


@router.get("/stress", response_model=StressStatsResponse)
async def get_weekly_stress_graph_all(session: AsyncSession = Depends(get_session)):
    import urllib.parse
    from datetime import datetime, timezone, timedelta

    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=6)

    daily_counts = [0] * 7
    stmt = select(Scream.timestamp).where(Scream.timestamp >= week_ago)

    result = await session.execute(stmt)
    timestamps = result.scalars().all()

    for ts in timestamps:
        ts = ts.astimezone(timezone.utc)
        index = (ts.date() - week_ago.date()).days
        if 0 <= index < 7:
            daily_counts[index] += 1

    labels = [(week_ago + timedelta(days=i)).strftime('%a') for i in range(7)]

    chart_url = urllib.parse.quote(f"https://quickchart.io/chart?c={{type:'bar',data:{{labels:{labels},datasets:[{{label:'Screams',data:{daily_counts}}}]}}}}", safe=':/?=&')

    
    return {"chart_url": chart_url}


@router.post("/create_admin", response_model=CreateAdminResponse)
async def create_admin(
    data: CreateAdminRequest,
    session: AsyncSession = Depends(get_session),  
    _: None = Depends(admin_middleware)
):

    """
    Assigns admin privileges to a specified user.

    This endpoint can only be accessed by an existing admin (validated via middleware).
    If the specified user is already an admin, returns status "already_admin".
    Otherwise, adds the user to the admin table and returns status "ok".

    Args:
        data (CreateAdminRequest): Contains the ID of the requester and ID of the user to be promoted.
        session (AsyncSession): Database session, injected via dependency.
        _ (None): Result of admin_middleware; ensures the requester is admin.

    Returns:
        CreateAdminResponse: A response object with status "ok" or "already_admin".
    """

    user_to_admin_hash = hash_user_id(data.user_id_to_admin)

    result = await session.execute(select(Admin).where(Admin.user_hash == user_to_admin_hash))
    existing_admin = result.scalar_one_or_none()
    if existing_admin:
        return {"status": "already_admin"}

    admin = Admin(user_hash=user_to_admin_hash)
    session.add(admin)
    await session.commit()

    return {"status": "ok"}


@router.post("/delete", response_model=DeleteResponse, dependencies=[Depends(admin_middleware)])
async def delete_scream(
    data: DeleteRequest, 
    session: AsyncSession = Depends(get_session),  
    _: None = Depends(admin_middleware)
):

    """
    Deletes a scream by its ID. 

    This endpoint can only be accessed by users with admin privileges, 
    which are verified by the `admin_middleware`. If the scream with the 
    specified ID does not exist, a 404 error is returned.

    Args:
        data (DeleteRequest): Contains the ID of the scream to be deleted and 
            the user ID of the requester.
        session (AsyncSession): Database session provided via dependency injection.
        _ (None): Result of admin_middleware; ensures the requester is admin.

    Returns:
        DeleteResponse: A response object with status "deleted".
    """

    scream = await session.get(Scream, data.scream_id)

    if not scream:
        raise HTTPException(status_code=404, detail="Scream not found")

    await session.delete(scream)
    await session.commit()
    return {"status": "deleted"}


@router.post("/my_id", response_model=GetMyIdResponse)
async def get_my_id(data: GetIdRequest):

    """
    Returns the user ID.

    This endpoint simply echoes back the user ID sent by the client. 

    Args:
        data (GetIdRequest): Contains the user ID to return.

    Returns:
        GetMyIdResponse: A response object with the provided user ID.
    """

    user_id = data.user_id

    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id")

    return {"user_id": user_id}


@router.get("/feed/{user_id}", response_model=ScreamResponse)
async def get_next_scream(user_id: str, session: AsyncSession = Depends(get_session)):
    from app_fastapi.models.scream import Scream
    from app_fastapi.models.reaction import Reaction

    user_hash = hash_user_id(user_id)
    
    stmt = (
        select(Scream)
        .outerjoin(Reaction, (Reaction.scream_id == Scream.id) & (Reaction.user_hash == user_hash))
        .where(
            Scream.user_hash != user_hash,
            Reaction.id.is_(None),
            Scream.timestamp >= get_week_start()
        )
        .order_by(Scream.timestamp.asc())
        .limit(1)
    )

    result = await session.execute(stmt)
    scream = result.scalar_one_or_none()

    if not scream:
        raise HTTPException(status_code=404, detail="No more screams")

    return {
        "scream_id": scream.id,
        "content": scream.content
    }

@router.post("/screams/admin", response_model=List[ScreamResponse], dependencies=[Depends(admin_middleware)])
async def get_screams_admin(data: UserRequest, session: AsyncSession = Depends(get_session),  _: None = Depends(admin_middleware)):
    from app_fastapi.models.scream import Scream
    
    stmt = (
        select(Scream)
        .where(
            Scream.timestamp >= get_week_start(), 
            Scream.moderated == False
        )
        .order_by(Scream.timestamp.asc())
    )

    result = await session.execute(stmt)
    screams = result.scalars().all()

    if not screams:
        raise HTTPException(status_code=404, detail="No screams found")

    return [
        {
            "scream_id": scream.id,
            "content": scream.content
        }
        for scream in screams
    ]

@router.post("/confirm", dependencies=[Depends(admin_middleware)])
async def confirm_scream(data: DeleteRequest, session: AsyncSession = Depends(get_session),  _: None = Depends(admin_middleware)):
    scream = await session.get(Scream, data.scream_id)

    if not scream:
        raise HTTPException(status_code=404, detail="Scream not found")

    scream.moderated = True
    await session.commit()
    return {"status": "confirmed"}