"""
Investment model.
"""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.constants import InvestmentType

if TYPE_CHECKING:
    from app.models.dividend import DividendPayment, DividendReinvestment
    from app.models.history import DailyChange, History
    from app.models.transaction import Purchase, Sale


class Investment(Base):
    """
    Represents a stock or cryptocurrency investment.

    One Investment can have multiple purchases, sales, dividends, etc.
    """

    __tablename__ = "investments"

    # Primary key - composite of exchange and symbol
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)

    # Basic information
    name: Mapped[str] = mapped_column(String(256), nullable=True)
    symbol: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    type: Mapped[str] = mapped_column(
        String(16),
        default=InvestmentType.SHARES.value,
        nullable=False
    )

    # Current price
    live_price: Mapped[float] = mapped_column(Float, default=0.0)

    # Visibility
    visible: Mapped[bool] = mapped_column(Boolean, default=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    purchases: Mapped[list["Purchase"]] = relationship(
        "Purchase",
        back_populates="investment",
        cascade="all, delete-orphan"
    )

    sales: Mapped[list["Sale"]] = relationship(
        "Sale",
        back_populates="investment",
        cascade="all, delete-orphan"
    )

    dividend_payments: Mapped[list["DividendPayment"]] = relationship(
        "DividendPayment",
        back_populates="investment",
        cascade="all, delete-orphan"
    )

    dividend_reinvestments: Mapped[list["DividendReinvestment"]] = relationship(
        "DividendReinvestment",
        back_populates="investment",
        cascade="all, delete-orphan"
    )

    history: Mapped[list["History"]] = relationship(
        "History",
        back_populates="investment",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Investment(key={self.key}, symbol={self.symbol}, name={self.name})>"

    @staticmethod
    def generate_key(exchange: str, symbol: str) -> str:
        """Generate a unique key for an investment."""
        return f"{exchange}-{symbol}"
