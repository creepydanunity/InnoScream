# Standard library
import logging
from datetime import timedelta
from typing import List

# Third‑party
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import distinct, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

# Local application
from app_fastapi.initializers.engine import get_session
from app_fastapi.middlewares.admin import admin_middleware
from app_fastapi.models.admin import Admin
from app_fastapi.models.archive import Archive
from app_fastapi.models.reaction import Reaction
from app_fastapi.models.scream import Scream
from app_fastapi.schemas.requests import (
    CreateAdminRequest,
    CreateScreamRequest,
    DeleteRequest,
    GetIdRequest,
    ReactionRequest,
    UserRequest,
)
from app_fastapi.schemas.responses import (
    ArchivedWeeksResponse,
    CreateAdminResponse,
    CreateScreamResponse,
    DeleteResponse,
    GetMyIdResponse,
    ReactionResponse,
    ScreamResponse,
    StressStatsResponse,
    TopScreamItem,
    TopScreamsResponse,
    UserStatsResponse,
)
from app_fastapi.tools.crypt import hash_user_id
from app_fastapi.tools.meme import generate_meme_url
from app_fastapi.tools.time import get_bounds, get_week_start


router = APIRouter()
logger = logging.getLogger("app_fastapi")


@router.post("/scream", response_model=CreateScreamResponse)
async def create_scream(data: CreateScreamRequest,
                        session: AsyncSession = Depends(get_session)):
    """
    Create a new scream for a user.

    Args:
        data (CreateScreamRequest):
        Request containing the user's external ID and scream content.
        session (AsyncSession): Database session dependency.

    Returns:
        CreateScreamResponse: Status and generated scream ID on success.

    Raises:
        HTTPException: On internal server error.
    """
    try:
        logger.debug(f"Creating scream for user: {data.user_id[:5]}...")
        user_hash = hash_user_id(data.user_id)
        scream = Scream(content=data.content, user_hash=user_hash)
        session.add(scream)
        await session.commit()

        logger.info(f"Scream created successfully. ID: {scream.id}")
        return {"status": "ok", "scream_id": scream.id}
    except Exception as e:
        logger.error(f"Failed to create scream: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/react", response_model=ReactionResponse)
