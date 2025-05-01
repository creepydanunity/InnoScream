from datetime import datetime, timedelta, timezone
from sqlalchemy import select, func
from app_fastapi.models.scream import Scream
from app_fastapi.models.archive import Archive
from app_fastapi.models.reaction import Reaction
import logging

logger = logging.getLogger("app_fastapi")

async def archive_top(session):
    try:
        now = datetime.now(timezone.utc)
        year, week_num, _ = now.isocalendar()
        week_id = f"{year}-{week_num:02d}"
        
        stmt = (
            select(Scream.id, func.count(Reaction.id).label("votes"))
            .join(Reaction, Scream.id == Reaction.scream_id)
            .where(
                Scream.timestamp >= now - timedelta(weeks=1),
                Reaction.emoji != "❌"
            )
            .group_by(Scream.id)
            .order_by(func.count(Reaction.id).desc())
            .limit(3)
        )
        
        result = await session.execute(stmt)
        top_screams = result.all()
        
        for idx, (scream_id, votes) in enumerate(top_screams, 1):
            archive = Archive(
                scream_id=scream_id,
                week_id=week_id,
                place=idx
            )
            session.add(archive)
        
        await session.commit()
        logger.info(f"Archived top for week {week_id}")
        
    except Exception as e:
        logger.error(f"Archive failed: {str(e)}", exc_info=True)
        raise