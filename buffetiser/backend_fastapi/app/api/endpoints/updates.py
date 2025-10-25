"""
Update endpoints for price scraping and data refresh.
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.scraper_service import PriceScraperService

router = APIRouter()


@router.post("/prices/all")
async def update_all_prices(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Update prices and history for all investments.

    This runs in the background to avoid blocking.
    """
    async def update_task():
        service = PriceScraperService(db)
        result = await service.update_all_investments()
        print(f"Price update complete: {result}")

    background_tasks.add_task(update_task)

    return {
        "message": "Price update started in background",
        "status": "processing"
    }


@router.post("/prices/daily")
async def update_daily_changes(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Update only daily price changes (lighter operation).

    This runs in the background.
    """
    async def update_task():
        service = PriceScraperService(db)
        result = await service.update_daily_changes_only()
        print(f"Daily changes update complete: {result}")

    background_tasks.add_task(update_task)

    return {
        "message": "Daily changes update started in background",
        "status": "processing"
    }


@router.post("/prices/investment/{investment_id}")
async def update_investment_price(
    investment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Update price for a specific investment.
    """
    service = PriceScraperService(db)
    success = await service.update_investment_price(investment_id)

    if success:
        return {"message": "Price updated successfully", "investment_id": investment_id}
    else:
        return {"message": "Failed to update price", "investment_id": investment_id}
