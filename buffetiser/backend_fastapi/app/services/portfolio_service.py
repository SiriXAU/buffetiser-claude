"""
Portfolio calculation service.

Provides portfolio-level calculations including total value, costs, and history.
"""
from datetime import date, datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dividend import DividendPayment, DividendReinvestment
from app.models.history import History
from app.models.investment import Investment
from app.models.transaction import Purchase, Sale


class PortfolioService:
    """Service for portfolio-level calculations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_total_units_held(self, investment_id: int, as_of_date: Optional[date] = None) -> float:
        """
        Get total units held for an investment as of a specific date.

        Args:
            investment_id: Investment ID
            as_of_date: Date to calculate units (defaults to today)

        Returns:
            Total units held
        """
        if as_of_date is None:
            as_of_date = date.today()

        # Purchases
        purchase_stmt = select(func.sum(Purchase.units)).where(
            Purchase.investment_id == investment_id,
            Purchase.date <= as_of_date
        )
        purchase_result = await self.db.execute(purchase_stmt)
        purchase_units = purchase_result.scalar() or 0.0

        # Reinvestments
        reinvest_stmt = select(func.sum(DividendReinvestment.units)).where(
            DividendReinvestment.investment_id == investment_id,
            DividendReinvestment.date <= as_of_date
        )
        reinvest_result = await self.db.execute(reinvest_stmt)
        reinvest_units = reinvest_result.scalar() or 0.0

        # Sales
        sale_stmt = select(func.sum(Sale.units)).where(
            Sale.investment_id == investment_id,
            Sale.date <= as_of_date
        )
        sale_result = await self.db.execute(sale_stmt)
        sale_units = sale_result.scalar() or 0.0

        return purchase_units + reinvest_units - sale_units

    async def get_total_cost(self, investment_id: int, as_of_date: Optional[date] = None) -> float:
        """
        Get total cost base for an investment.

        Args:
            investment_id: Investment ID
            as_of_date: Date to calculate cost (defaults to today)

        Returns:
            Total cost including fees
        """
        if as_of_date is None:
            as_of_date = date.today()

        total_cost = 0.0
        total_units_purchased = 0.0

        # Sum purchase costs and track units
        purchases = await self.db.execute(
            select(Purchase).where(
                Purchase.investment_id == investment_id,
                Purchase.date <= as_of_date
            )
        )
        for purchase in purchases.scalars():
            total_cost += purchase.total_cost
            total_units_purchased += purchase.units

        # Sum reinvestment costs and track units
        reinvestments = await self.db.execute(
            select(DividendReinvestment).where(
                DividendReinvestment.investment_id == investment_id,
                DividendReinvestment.date <= as_of_date
            )
        )
        for reinvest in reinvestments.scalars():
            total_cost += reinvest.units * reinvest.price_per_unit
            total_units_purchased += reinvest.units

        # Subtract sale proceeds (on average cost basis)
        if total_units_purchased > 0:
            avg_cost = total_cost / total_units_purchased

            sales = await self.db.execute(
                select(Sale).where(
                    Sale.investment_id == investment_id,
                    Sale.date <= as_of_date
                )
            )
            for sale in sales.scalars():
                total_cost -= sale.units * avg_cost

        return total_cost

    async def get_current_value(self, investment_id: int) -> float:
        """
        Get current market value of an investment.

        Args:
            investment_id: Investment ID

        Returns:
            Current value (units * live_price)
        """
        investment = await self.db.get(Investment, investment_id)
        if not investment:
            return 0.0

        units = await self.get_total_units_held(investment_id)
        return units * investment.live_price

    async def get_investment_summary(self, investment_id: int) -> dict:
        """
        Get complete summary for an investment.

        Args:
            investment_id: Investment ID

        Returns:
            Dictionary with all calculated values
        """
        investment = await self.db.get(Investment, investment_id)
        if not investment:
            return {}

        units_held = await self.get_total_units_held(investment_id)
        total_cost = await self.get_total_cost(investment_id)
        current_value = await self.get_current_value(investment_id)

        average_cost = total_cost / units_held if units_held > 0 else 0.0
        total_profit = current_value - total_cost
        profit_percent = (total_profit / total_cost * 100) if total_cost > 0 else 0.0

        return {
            "investment_id": investment.id,
            "symbol": investment.symbol,
            "name": investment.name,
            "units_held": units_held,
            "live_price": investment.live_price,
            "average_cost": average_cost,
            "total_cost": total_cost,
            "current_value": current_value,
            "total_profit": total_profit,
            "total_profit_percent": profit_percent,
        }

    async def get_portfolio_summary(self) -> dict:
        """
        Get summary for entire portfolio.

        Returns:
            Dictionary with portfolio totals
        """
        investments_stmt = select(Investment).where(Investment.visible == True)
        result = await self.db.execute(investments_stmt)
        investments = result.scalars().all()

        total_cost = 0.0
        total_value = 0.0
        total_profit = 0.0

        for investment in investments:
            summary = await self.get_investment_summary(investment.id)
            total_cost += summary.get("total_cost", 0)
            total_value += summary.get("current_value", 0)
            total_profit += summary.get("total_profit", 0)

        profit_percent = (total_profit / total_cost * 100) if total_cost > 0 else 0.0

        return {
            "total_cost": total_cost,
            "total_value": total_value,
            "total_profit": total_profit,
            "total_profit_percent": profit_percent,
            "total_investments": len(investments),
        }

    async def get_portfolio_history(self, days: int = 365) -> list[dict]:
        """
        Get portfolio value history over time.

        Args:
            days: Number of days of history to retrieve

        Returns:
            List of {date, total_value} dictionaries
        """
        # Get all investments
        investments_stmt = select(Investment).where(Investment.visible == True)
        result = await self.db.execute(investments_stmt)
        investments = result.scalars().all()

        # Get unique history dates
        history_stmt = (
            select(History.date)
            .distinct()
            .order_by(History.date.desc())
            .limit(days)
        )
        dates_result = await self.db.execute(history_stmt)
        dates = [row[0] for row in dates_result.all()]
        dates.sort()

        # Calculate portfolio value for each date
        history_data = []
        for history_date in dates:
            total_value = 0.0

            for investment in investments:
                # Get units held on this date
                units = await self.get_total_units_held(investment.id, history_date)

                # Get price on this date
                price_stmt = select(History.close).where(
                    History.investment_id == investment.id,
                    History.date == history_date
                )
                price_result = await self.db.execute(price_stmt)
                close_price = price_result.scalar() or investment.live_price

                total_value += units * close_price

            history_data.append({
                "date": history_date.isoformat(),
                "total_value": total_value
            })

        return history_data