async def react(data: ReactionRequest,
                session: AsyncSession = Depends(get_session)):
    """
    Record a reaction to a specific scream by a user.

    Args:
        data (ReactionRequest):
        Request containing the scream ID, user's external ID, and emoji.
        session (AsyncSession): Database session dependency.

    Returns:
        ReactionResponse: Status "ok" on success.

    Raises:
        HTTPException:
        404 if scream not found,
        409 if user already reacted,
        500 on server error.
    """
    try:
        logger.debug(f"Processing reaction {data.emoji} "
                     f"for scream {data.scream_id} "
                     f"from user {data.user_id[:5]}...")

        scream = await session.get(Scream, data.scream_id)
        if not scream:
            logger.warning(f"Scream not found: {data.scream_id}")
            raise HTTPException(status_code=404, detail="Scream not found")

        user_hash = hash_user_id(data.user_id)
        exists = await session.scalar(
            select(Reaction).where(
                Reaction.scream_id == data.scream_id,
                Reaction.user_hash == user_hash
            )
        )
        if exists:
            logger.warning(f"User already reacted to scream {data.scream_id}")
            raise HTTPException(status_code=409, detail="Already reacted")
        reaction = Reaction(emoji=data.emoji,
                            scream_id=data.scream_id,
                            user_hash=user_hash)
        session.add(reaction)
        await session.commit()
        logger.info(f"Reaction {data.emoji} added to scream {data.scream_id}")
        return {"status": "ok"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to process reaction: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/top", response_model=TopScreamsResponse)
async def get_top_screams(n: int = 3,
                          session: AsyncSession = Depends(get_session)):
    """
    Retrieve the top N screams based on the number of positive reactions.

    Args:
        n (int, optional):
        The number of top screams to retrieve. Defaults to 3.
        session (AsyncSession, optional): Database session dependency.

    Returns:
        dict:
            A dictionary with a list of top screams,
            each containing the scream ID, content, vote count,
            and meme URL. If no screams are found, returns
            an empty list under "posts".

    Notes:
        - This endpoint returns a JSON response.
        - Meme URLs are generated asynchronously
            Saved back into the database.
    """
    try:
        logger.debug(f"Fetching top {n} screams")
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
            logger.info("No top screams found for today")
            return {"posts": []}

        posts = []
        for scream, votes in top_n:
            if not scream.meme_url:
                try:
                    meme_url = await generate_meme_url(scream.content)
                    scream.meme_url = meme_url
                    await session.execute(
                        update(Scream)
                        .where(Scream.id == scream.id)
                        .values(meme_url=meme_url)
                    )
                    await session.commit()
                    logger.debug(f"Generated meme for scream {scream.id}")
                except Exception as e:
                    logger.warning(f"Failed to generate meme for scream "
                                   f"{scream.id}: {str(e)}")
                    continue
            posts.append(
                TopScreamItem(
                    id=scream.id,
                    content=scream.content,
                    votes=votes,
                    meme_url=scream.meme_url
                )
            )

        logger.info(f"Returned {len(posts)} top screams")
        return {"posts": posts}
    except Exception as e:
        logger.error(f"Failed to get top screams: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stats/{user_id}", response_model=UserStatsResponse)
async def get_user_stats(user_id: str,
                         session: AsyncSession = Depends(get_session)):
    """
    Get user stats.

    Retrieve statistics for a specific user,
    including post and reaction counts and activity charts.

    This function:
    - Hashes the `user_id` to match internal database storage.
    - Computes the number of posts made each day in the last 7 days.
    - Generates a QuickChart URL for a bar chart of daily posts.
    - Computes total number of screams reactions given, and reactions received.
    - Generates a QuickChart URL for a pie chart of received reactions.

    Args:
        user_id (str): The external user ID (to be hashed internally).
        session (AsyncSession, optional): Database session dependency.

    Returns:
        dict: A dictionary containing:
            - screams_posted (int): Total number of
                screams posted by the user.
            - reactions_given (int): Total number of
                reactions the user has given.
            - reactions_got (int): Total number of
                reactions received on the user's screams.
            - chart_url (str): URL to a bar chart
                showing daily post counts over the week.
            - reaction_chart_url (str): URL to a
                pie chart showing distribution of reaction emojis.
    """
    import urllib.parse
    from datetime import datetime, timezone, timedelta

    user_hash = hash_user_id(user_id)
    today = datetime.now(timezone.utc).replace(hour=0, minute=0,
                                               second=0, microsecond=0)
    week_ago = today - timedelta(days=6)
    try:
        logger.debug(f"Getting stats for user: {user_id[:5]}...")
        user_hash = hash_user_id(user_id)
        _, week_ago = get_bounds(days=6, addition=False)

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

        labels = [(week_ago + timedelta(days=i)).strftime(
            '%a'
            ) for i in range(7)]
        chart_url = urllib.parse.quote(
            f"https://quickchart.io/chart?c="
            f"{{type:'bar',data:{{labels:{labels},"
            f"datasets:[{{label:'Screams',data:{daily_counts}}}]}}}}",
            safe=':/?=&'
        )
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
        if emoji_data:
            labels = [emoji for emoji, _ in emoji_data]
            values = [count for _, count in emoji_data]
        else:
            labels = ["No reactions"]
            values = [1]

        chart = (
            f"https://quickchart.io/chart?c="
            f"{{type:'pie',data:{{labels:{labels},"
            f"datasets:[{{data:{values}}}]}}}}"
        )
        reaction_chart_url = urllib.parse.quote(chart, safe=':/?=&')

        logger.info(f"Successfully retrieved stats for user: {user_id[:5]}...")
        return {
            "screams_posted": total_posts,
            "reactions_given": total_reactions_given,
            "reactions_got": total_reactions_got,
            "chart_url": chart_url,
            "reaction_chart_url": reaction_chart_url
        }
    except Exception as e:
        logger.error(f"Failed to get user stats: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stress", response_model=StressStatsResponse)
async def get_weekly_stress_graph_all(
    session: AsyncSession = Depends(get_session)
):
    """
    Generate a weekly stress graph showing the number of screams.

    Uses quickchart.io API for graph generation.

    Args:
        session (AsyncSession, optional): Database session dependency.

    Returns:
        dict: A dictionary containing:
            - chart_url (str): A URL to a bar chart visualizing
            The daily scream counts over the past 7 days.

    Behavior:
        - Counts all screams posted in the last 7 days (UTC time).
        - Aggregates the daily totals.
        - Creates a bar chart using QuickChart.io and returns the chart URL.
    """
    import urllib.parse
    from datetime import datetime, timezone, timedelta

    today = datetime.now(timezone.utc).replace(hour=0, minute=0,
                                               second=0, microsecond=0)
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

    chart_url = urllib.parse.quote(f"https://quickchart.io/chart?c="
                                   f"{{type:'bar',data:{{labels:{labels},"
                                   f"datasets:[{{label:'Screams',"
                                   f"data:{daily_counts}}}]}}}}",
                                   safe=':/?=&')
    return {"chart_url": chart_url}


@router.post("/create_admin", response_model=CreateAdminResponse)
async def create_admin(
    data: CreateAdminRequest,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(admin_middleware)
):
    """
    Assign admin privileges to a specified user.

    This endpoint can only be accessed by an existing admin
    (validated via middleware).
    If the specified user is already an admin, returns status "already_admin".
    Otherwise, adds the user to the admin table and returns status "ok".

    Args:
        data (CreateAdminRequest):
        Contains the ID of the requester and ID of the user to be promoted.
        session (AsyncSession): Database session, injected via dependency.
        _ (None): Result of admin_middleware; ensures the requester is admin.

    Returns:
        CreateAdminResponse:
        A response object with status "ok" or "already_admin".
    """
    user_to_admin_hash = hash_user_id(data.user_id_to_admin)

    result = await session.execute(select(Admin).where(
        Admin.user_hash == user_to_admin_hash
        ))
    existing_admin = result.scalar_one_or_none()
    if existing_admin:
        logger.warning(f"User already admin: {data.user_id_to_admin[:5]}...")
        return {"status": "already_admin"}

    admin = Admin(user_hash=user_to_admin_hash)
    session.add(admin)
    await session.commit()
    logger.info(f"Successfully created admin: {data.user_id_to_admin[:5]}...")
    return {"status": "ok"}


@router.post("/delete", response_model=DeleteResponse,
             dependencies=[Depends(admin_middleware)])
async def delete_scream(
    data: DeleteRequest,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(admin_middleware)
):
    """
    Delete a scream by its ID.

    This endpoint can only be accessed by users with admin privileges,
    which are verified by the `admin_middleware`. If the scream with the
    specified ID does not exist, a 404 error is returned.

    Args:
        data (DeleteRequest): Contains the ID of the scream to be deleted and
            the user ID of the requester.
        session (AsyncSession):
            Database session provided via dependency injection.
        _ (None): Result of admin_middleware; ensures the requester is admin.

    Returns:
        DeleteResponse: A response object with status "deleted".
    """
    try:
        logger.info(f"Deleting scream: {data.scream_id}")

        scream = await session.get(Scream, data.scream_id)

        if not scream:
            logger.warning(f"Scream not found: {data.scream_id}")
            raise HTTPException(status_code=404, detail="Scream not found")

        await session.delete(scream)
        await session.commit()

        logger.info(f"Successfully deleted scream: {data.scream_id}")
        return {"status": "deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete scream: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/my_id", response_model=GetMyIdResponse)
async def get_my_id(data: GetIdRequest):
    """
    Retrieve the user ID.

    This endpoint simply echoes back the user ID sent by the client.

    Args:
        data (GetIdRequest): Contains the user ID to return.

    Returns:
        GetMyIdResponse: A response object with the provided user ID.
    """
    user_id = data.user_id

    try:
        logger.debug(f"Getting user ID for: {data.user_id[:5]}...")

        if not user_id:
            logger.warning("Missing user_id in request")
            raise HTTPException(status_code=400, detail="Missing user_id")

        logger.info(f"Returned user ID: {data.user_id[:5]}...")
        return {"user_id": data.user_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user ID: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/feed/{user_id}", response_model=ScreamResponse)
async def get_next_scream(user_id: str,
                          session: AsyncSession = Depends(get_session)):
    """
    Retrieve user feed.

    Retrieve the next unseen scream for a given user
    from the current week's feed.

    Args:
        user_id (str): The external user ID used to determine reaction history.
        session (AsyncSession, optional): Database session dependency.

    Returns:
        dict: A dictionary containing:
            - scream_id (str): The ID of the next scream.
            - content (str): The content of the scream.

    Behavior:
        - Hashes the `user_id` to compare against stored data.
        - Retrieves the next scream
        from this week that the user has not reacted to.
        - Excludes the user's own screams.
    """
    from app_fastapi.models.scream import Scream
    from app_fastapi.models.reaction import Reaction

    try:
        logger.debug(f"Getting next scream for user: {user_id[:5]}...")
        user_hash = hash_user_id(user_id)

        stmt = (
            select(Scream)
            .outerjoin(Reaction, (Reaction.scream_id == Scream.id) &
                       (Reaction.user_hash == user_hash))
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
            logger.info(f"No more screams for user: {user_id[:5]}...")
            raise HTTPException(status_code=404, detail="No more screams")

        logger.info(f"Returned scream {scream.id} for user: {user_id[:5]}...")
        return {
            "scream_id": scream.id,
            "content": scream.content
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get next scream: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/screams/admin", response_model=List[ScreamResponse],
             dependencies=[Depends(admin_middleware)])
async def get_screams_admin(
    data: UserRequest,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(admin_middleware)
):
    """
    Retrieve all unmoderated screams for admin review.

    Args:
        data (UserRequest): Request data containing the admin's user ID.
        session (AsyncSession): Database session dependency.
        _ (None): Middleware dependency ensuring the user is an admin.

    Behavior:
        - Fetches all screams from the current week
        that haven't been moderated.
        - Returns a list of scream IDs and content.
    """
    try:
        logger.info(f"Getting screams for admin: {data.user_id[:5]}...")
        stmt = (
            select(Scream)
            .where(
                Scream.timestamp >= get_week_start(),
                Scream.moderated.is_(False)
            )
            .order_by(Scream.timestamp.asc())
        )

        result = await session.execute(stmt)
        screams = result.scalars().all()

        if not screams:
            logger.info("No unmoderated screams found")
            raise HTTPException(status_code=404, detail="No screams found")

        logger.info(f"Returned {len(screams)} screams for admin")
        return [
            {
                "scream_id": scream.id,
                "content": scream.content
            }
            for scream in screams
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get screams for admin: "
                     f"{str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error!")


@router.post("/confirm", dependencies=[Depends(admin_middleware)])
async def confirm_scream(
    data: DeleteRequest,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(admin_middleware)
):
    """
    Confirm a scream as reviewed.

    Args:
        data (DeleteRequest): Contains the scream ID to confirm.
        session (AsyncSession): Database session dependency.
        _ (None): Middleware dependency ensuring the user is an admin.

    Behavior:
        - Marks the scream as moderated in the database.
        - Returns a confirmation status.
    """
    try:
        logger.info(f"Confirming scream: {data.scream_id}")
        scream = await session.get(Scream, data.scream_id)

        if not scream:
            logger.warning(f"Scream not found: {data.scream_id}")
            raise HTTPException(status_code=404, detail="Scream not found")

        scream.moderated = True
        await session.commit()
        logger.info(f"Successfully confirmed scream: {data.scream_id}")
        return {"status": "confirmed"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to confirm scream: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/history", response_model=ArchivedWeeksResponse)
async def get_history(session: AsyncSession = Depends(get_session)):
    """
    Retrieve all archived week identifiers.

    Args:
        session (AsyncSession): Database session dependency.

    Behavior:
        - Queries the database for distinct archived week IDs.
        - Returns them in descending order.
    """
    try:
        stmt = select(distinct(Archive.week_id)).order_by(
            Archive.week_id.desc()
            )
        result = await session.execute(stmt)
        weeks = result.scalars().all()

        return {
            "weeks": weeks
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to load archives: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/history/{week_id}", response_model=TopScreamsResponse)
async def get_historical_week(week_id: str,
                              session: AsyncSession = Depends(get_session)):
    """
    Retrieve archived screams for a specific week.

    Args:
        week_id (str): The week identifier to retrieve data for.
        session (AsyncSession): Database session dependency.

    Behavior:
        - Fetches archived screams for the given week ID.
        - Returns scream content, vote count, and meme URL.
    """
    try:
        logger.info(f"Getting historical week: {week_id}")
        stmt = select(Archive).where(Archive.week_id == week_id).order_by(
            Archive.votes.desc()
            )
        result = await session.execute(stmt)
        archives = result.scalars().all()

        if not archives:
            logger.warning(f"Archive not found for week: {week_id}")
            raise HTTPException(status_code=404,
                                detail="Week not found in archive")

        posts = [
            TopScreamItem(
                id=arc.scream_id,
                content=arc.content,
                votes=arc.votes,
                meme_url=arc.meme_url
            )
            for arc in archives
        ]

        logger.info(f"Returned {len(posts)} screams for week {week_id}")
        return {"posts": posts}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get historical week: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/history/{week_id}", dependencies=[Depends(admin_middleware)])
async def archive_current_week(
    week_id: str,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(admin_middleware)
):
    """
    Archive the top screams of the current week under a given ID.

    Args:
        week_id (str): The archive label (e.g., "2025-W18").
        session (AsyncSession): Database session dependency.
        _ (None): Middleware dependency ensuring the user is an admin.

    Behavior:
        - Validates the archive does not already exist.
        - Calculates top-voted screams of the current week.
        - Stores them in the archive table.
    """
    try:
        logger.info(f"Archiving week as {week_id}")
        existing = await session.scalar(select(Archive).where(
            Archive.week_id == week_id).limit(1)
            )
        if existing:
            logger.warning(f"Week {week_id} already archived")
            raise HTTPException(status_code=409, detail="Week already exists")

        week_start = get_week_start()
        week_end = week_start + timedelta(days=7)

        stmt = (
            select(Scream, func.count(Reaction.id).label("votes"))
            .join(Reaction, Scream.id == Reaction.scream_id)
            .where(
                Scream.timestamp >= week_start,
                Scream.timestamp < week_end,
                Reaction.emoji != "❌"
            )
            .group_by(Scream.id)
            .order_by(func.count(Reaction.id).desc())
        )

        result = await session.execute(stmt)
        top_screams = result.all()

        for scream, votes in top_screams:
            archive = Archive(
                week_id=week_id,
                scream_id=scream.id,
                content=scream.content,
                meme_url=scream.meme_url,
                votes=votes
            )
            session.add(archive)
        await session.commit()
        logger.info(f"Week {week_id} archived with {len(top_screams)} screams")
        return {"status": "archived", "count": len(top_screams)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to archive week: {str(e)}", exc_info=True)
        await session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
