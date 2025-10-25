"""
History models for price tracking.
"""
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.investment import Investment


class History(Base):
    """
    Records daily price history for an investment.

    Stores OHLCV (Open, High, Low, Close, Volume) data.
    """

    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Foreign key to investment
    investment_id: Mapped[int] = mapped_column(
        ForeignKey("investments.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Price data
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    high: Mapped[float] = mapped_column(Float, default=0.0)
    low: Mapped[float] = mapped_column(Float, default=0.0)
    close: Mapped[float] = mapped_column(Float, default=0.0)
    volume: Mapped[int] = mapped_column(Integer, default=0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationship
    investment: Mapped["Investment"] = relationship("Investment", back_populates="history")

    __table_args__ = (
        UniqueConstraint("investment_id", "date", name="uq_history_date"),
    )

    def __repr__(self) -> str:
        return (
            f"<History(id={self.id}, date={self.date}, "
            f"close={self.close}, volume={self.volume})>"
        )


class DailyChange(Base):
    """
    Stores the most recent daily change for an investment.

    This is temporary data that gets updated frequently and represents
    the current day's price movement.
    """

    __tablename__ = "daily_changes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Investment identifier
    symbol: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)

    # Daily change data
    daily_change: Mapped[float] = mapped_column(Float, default=0.0)
    daily_change_percent: Mapped[float] = mapped_column(Float, default=0.0)

    # Timestamps
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return (
            f"<DailyChange(symbol={self.symbol}, "
            f"change={self.daily_change}, percent={self.daily_change_percent}%)>"
        )
