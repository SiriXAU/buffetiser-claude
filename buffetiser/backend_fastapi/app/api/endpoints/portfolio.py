"""
Portfolio endpoints for overall portfolio statistics.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.investment import Investment
from app.services.portfolio_service import PortfolioService

router = APIRouter()


@router.get("/summary")
async def get_portfolio_summary(
    db: AsyncSession = Depends(get_db)
):
    """
    Get portfolio summary with totals.

    Returns:
        - total_cost: Total amount invested
        - total_value: Current market value
        - total_profit: Profit/loss in dollars
        - total_profit_percent: Profit/loss percentage
        - total_investments: Number of investments
    """
    service = PortfolioService(db)
    return await service.get_portfolio_summary()


@router.get("/history")
async def get_portfolio_history(
    days: int = Query(default=365, ge=1, le=1825, description="Number of days of history"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get portfolio value history over time.

    Args:
        days: Number of days of history (default 365, max 1825 = 5 years)

    Returns:
        List of {date, total_value} for charting
    """
    service = PortfolioService(db)
    return await service.get_portfolio_history(days)


@router.get("/investments/summary")
async def get_all_investments_summary(
    db: AsyncSession = Depends(get_db)
):
    """
    Get summary for all investments.

    Returns list of investment summaries with calculated values.
    """
    service = PortfolioService(db)

    stmt = select(Investment).where(Investment.visible == True)
    result = await db.execute(stmt)
    investments = result.scalars().all()

    summaries = []
    for investment in investments:
        summary = await service.get_investment_summary(investment.id)
        summaries.append(summary)

    return summaries
