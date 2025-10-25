"""
Dividend schemas.
"""
from datetime import date, datetime

from pydantic import BaseModel, Field


class DividendPaymentBase(BaseModel):
    """Base dividend payment schema."""
    symbol: str = Field(..., description="Investment symbol")
    value: float = Field(..., gt=0, description="Dividend payment amount")
    date: date = Field(..., description="Payment date")


class DividendPaymentCreate(DividendPaymentBase):
    """Schema for creating a dividend payment."""
    pass


class DividendPaymentResponse(BaseModel):
    """Schema for dividend payment response."""
    id: int
    investment_id: int
    value: float
    date: date
    created_at: datetime

    model_config = {"from_attributes": True}


class DividendReinvestmentBase(BaseModel):
    """Base dividend reinvestment schema."""
    symbol: str = Field(..., description="Investment symbol")
    units: float = Field(..., gt=0, description="Units acquired through reinvestment (fractional allowed)")
    price_per_unit: float = Field(..., gt=0, description="Price per unit")
    date: date = Field(..., description="Reinvestment date")


class DividendReinvestmentCreate(DividendReinvestmentBase):
    """Schema for creating a dividend reinvestment."""
    pass


class DividendReinvestmentResponse(BaseModel):
    """Schema for dividend reinvestment response."""
    id: int
    investment_id: int
    units: float
    price_per_unit: float
    date: date
    created_at: datetime
    total_value: float  # Calculated property

    model_config = {"from_attributes": True}
