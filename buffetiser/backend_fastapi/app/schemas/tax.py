"""
Tax schemas for CGT reporting and calculations.
"""
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.utils.constants import CGTTreatment, TaxMethod


class TaxParcelBase(BaseModel):
    """Base tax parcel schema."""
    acquisition_date: date
    units_acquired: float
    cost_base_per_unit: float
    description: Optional[str] = None


class TaxParcelCreate(TaxParcelBase):
    """Schema for creating a tax parcel."""
    investment_id: int


class TaxParcelResponse(TaxParcelBase):
    """Schema for tax parcel response."""
    id: int
    investment_id: int
    units_remaining: float
    total_cost_base: float
    is_fully_sold: bool
    percentage_remaining: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CGTEvent(BaseModel):
    """
    Represents a Capital Gains Tax event (usually a sale).

    This is the core data structure for tax reporting in Australia.
    """
    id: int
    event_date: date = Field(..., description="Date of CGT event")
    financial_year: str = Field(..., description="Financial year (e.g., '2023-24')")

    # Investment details
    investment_symbol: str
    investment_name: Optional[str] = None

    # Transaction details
    units_sold: float
    acquisition_date: date
    disposal_date: date

    # Financial details
    cost_base: float = Field(..., description="Total cost base of units sold")
    proceeds: float = Field(..., description="Sale proceeds after fees")

    # CGT calculation
    capital_gain: float = Field(..., description="Gross capital gain (proceeds - cost base)")
    holding_period_days: int = Field(..., description="Number of days held")
    cgt_treatment: CGTTreatment = Field(..., description="Short-term or long-term")

    # Australian CGT discount (50% for assets held > 12 months)
    cgt_discount_applied: bool = Field(
        ...,
        description="Whether 50% CGT discount was applied"
    )
    discount_amount: float = Field(default=0.0, description="Amount of CGT discount")
    net_capital_gain: float = Field(..., description="Capital gain after discount")

    # Additional info
    sale_id: int
    parcel_id: Optional[int] = None

    model_config = {"from_attributes": True}


class CGTSummary(BaseModel):
    """
    Summary of CGT for a financial year.

    Provides totals and breakdowns for tax reporting.
    """
    financial_year: str

    # Summary figures
    total_capital_gains: float = Field(..., description="Total gross capital gains")
    total_capital_losses: float = Field(..., description="Total capital losses")
    total_discount_amount: float = Field(..., description="Total CGT discount applied")
    net_capital_gain: float = Field(..., description="Net capital gain after discounts")

    # Breakdown by holding period
    short_term_gains: float = Field(default=0.0, description="Gains on assets held < 12 months")
    long_term_gains: float = Field(default=0.0, description="Gains on assets held >= 12 months")
    long_term_discounted: float = Field(default=0.0, description="Long-term gains after 50% discount")

    # Transaction counts
    total_events: int = Field(..., description="Total number of CGT events")
    short_term_events: int = Field(default=0, description="Number of short-term sales")
    long_term_events: int = Field(default=0, description="Number of long-term sales")

    # By investment
    gains_by_investment: dict[str, float] = Field(
        default_factory=dict,
        description="Capital gains grouped by investment symbol"
    )


class TaxReportResponse(BaseModel):
    """
    Complete tax report response.

    Includes all CGT events and summary for a given period.
    """
    financial_year: str
    report_generated: datetime = Field(default_factory=datetime.utcnow)

    # All CGT events
    events: list[CGTEvent] = Field(default_factory=list)

    # Summary
    summary: CGTSummary

    # Report metadata
    total_investments: int = Field(..., description="Number of investments with CGT events")
    date_range: dict[str, date] = Field(..., description="Start and end dates of FY")


class TaxCalculationRequest(BaseModel):
    """Request to calculate tax for a specific period."""
    start_date: date
    end_date: date
    method: TaxMethod = Field(default=TaxMethod.SPECIFIC_PARCEL)


class FinancialYearRequest(BaseModel):
    """Request for a specific financial year."""
    year: int = Field(..., description="Starting year of financial year (e.g., 2023 for FY2023-24)")


class AvailableParcelsResponse(BaseModel):
    """Response listing available parcels for sale."""
    investment_id: int
    investment_symbol: str
    total_units_available: float
    parcels: list[TaxParcelResponse]
