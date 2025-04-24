from typing import List
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
import logging
import urllib.parse

from app_fastapi.tools.meme import generate_meme_url
from app_fastapi.tools.time import get_bounds, get_week_start
from app_fastapi.initializers.engine import get_session
from app_fastapi.tools.crypt import hash_user_id
from app_fastapi.models.scream import Scream
from app_fastapi.models.reaction import Reaction
from app_fastapi.models.admin import Admin
from app_fastapi.middlewares.admin import admin_middleware
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

router = APIRouter()
logger = logging.getLogger("app_fastapi")

@router.post("/scream", response_model=CreateScreamResponse)
async def create_scream(data: CreateScreamRequest, session: AsyncSession = Depends(get_session)):
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
async def react(data: ReactionRequest, session: AsyncSession = Depends(get_session)):
    try:
        logger.debug(f"Processing reaction {data.emoji} for scream {data.scream_id} from user {data.user_id[:5]}...")
        
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
        
        reaction = Reaction(emoji=data.emoji, scream_id=data.scream_id, user_hash=user_hash)
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
async def get_top_screams(n: int = 3, session: AsyncSession = Depends(get_session)):
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
                    meme_url = await generate_meme_url(scream.user_hash[:5], scream.content)
                    scream.meme_url = meme_url
                    await session.execute(
                        update(Scream)
                        .where(Scream.id == scream.id)
                        .values(meme_url=meme_url)
                    )
                    await session.commit()
                    logger.debug(f"Generated meme for scream {scream.id}")
                except Exception as e:
                    logger.warning(f"Failed to generate meme for scream {scream.id}: {str(e)}")
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
async def get_user_stats(user_id: str, session: AsyncSession = Depends(get_session)):
    try:
        logger.debug(f"Getting stats for user: {user_id[:5]}...")
        user_hash = hash_user_id(user_id)
        _, week_ago = get_bounds(days=6, addition=False)

        # Get daily scream counts
        daily_counts = [0] * 7
        stmt = (
            select(Scream.timestamp)
            .where(Scream.user_hash == user_hash, Scream.timestamp >= week_ago)
        )
        result = await session.execute(stmt)
        timestamps = result.scalars().all()

        for ts in timestamps:
            index = (ts.date() - week_ago.date()).days
            if 0 <= index < 7:
                daily_counts[index] += 1

        labels = [(week_ago + timedelta(days=i)).strftime('%a') for i in range(7)]
        chart_url = urllib.parse.quote(
            f"https://quickchart.io/chart?c={{type:'bar',data:{{labels:{labels},datasets:[{{label:'Screams',data:{daily_counts}}}]}}}}",
            safe=':/?=&'
        )
        
        # Get total stats
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
        
        # Get reaction stats
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
        
        # Generate reaction chart
        if emoji_data:
            labels = [emoji for emoji, _ in emoji_data]
            values = [count for _, count in emoji_data]
        else:
            labels = ["No reactions"]
            values = [1]

        chart = f"https://quickchart.io/chart?c={{type:'pie',data:{{labels:{labels},datasets:[{{data:{values}}}]}}}}"
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

@router.get("/stats/weekly", response_model=StressStatsResponse)
async def get_weekly_stress_graph_all(session: AsyncSession = Depends(get_session)):
    try:
        logger.debug("Getting weekly stress stats")
        _, week_ago = get_bounds(days=6, addition=False)

        daily_counts = [0] * 7
        stmt = select(Scream.timestamp).where(Scream.timestamp >= week_ago)
        result = await session.execute(stmt)
        timestamps = result.scalars().all()

        for ts in timestamps:
            index = (ts.date() - week_ago.date()).days
            if 0 <= index < 7:
                daily_counts[index] += 1

        labels = [(week_ago + timedelta(days=i)).strftime('%a') for i in range(7)]
        chart_url = f"https://quickchart.io/chart/create?c={{type:'bar',data:{{labels:{labels},datasets:[{{label:'Screams',data:{daily_counts}}}]}}}}"
        
        logger.info("Successfully retrieved weekly stress stats")
        return {"chart_url": urllib.parse.quote(chart_url, safe=':/?=&')}
    except Exception as e:
        logger.error(f"Failed to get weekly stress stats: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/create_admin", response_model=CreateAdminResponse)
async def create_admin(
    data: CreateAdminRequest,
    session: AsyncSession = Depends(get_session),  
    _: None = Depends(admin_middleware)
):
    try:
        logger.info(f"Creating admin for user: {data.user_id_to_admin[:5]}...")
        user_to_admin_hash = hash_user_id(data.user_id_to_admin)

        result = await session.execute(select(Admin).where(Admin.user_hash == user_to_admin_hash))
        existing_admin = result.scalar_one_or_none()
        if existing_admin:
            logger.warning(f"User already admin: {data.user_id_to_admin[:5]}...")
            return {"status": "already_admin"}

        admin = Admin(user_hash=user_to_admin_hash)
        session.add(admin)
        await session.commit()
        
        logger.info(f"Successfully created admin: {data.user_id_to_admin[:5]}...")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Failed to create admin: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/delete", response_model=DeleteResponse, dependencies=[Depends(admin_middleware)])
async def delete_scream(
    data: DeleteRequest, 
    session: AsyncSession = Depends(get_session),  
    _: None = Depends(admin_middleware)
):
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
    try:
        logger.debug(f"Getting user ID for: {data.user_id[:5]}...")
        if not data.user_id:
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
async def get_next_scream(user_id: str, session: AsyncSession = Depends(get_session)):
    try:
        logger.debug(f"Getting next scream for user: {user_id[:5]}...")
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

@router.post("/screams/admin", response_model=List[ScreamResponse], dependencies=[Depends(admin_middleware)])
async def get_screams_admin(
    data: UserRequest, 
    session: AsyncSession = Depends(get_session),  
    _: None = Depends(admin_middleware)
):
    try:
        logger.info(f"Getting screams for admin: {data.user_id[:5]}...")
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
        logger.error(f"Failed to get screams for admin: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/confirm", dependencies=[Depends(admin_middleware)])
async def confirm_scream(
    data: DeleteRequest, 
    session: AsyncSession = Depends(get_session),  
    _: None = Depends(admin_middleware)
):
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