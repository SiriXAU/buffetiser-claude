"""
Investment schemas.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.utils.constants import InvestmentType


class InvestmentBase(BaseModel):
    """Base investment schema."""
    symbol: str = Field(..., min_length=1, max_length=32, description="Investment symbol")
    name: Optional[str] = Field(None, max_length=256, description="Investment name")
    type: InvestmentType = Field(default=InvestmentType.SHARES, description="Investment type")


class InvestmentCreate(InvestmentBase):
    """Schema for creating a new investment."""
    exchange: str = Field(..., description="Exchange code")

    @field_validator("symbol", "exchange")
    @classmethod
    def uppercase_fields(cls, v: str) -> str:
        """Convert symbol and exchange to uppercase."""
        return v.upper() if v else v


class InvestmentUpdate(BaseModel):
    """Schema for updating an investment."""
    name: Optional[str] = Field(None, max_length=256)
    live_price: Optional[float] = Field(None, ge=0)
    visible: Optional[bool] = None


class InvestmentResponse(InvestmentBase):
    """Schema for investment response."""
    id: int
    key: str
    live_price: float = 0.0
    visible: bool = True
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class InvestmentDetail(InvestmentResponse):
    """
    Detailed investment response with calculated fields.

    This includes all the calculated metrics like units held, profit, etc.
    """
    # Current holdings
    units_held: float = Field(default=0.0, description="Total units currently held")
    average_cost: float = Field(default=0.0, description="Average cost per unit")
    total_cost: float = Field(default=0.0, description="Total cost including fees")

    # Current values
    current_value: float = Field(default=0.0, description="Current market value")

    # Profit/Loss
    total_profit: float = Field(default=0.0, description="Total profit/loss in dollars")
    total_profit_percent: float = Field(default=0.0, description="Total profit/loss percentage")

    # Daily changes
    daily_change: float = Field(default=0.0, description="Daily price change")
    daily_change_percent: float = Field(default=0.0, description="Daily percentage change")

    # Price history (dates and values for charting)
    price_history: list[dict] = Field(default_factory=list, description="Historical price data")

    model_config = {"from_attributes": True}
