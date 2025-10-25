"""
Australian Capital Gains Tax (CGT) Calculator.

Implements Australian tax rules:
- 50% CGT discount for assets held >= 12 months
- Financial year: July 1 - June 30
- Supports specific parcel identification for tax optimization
"""
from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.investment import Investment
from app.models.transaction import Purchase, Sale, TaxParcel, TaxParcelAllocation
from app.schemas.tax import CGTEvent, CGTSummary, CGTTreatment
from app.utils.constants import TaxMethod

settings = get_settings()


class AustralianCGTCalculator:
    """
    Calculator for Australian Capital Gains Tax.

    Handles parcel tracking, discount calculations, and financial year reporting.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.cgt_holding_period_days = settings.CGT_HOLDING_PERIOD_DAYS
        self.cgt_discount_rate = settings.CGT_DISCOUNT_RATE

    @staticmethod
    def get_financial_year(event_date: date) -> str:
        """
        Get the Australian financial year for a given date.

        Financial year runs from July 1 to June 30.

        Args:
            event_date: The date to check

        Returns:
            Financial year string (e.g., "2023-24")
        """
        if event_date.month >= 7:
            start_year = event_date.year
        else:
            start_year = event_date.year - 1

        end_year = start_year + 1
        return f"{start_year}-{str(end_year)[-2:]}"

    @staticmethod
    def get_financial_year_dates(year: int) -> tuple[date, date]:
        """
        Get start and end dates for a financial year.

        Args:
            year: Starting year (e.g., 2023 for FY2023-24)

        Returns:
            Tuple of (start_date, end_date)
        """
        start_date = date(year, 7, 1)
        end_date = date(year + 1, 6, 30)
        return start_date, end_date

    def calculate_holding_period(
        self,
        acquisition_date: date,
        disposal_date: date
    ) -> int:
        """
        Calculate holding period in days.

        Args:
            acquisition_date: Date of acquisition
            disposal_date: Date of disposal

        Returns:
            Number of days held
        """
        return (disposal_date - acquisition_date).days

    def determine_cgt_treatment(
        self,
        holding_period_days: int
    ) -> CGTTreatment:
        """
        Determine if CGT discount applies.

        Assets held >= 12 months qualify for 50% CGT discount in Australia.

        Args:
            holding_period_days: Number of days asset was held

        Returns:
            CGT treatment (short-term or long-term)
        """
        if holding_period_days >= self.cgt_holding_period_days:
            return CGTTreatment.LONG_TERM
        return CGTTreatment.SHORT_TERM

    def calculate_cgt_discount(
        self,
        capital_gain: float,
        cgt_treatment: CGTTreatment
    ) -> tuple[float, bool]:
        """
        Calculate CGT discount amount.

        Args:
            capital_gain: Gross capital gain
            cgt_treatment: Short-term or long-term

        Returns:
            Tuple of (discount_amount, discount_applied)
        """
        if cgt_treatment == CGTTreatment.LONG_TERM and capital_gain > 0:
            discount_amount = capital_gain * self.cgt_discount_rate
            return discount_amount, True
        return 0.0, False

    async def create_tax_parcel_from_purchase(
        self,
        purchase: Purchase
    ) -> TaxParcel:
        """
        Create a tax parcel from a purchase.

        Args:
            purchase: The purchase transaction

        Returns:
            Created TaxParcel
        """
        parcel = TaxParcel(
            investment_id=purchase.investment_id,
            purchase_id=purchase.id,
            acquisition_date=purchase.date,
            units_acquired=purchase.units,
            units_remaining=purchase.units,
            cost_base_per_unit=purchase.cost_base_per_unit,
            total_cost_base=purchase.total_cost,
            description=f"Purchase on {purchase.date}"
        )
        self.db.add(parcel)
        await self.db.flush()
        return parcel

    async def allocate_sale_to_parcels(
        self,
        sale: Sale,
        parcel_selections: Optional[list[dict]] = None,
        method: TaxMethod = TaxMethod.SPECIFIC_PARCEL
    ) -> list[TaxParcelAllocation]:
        """
        Allocate a sale to specific tax parcels.

        Args:
            sale: The sale transaction
            parcel_selections: Optional list of {parcel_id, units_to_sell}
            method: Tax method (specific_parcel, fifo, average_cost)

        Returns:
            List of TaxParcelAllocation objects
        """
        allocations = []

        if method == TaxMethod.SPECIFIC_PARCEL and parcel_selections:
            # User-selected parcels
            for selection in parcel_selections:
                parcel = await self.db.get(TaxParcel, selection["parcel_id"])
                if not parcel:
                    raise ValueError(f"Parcel {selection['parcel_id']} not found")

                units_to_sell = min(selection["units_to_sell"], parcel.units_remaining)
                allocation = await self._create_allocation(sale, parcel, units_to_sell)
                allocations.append(allocation)

        elif method == TaxMethod.FIFO:
            # First In First Out
            parcels = await self._get_available_parcels_fifo(sale.investment_id)
            units_remaining = sale.units

            for parcel in parcels:
                if units_remaining <= 0:
                    break

                units_to_sell = min(units_remaining, parcel.units_remaining)
                allocation = await self._create_allocation(sale, parcel, units_to_sell)
                allocations.append(allocation)
                units_remaining -= units_to_sell

        else:  # AVERAGE_COST or fallback
            # Use FIFO as fallback for average cost
            parcels = await self._get_available_parcels_fifo(sale.investment_id)
            units_remaining = sale.units

            for parcel in parcels:
                if units_remaining <= 0:
                    break

                units_to_sell = min(units_remaining, parcel.units_remaining)
                allocation = await self._create_allocation(sale, parcel, units_to_sell)
                allocations.append(allocation)
                units_remaining -= units_to_sell

        return allocations

    async def _create_allocation(
        self,
        sale: Sale,
        parcel: TaxParcel,
        units_to_sell: float
    ) -> TaxParcelAllocation:
        """
        Create a tax parcel allocation and update parcel.

        Args:
            sale: The sale transaction
            parcel: The tax parcel to sell from
            units_to_sell: Number of units to sell

        Returns:
            TaxParcelAllocation
        """
        # Calculate values
        cost_base = units_to_sell * parcel.cost_base_per_unit
        unit_proceeds = sale.proceeds_per_unit
        proceeds = units_to_sell * unit_proceeds

        # Calculate CGT
        capital_gain = proceeds - cost_base
        holding_period = self.calculate_holding_period(parcel.acquisition_date, sale.date)
        cgt_treatment = self.determine_cgt_treatment(holding_period)
        discount_amount, discount_applied = self.calculate_cgt_discount(
            capital_gain,
            cgt_treatment
        )
        discounted_gain = capital_gain - discount_amount

        # Create allocation
        allocation = TaxParcelAllocation(
            sale_id=sale.id,
            parcel_id=parcel.id,
            units_sold=units_to_sell,
            cost_base=cost_base,
            proceeds=proceeds,
            capital_gain=capital_gain,
            holding_period_days=holding_period,
            cgt_discount_applied=discount_applied,
            discounted_capital_gain=discounted_gain
        )

        # Update parcel
        parcel.units_remaining -= units_to_sell

        self.db.add(allocation)
        return allocation

    async def _get_available_parcels_fifo(
        self,
        investment_id: int
    ) -> list[TaxParcel]:
        """
        Get available parcels ordered by FIFO (earliest first).

        Args:
            investment_id: Investment ID

        Returns:
            List of available tax parcels
        """
        stmt = (
            select(TaxParcel)
            .where(TaxParcel.investment_id == investment_id)
            .where(TaxParcel.units_remaining > 0)
            .order_by(TaxParcel.acquisition_date.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_cgt_events_for_period(
        self,
        start_date: date,
        end_date: date,
        investment_id: Optional[int] = None
    ) -> list[CGTEvent]:
        """
        Get all CGT events for a period.

        Args:
            start_date: Start of period
            end_date: End of period
            investment_id: Optional filter by investment

        Returns:
            List of CGT events
        """
        # Build query for sales in period
        stmt = (
            select(Sale)
            .where(Sale.date >= start_date)
            .where(Sale.date <= end_date)
        )
        if investment_id:
            stmt = stmt.where(Sale.investment_id == investment_id)

        stmt = stmt.order_by(Sale.date.desc())

        result = await self.db.execute(stmt)
        sales = result.scalars().all()

        # Convert to CGT events
        cgt_events = []
        for sale in sales:
            # Get investment
            investment = await self.db.get(Investment, sale.investment_id)

            # Get allocations for this sale
            alloc_stmt = (
                select(TaxParcelAllocation)
                .where(TaxParcelAllocation.sale_id == sale.id)
            )
            alloc_result = await self.db.execute(alloc_stmt)
            allocations = alloc_result.scalars().all()

            # Create CGT event for each allocation
            for allocation in allocations:
                parcel = await self.db.get(TaxParcel, allocation.parcel_id)

                # Determine CGT treatment
                cgt_treatment = self.determine_cgt_treatment(allocation.holding_period_days)

                cgt_event = CGTEvent(
                    id=allocation.id,
                    event_date=sale.date,
                    financial_year=self.get_financial_year(sale.date),
                    investment_symbol=investment.symbol,
                    investment_name=investment.name,
                    units_sold=allocation.units_sold,
                    acquisition_date=parcel.acquisition_date,
                    disposal_date=sale.date,
                    cost_base=allocation.cost_base,
                    proceeds=allocation.proceeds,
                    capital_gain=allocation.capital_gain,
                    holding_period_days=allocation.holding_period_days,
                    cgt_treatment=cgt_treatment,
                    cgt_discount_applied=allocation.cgt_discount_applied,
                    discount_amount=(
                        allocation.capital_gain - allocation.discounted_capital_gain
                        if allocation.cgt_discount_applied else 0
                    ),
                    net_capital_gain=allocation.discounted_capital_gain,
                    sale_id=sale.id,
                    parcel_id=parcel.id
                )
                cgt_events.append(cgt_event)

        return cgt_events

    async def get_financial_year_summary(
        self,
        year: int
    ) -> CGTSummary:
        """
        Get CGT summary for a financial year.

        Args:
            year: Starting year of financial year

        Returns:
            CGT summary
        """
        start_date, end_date = self.get_financial_year_dates(year)
        events = await self.get_cgt_events_for_period(start_date, end_date)

        # Calculate totals
        total_gains = sum(e.capital_gain for e in events if e.capital_gain > 0)
        total_losses = sum(abs(e.capital_gain) for e in events if e.capital_gain < 0)
        total_discount = sum(e.discount_amount for e in events)
        net_gain = sum(e.net_capital_gain for e in events)

        # Short-term vs long-term
        short_term_gains = sum(
            e.capital_gain for e in events
            if e.cgt_treatment == CGTTreatment.SHORT_TERM and e.capital_gain > 0
        )
        long_term_gains = sum(
            e.capital_gain for e in events
            if e.cgt_treatment == CGTTreatment.LONG_TERM and e.capital_gain > 0
        )
        long_term_discounted = sum(
            e.net_capital_gain for e in events
            if e.cgt_treatment == CGTTreatment.LONG_TERM and e.capital_gain > 0
        )

        # Event counts
        total_events = len(events)
        short_term_count = len([
            e for e in events if e.cgt_treatment == CGTTreatment.SHORT_TERM
        ])
        long_term_count = len([
            e for e in events if e.cgt_treatment == CGTTreatment.LONG_TERM
        ])

        # By investment
        gains_by_investment = {}
        for event in events:
            symbol = event.investment_symbol
            if symbol not in gains_by_investment:
                gains_by_investment[symbol] = 0
            gains_by_investment[symbol] += event.net_capital_gain

        return CGTSummary(
            financial_year=self.get_financial_year(start_date),
            total_capital_gains=total_gains,
            total_capital_losses=total_losses,
            total_discount_amount=total_discount,
            net_capital_gain=net_gain,
            short_term_gains=short_term_gains,
            long_term_gains=long_term_gains,
            long_term_discounted=long_term_discounted,
            total_events=total_events,
            short_term_events=short_term_count,
            long_term_events=long_term_count,
            gains_by_investment=gains_by_investment
        )
