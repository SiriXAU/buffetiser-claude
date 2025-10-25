"""
Tax endpoints for CGT reporting and calculations.
"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.transaction import TaxParcel
from app.schemas.tax import (
    AvailableParcelsResponse,
    FinancialYearRequest,
    TaxParcelResponse,
    TaxReportResponse,
)
from app.services.tax_calculator import AustralianCGTCalculator

router = APIRouter()


@router.get("/events", response_model=list)
async def get_cgt_events(
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
    investment_id: int = Query(None, description="Filter by investment"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all CGT events for a date range.

    Returns list of Capital Gains Tax events with full details.
    """
    tax_calculator = AustralianCGTCalculator(db)
    events = await tax_calculator.get_cgt_events_for_period(
        start_date=start_date,
        end_date=end_date,
        investment_id=investment_id
    )

    return events


@router.get("/report/{year}", response_model=TaxReportResponse)
async def get_financial_year_report(
    year: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get complete CGT report for a financial year.

    Args:
        year: Starting year of financial year (e.g., 2023 for FY2023-24)

    Returns:
        Complete tax report with events and summary
    """
    tax_calculator = AustralianCGTCalculator(db)

    # Get date range
    start_date, end_date = tax_calculator.get_financial_year_dates(year)

    # Get all events
    events = await tax_calculator.get_cgt_events_for_period(start_date, end_date)

    # Get summary
    summary = await tax_calculator.get_financial_year_summary(year)

    # Count unique investments
    unique_investments = len(set(e.investment_symbol for e in events))

    return TaxReportResponse(
        financial_year=summary.financial_year,
        events=events,
        summary=summary,
        total_investments=unique_investments,
        date_range={"start": start_date, "end": end_date}
    )


@router.get("/parcels/{investment_id}", response_model=AvailableParcelsResponse)
async def get_available_parcels(
    investment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all available tax parcels for an investment.

    Useful for showing users which parcels they can sell.
    """
    from app.models.investment import Investment

    # Get investment
    investment = await db.get(Investment, investment_id)
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )

    # Get available parcels
    stmt = (
        select(TaxParcel)
        .where(TaxParcel.investment_id == investment_id)
        .where(TaxParcel.units_remaining > 0)
        .order_by(TaxParcel.acquisition_date)
    )
    result = await db.execute(stmt)
    parcels = result.scalars().all()

    total_units = sum(p.units_remaining for p in parcels)

    return AvailableParcelsResponse(
        investment_id=investment_id,
        investment_symbol=investment.symbol,
        total_units_available=total_units,
        parcels=[TaxParcelResponse.model_validate(p) for p in parcels]
    )


@router.get("/summary/{year}")
async def get_tax_summary(
    year: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get tax summary for a financial year.

    Quick overview without detailed events.
    """
    tax_calculator = AustralianCGTCalculator(db)
    summary = await tax_calculator.get_financial_year_summary(year)

    return summary
