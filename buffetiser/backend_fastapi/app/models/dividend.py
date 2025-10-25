"""
Dividend models for payments and reinvestments.
"""
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.investment import Investment


class DividendPayment(Base):
    """
    Records a cash dividend payment.

    When an investment pays out a dividend in cash rather than reinvesting it.
    """

    __tablename__ = "dividend_payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Foreign key to investment
    investment_id: Mapped[int] = mapped_column(
        ForeignKey("investments.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Payment details
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationship
    investment: Mapped["Investment"] = relationship(
        "Investment",
        back_populates="dividend_payments"
    )

    __table_args__ = (
        UniqueConstraint("investment_id", "date", name="uq_dividend_payment_date"),
    )

    def __repr__(self) -> str:
        return f"<DividendPayment(id={self.id}, value={self.value}, date={self.date})>"


class DividendReinvestment(Base):
    """
    Records a dividend reinvestment.

    When a dividend is used to automatically purchase additional shares/units
    of the investment. This increases the total units held.
    """

    __tablename__ = "dividend_reinvestments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Foreign key to investment
    investment_id: Mapped[int] = mapped_column(
        ForeignKey("investments.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Reinvestment details
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    units: Mapped[int] = mapped_column(Integer, default=0)
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationship
    investment: Mapped["Investment"] = relationship(
        "Investment",
        back_populates="dividend_reinvestments"
    )

    __table_args__ = (
        UniqueConstraint("investment_id", "date", name="uq_dividend_reinvestment_date"),
    )

    def __repr__(self) -> str:
        return (
            f"<DividendReinvestment(id={self.id}, units={self.units}, "
            f"price={self.price_per_unit}, date={self.date})>"
        )

    @property
    def total_value(self) -> float:
        """Total value of the reinvested dividend."""
        return self.units * self.price_per_unit
