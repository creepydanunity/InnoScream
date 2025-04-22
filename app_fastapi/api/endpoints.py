from datetime import timedelta
from app_fastapi.tools.meme import generate_meme_url
from app_fastapi.tools.time import get_bounds, get_week_start
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func, select, update
from app_fastapi.initializers.engine import get_session
from app_fastapi.tools.crypt import hash_user_id
from app_fastapi.models.scream import Scream
from app_fastapi.models.reaction import Reaction
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
)
from app_fastapi.schemas.requests import (
    CreateScreamRequest,
    ReactionRequest,
)

router = APIRouter()


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
                meme_url = await generate_meme_url(scream.user_hash[:5], scream.content)
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
    import urllib.parse
    
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
        index = (ts.date() - week_ago.date()).days
        if 0 <= index < 7:
            daily_counts[index] += 1

    labels = [(week_ago + timedelta(days=i)).strftime('%a') for i in range(7)]
    chart_url = f"https://quickchart.io/chart?c={{type:'bar',data:{{labels:{labels},datasets:[{{label:'Screams',data:{daily_counts}}}]}}}}"

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
        "chart_url": urllib.parse.quote(chart_url, safe=':/?=&'),
        "reaction_chart_url": reaction_chart_url
    }


@router.get("/stats/weekly", response_model=StressStatsResponse)
async def get_weekly_stress_graph_all(session: AsyncSession = Depends(get_session)):
    import urllib.parse

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
    chart_url = f"https://quickchart.io/chart?c={{type:'bar',data:{{labels:{labels},datasets:[{{label:'Screams',data:{daily_counts}}}]}}}}"
    return {"chart_url": urllib.parse.quote(chart_url, safe=':/?=&')}


@router.delete("/delete/{scream_id}", response_model=DeleteResponse)
async def delete_scream(scream_id: int, session: AsyncSession = Depends(get_session)):
    scream = await session.get(Scream, scream_id)
    if not scream:
        raise HTTPException(status_code=404, detail="Scream not found")

    await session.delete(scream)
    await session.commit()
    return {"status": "deleted"}


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
