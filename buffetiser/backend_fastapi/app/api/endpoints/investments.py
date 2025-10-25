"""
Investment endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.investment import Investment
from app.schemas.investment import (
    InvestmentCreate,
    InvestmentDetail,
    InvestmentResponse,
    InvestmentUpdate,
)

router = APIRouter()


@router.post("/", response_model=InvestmentResponse, status_code=status.HTTP_201_CREATED)
async def create_investment(
    investment_data: InvestmentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new investment."""
    # Generate key
    key = Investment.generate_key(investment_data.exchange, investment_data.symbol)

    # Check if exists
    stmt = select(Investment).where(Investment.key == key)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Investment already exists"
        )

    # Create new investment
    investment = Investment(
        key=key,
        symbol=investment_data.symbol.upper(),
        name=investment_data.name,
        type=investment_data.type.value,
    )

    db.add(investment)
    await db.commit()
    await db.refresh(investment)

    return investment


@router.get("/", response_model=list[InvestmentResponse])
async def list_investments(
    visible_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """List all investments."""
    stmt = select(Investment)
    if visible_only:
        stmt = stmt.where(Investment.visible == True)

    stmt = stmt.order_by(Investment.symbol)

    result = await db.execute(stmt)
    investments = result.scalars().all()

    return list(investments)


@router.get("/{investment_id}", response_model=InvestmentResponse)
async def get_investment(
    investment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific investment."""
    investment = await db.get(Investment, investment_id)
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )

    return investment


@router.patch("/{investment_id}", response_model=InvestmentResponse)
async def update_investment(
    investment_id: int,
    update_data: InvestmentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an investment."""
    investment = await db.get(Investment, investment_id)
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )

    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(investment, field, value)

    await db.commit()
    await db.refresh(investment)

    return investment


@router.delete("/{investment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_investment(
    investment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete an investment (soft delete by setting visible=False)."""
    investment = await db.get(Investment, investment_id)
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )

    investment.visible = False
    await db.commit()

    return None
