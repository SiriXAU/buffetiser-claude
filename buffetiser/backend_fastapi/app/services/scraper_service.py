"""
Price scraping service for updating investment prices.

Ports logic from Django version using async httpx.
"""
import asyncio
from datetime import date
from typing import Optional

import httpx
from bs4 import BeautifulSoup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.history import DailyChange, History
from app.models.investment import Investment


class PriceScraperService:
    """Service for scraping investment prices from market sources."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.base_url = "https://bigcharts.marketwatch.com/quotes/multi.asp"

    async def scrape_investment_price(
        self, investment: Investment
    ) -> Optional[dict]:
        """
        Scrape current price and daily change for an investment.

        Args:
            investment: Investment to scrape

        Returns:
            Dictionary with price data or None if failed
        """
        url = f"{self.base_url}?view=q&msymb=au:{investment.symbol}+"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract price data (adjust selectors based on actual HTML structure)
            # This is a simplified version - adjust based on actual site structure
            price_data = {
                "symbol": investment.symbol,
                "last_price": 0.0,
                "daily_change": 0.0,
                "daily_change_percent": 0.0,
                "high": 0.0,
                "low": 0.0,
                "volume": 0,
            }

            # Note: You'll need to adjust these selectors based on the actual HTML structure
            # of the market data source you're using

            return price_data

        except Exception as e:
            print(f"Error scraping {investment.symbol}: {e}")
            return None

    async def update_investment_price(self, investment_id: int) -> bool:
        """
        Update an investment's live price.

        Args:
            investment_id: Investment ID

        Returns:
            True if successful, False otherwise
        """
        investment = await self.db.get(Investment, investment_id)
        if not investment:
            return False

        price_data = await self.scrape_investment_price(investment)
        if not price_data:
            return False

        # Update investment live price
        investment.live_price = price_data.get("last_price", investment.live_price)

        # Update or create daily change
        daily_change_stmt = select(DailyChange).where(
            DailyChange.symbol == investment.symbol
        )
        result = await self.db.execute(daily_change_stmt)
        daily_change = result.scalar_one_or_none()

        if daily_change:
            daily_change.daily_change = price_data.get("daily_change", 0.0)
            daily_change.daily_change_percent = price_data.get("daily_change_percent", 0.0)
        else:
            daily_change = DailyChange(
                symbol=investment.symbol,
                daily_change=price_data.get("daily_change", 0.0),
                daily_change_percent=price_data.get("daily_change_percent", 0.0),
            )
            self.db.add(daily_change)

        await self.db.commit()
        return True

    async def update_investment_history(self, investment_id: int) -> bool:
        """
        Add a history entry for an investment.

        Args:
            investment_id: Investment ID

        Returns:
            True if successful, False otherwise
        """
        investment = await self.db.get(Investment, investment_id)
        if not investment:
            return False

        price_data = await self.scrape_investment_price(investment)
        if not price_data:
            return False

        today = date.today()

        # Check if history entry already exists for today
        history_stmt = select(History).where(
            History.investment_id == investment_id,
            History.date == today
        )
        result = await self.db.execute(history_stmt)
        existing_history = result.scalar_one_or_none()

        if existing_history:
            # Update existing entry
            existing_history.high = price_data.get("high", existing_history.high)
            existing_history.low = price_data.get("low", existing_history.low)
            existing_history.close = price_data.get("last_price", existing_history.close)
            existing_history.volume = price_data.get("volume", existing_history.volume)
        else:
            # Create new history entry
            history = History(
                investment_id=investment_id,
                date=today,
                high=price_data.get("high", investment.live_price),
                low=price_data.get("low", investment.live_price),
                close=price_data.get("last_price", investment.live_price),
                volume=price_data.get("volume", 0),
            )
            self.db.add(history)

        await self.db.commit()
        return True

    async def update_all_investments(self) -> dict:
        """
        Update prices and history for all visible investments.

        Returns:
            Dictionary with update statistics
        """
        stmt = select(Investment).where(Investment.visible == True)
        result = await self.db.execute(stmt)
        investments = result.scalars().all()

        success_count = 0
        failed_count = 0
        failed_symbols = []

        for investment in investments:
            try:
                price_success = await self.update_investment_price(investment.id)
                history_success = await self.update_investment_history(investment.id)

                if price_success and history_success:
                    success_count += 1
                else:
                    failed_count += 1
                    failed_symbols.append(investment.symbol)

                # Small delay to avoid overwhelming the server
                await asyncio.sleep(0.5)

            except Exception as e:
                print(f"Error updating {investment.symbol}: {e}")
                failed_count += 1
                failed_symbols.append(investment.symbol)

        return {
            "total": len(investments),
            "success": success_count,
            "failed": failed_count,
            "failed_symbols": failed_symbols,
        }

    async def update_daily_changes_only(self) -> dict:
        """
        Update only daily changes (lighter operation for frequent updates).

        Returns:
            Dictionary with update statistics
        """
        stmt = select(Investment).where(Investment.visible == True)
        result = await self.db.execute(stmt)
        investments = result.scalars().all()

        # Clear existing daily changes
        await self.db.execute(select(DailyChange))
        await self.db.execute(DailyChange.__table__.delete())

        success_count = 0
        failed_count = 0

        for investment in investments:
            try:
                success = await self.update_investment_price(investment.id)
                if success:
                    success_count += 1
                else:
                    failed_count += 1

                await asyncio.sleep(0.5)

            except Exception as e:
                print(f"Error updating {investment.symbol}: {e}")
                failed_count += 1

        return {
            "total": len(investments),
            "success": success_count,
            "failed": failed_count,
        }
