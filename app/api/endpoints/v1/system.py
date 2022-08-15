from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.config import settings
from app.schemas.system import Health, Root

router = APIRouter()


@router.get("/", response_model=Root)
def root() -> dict:
    return {"name": f"{settings.PROJECT_NAME}", "version": f"{settings.APP_VERSION}"}


@router.get("/health", response_model=Health)
async def get_health(db: AsyncSession = Depends(get_db)) -> dict:
    try:
        healthy = await db.execute("SELECT 1")
        if healthy.scalars().first() is None:
            raise HTTPException(status_code=404, detail={"msg": "Not Healthy ❌"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"msg": "Healthy ✅"}
