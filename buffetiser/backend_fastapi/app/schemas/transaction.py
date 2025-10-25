"""
Transaction schemas for purchases and sales.
"""
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.utils.constants import Currency, Exchange, Platform


class PurchaseBase(BaseModel):
    """Base purchase schema."""
    symbol: str = Field(..., description="Investment symbol")
    units: float = Field(..., gt=0, description="Number of units purchased")
    price_per_unit: float = Field(..., gt=0, description="Price per unit")
    fee: float = Field(default=0.0, ge=0, description="Transaction fee")
    date: date = Field(..., description="Purchase date")
    currency: Currency = Field(default=Currency.AUD)
    exchange: Exchange = Field(default=Exchange.XASX)
    platform: Platform = Field(default=Platform.CMC)


class PurchaseCreate(PurchaseBase):
    """Schema for creating a purchase."""
    pass


class PurchaseResponse(BaseModel):
    """Schema for purchase response."""
    id: int
    investment_id: int
    units: float
    price_per_unit: float
    fee: float
    date: date
    trade_count: int
    currency: str
    exchange: str
    platform: str
    created_at: datetime

    # Calculated fields
    total_cost: float
    cost_base_per_unit: float

    model_config = {"from_attributes": True}


class SaleBase(BaseModel):
    """Base sale schema."""
    symbol: str = Field(..., description="Investment symbol")
    units: float = Field(..., gt=0, description="Number of units sold")
    price_per_unit: float = Field(..., gt=0, description="Sale price per unit")
    fee: float = Field(default=0.0, ge=0, description="Transaction fee")
    date: date = Field(..., description="Sale date")
    currency: Currency = Field(default=Currency.AUD)
    exchange: Exchange = Field(default=Exchange.XASX)


class SaleCreate(SaleBase):
    """Schema for creating a sale (automatic parcel selection)."""
    pass


class ParcelSelection(BaseModel):
    """Schema for selecting specific parcels to sell."""
    parcel_id: int = Field(..., description="Tax parcel ID")
    units_to_sell: float = Field(..., gt=0, description="Units to sell from this parcel")


class SaleWithParcelSelection(SaleBase):
    """
    Schema for creating a sale with specific parcel selection.

    Allows users to choose which tax parcels to sell for tax optimization.
    """
    parcel_selections: list[ParcelSelection] = Field(
        ...,
        description="List of parcels to sell with units from each"
    )


class SaleResponse(BaseModel):
    """Schema for sale response."""
    id: int
    investment_id: int
    units: float
    price_per_unit: float
    fee: float
    date: date
    trade_count: int
    currency: str
    exchange: str
    created_at: datetime

    # Calculated fields
    total_proceeds: float
    proceeds_per_unit: float

    # CGT information
    capital_gain: Optional[float] = None
    cgt_discount_applied: bool = False
    discounted_capital_gain: Optional[float] = None

    model_config = {"from_attributes": True}
