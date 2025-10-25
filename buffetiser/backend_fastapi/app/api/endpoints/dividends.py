"""
Dividend endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.dividend import DividendPayment, DividendReinvestment
from app.models.investment import Investment
from app.schemas.dividend import (
    DividendPaymentCreate,
    DividendPaymentResponse,
    DividendReinvestmentCreate,
    DividendReinvestmentResponse,
)

router = APIRouter()


@router.post("/payment", response_model=DividendPaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_dividend_payment(
    dividend_data: DividendPaymentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Record a dividend payment."""
    # Find investment
    stmt = select(Investment).where(Investment.symbol == dividend_data.symbol.upper())
    result = await db.execute(stmt)
    investment = result.scalar_one_or_none()

    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Investment {dividend_data.symbol} not found"
        )

    # Create dividend payment
    dividend = DividendPayment(
        investment_id=investment.id,
        value=dividend_data.value,
        date=dividend_data.date,
    )

    db.add(dividend)
    await db.commit()
    await db.refresh(dividend)

    return dividend


@router.post("/reinvestment", response_model=DividendReinvestmentResponse, status_code=status.HTTP_201_CREATED)
async def create_dividend_reinvestment(
    reinvestment_data: DividendReinvestmentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Record a dividend reinvestment."""
    # Find investment
    stmt = select(Investment).where(Investment.symbol == reinvestment_data.symbol.upper())
    result = await db.execute(stmt)
    investment = result.scalar_one_or_none()

    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Investment {reinvestment_data.symbol} not found"
        )

    # Create dividend reinvestment
    reinvestment = DividendReinvestment(
        investment_id=investment.id,
        units=reinvestment_data.units,
        price_per_unit=reinvestment_data.price_per_unit,
        date=reinvestment_data.date,
    )

    db.add(reinvestment)
    await db.commit()
    await db.refresh(reinvestment)

    return reinvestment


@router.get("/{investment_id}/payments", response_model=list[DividendPaymentResponse])
async def get_dividend_payments(
    investment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all dividend payments for an investment."""
    stmt = (
        select(DividendPayment)
        .where(DividendPayment.investment_id == investment_id)
        .order_by(DividendPayment.date.desc())
    )
    result = await db.execute(stmt)
    payments = result.scalars().all()

    return list(payments)


@router.get("/{investment_id}/reinvestments", response_model=list[DividendReinvestmentResponse])
async def get_dividend_reinvestments(
    investment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all dividend reinvestments for an investment."""
    stmt = (
        select(DividendReinvestment)
        .where(DividendReinvestment.investment_id == investment_id)
        .order_by(DividendReinvestment.date.desc())
    )
    result = await db.execute(stmt)
    reinvestments = result.scalars().all()

    return list(reinvestments)
