"""
Transaction endpoints for purchases and sales.
"""
from itertools import count

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.investment import Investment
from app.models.transaction import Purchase, Sale
from app.schemas.transaction import (
    PurchaseCreate,
    PurchaseResponse,
    SaleCreate,
    SaleResponse,
    SaleWithParcelSelection,
)
from app.services.tax_calculator import AustralianCGTCalculator
from app.utils.constants import TaxMethod

router = APIRouter()

# Trade counter for multiple transactions on same day
trade_counter = count()


@router.post("/purchase", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED)
async def create_purchase(
    purchase_data: PurchaseCreate,
    db: AsyncSession = Depends(get_db)
):
    """Record a purchase transaction."""
    # Find investment
    stmt = select(Investment).where(Investment.symbol == purchase_data.symbol.upper())
    result = await db.execute(stmt)
    investment = result.scalar_one_or_none()

    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Investment {purchase_data.symbol} not found"
        )

    # Create purchase
    purchase = Purchase(
        investment_id=investment.id,
        units=purchase_data.units,
        price_per_unit=purchase_data.price_per_unit,
        fee=purchase_data.fee,
        date=purchase_data.date,
        trade_count=next(trade_counter),
        currency=purchase_data.currency.value,
        exchange=purchase_data.exchange.value,
        platform=purchase_data.platform.value,
    )

    db.add(purchase)
    await db.flush()

    # Create tax parcel
    tax_calculator = AustralianCGTCalculator(db)
    await tax_calculator.create_tax_parcel_from_purchase(purchase)

    await db.commit()
    await db.refresh(purchase)

    return purchase


@router.post("/sale", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
async def create_sale(
    sale_data: SaleCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Record a sale transaction (automatic FIFO parcel selection).

    For manual parcel selection, use /sale-with-parcels endpoint.
    """
    # Find investment
    stmt = select(Investment).where(Investment.symbol == sale_data.symbol.upper())
    result = await db.execute(stmt)
    investment = result.scalar_one_or_none()

    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Investment {sale_data.symbol} not found"
        )

    # Create sale
    sale = Sale(
        investment_id=investment.id,
        units=sale_data.units,
        price_per_unit=sale_data.price_per_unit,
        fee=sale_data.fee,
        date=sale_data.date,
        trade_count=next(trade_counter),
        currency=sale_data.currency.value,
        exchange=sale_data.exchange.value,
    )

    db.add(sale)
    await db.flush()

    # Allocate to parcels using FIFO
    tax_calculator = AustralianCGTCalculator(db)
    allocations = await tax_calculator.allocate_sale_to_parcels(
        sale=sale,
        method=TaxMethod.FIFO
    )

    await db.commit()
    await db.refresh(sale)

    # Calculate CGT totals
    total_capital_gain = sum(a.capital_gain for a in allocations)
    total_discounted_gain = sum(a.discounted_capital_gain for a in allocations)
    cgt_discount_applied = any(a.cgt_discount_applied for a in allocations)

    # Add CGT info to response
    response = SaleResponse.model_validate(sale)
    response.capital_gain = total_capital_gain
    response.discounted_capital_gain = total_discounted_gain
    response.cgt_discount_applied = cgt_discount_applied

    return response


@router.post("/sale-with-parcels", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
async def create_sale_with_parcel_selection(
    sale_data: SaleWithParcelSelection,
    db: AsyncSession = Depends(get_db)
):
    """
    Record a sale with specific parcel selection.

    Allows users to choose which tax parcels to sell for tax optimization.
    """
    # Find investment
    stmt = select(Investment).where(Investment.symbol == sale_data.symbol.upper())
    result = await db.execute(stmt)
    investment = result.scalar_one_or_none()

    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Investment {sale_data.symbol} not found"
        )

    # Verify total units match
    total_selected_units = sum(p.units_to_sell for p in sale_data.parcel_selections)
    if abs(total_selected_units - sale_data.units) > 0.0001:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Selected parcel units ({total_selected_units}) don't match sale units ({sale_data.units})"
        )

    # Create sale
    sale = Sale(
        investment_id=investment.id,
        units=sale_data.units,
        price_per_unit=sale_data.price_per_unit,
        fee=sale_data.fee,
        date=sale_data.date,
        trade_count=next(trade_counter),
        currency=sale_data.currency.value,
        exchange=sale_data.exchange.value,
    )

    db.add(sale)
    await db.flush()

    # Allocate to selected parcels
    tax_calculator = AustralianCGTCalculator(db)
    parcel_selections = [
        {"parcel_id": p.parcel_id, "units_to_sell": p.units_to_sell}
        for p in sale_data.parcel_selections
    ]
    allocations = await tax_calculator.allocate_sale_to_parcels(
        sale=sale,
        parcel_selections=parcel_selections,
        method=TaxMethod.SPECIFIC_PARCEL
    )

    await db.commit()
    await db.refresh(sale)

    # Calculate CGT totals
    total_capital_gain = sum(a.capital_gain for a in allocations)
    total_discounted_gain = sum(a.discounted_capital_gain for a in allocations)
    cgt_discount_applied = any(a.cgt_discount_applied for a in allocations)

    # Add CGT info to response
    response = SaleResponse.model_validate(sale)
    response.capital_gain = total_capital_gain
    response.discounted_capital_gain = total_discounted_gain
    response.cgt_discount_applied = cgt_discount_applied

    return response


@router.get("/{investment_id}/purchases", response_model=list[PurchaseResponse])
async def get_investment_purchases(
    investment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all purchases for an investment."""
    stmt = (
        select(Purchase)
        .where(Purchase.investment_id == investment_id)
        .order_by(Purchase.date.desc())
    )
    result = await db.execute(stmt)
    purchases = result.scalars().all()

    return list(purchases)


@router.get("/{investment_id}/sales", response_model=list[SaleResponse])
async def get_investment_sales(
    investment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all sales for an investment."""
    stmt = (
        select(Sale)
        .where(Sale.investment_id == investment_id)
        .order_by(Sale.date.desc())
    )
    result = await db.execute(stmt)
    sales = result.scalars().all()

    return list(sales)
