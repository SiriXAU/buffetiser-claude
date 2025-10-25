"""
Transaction models for purchases and sales.
"""
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.constants import Currency, Exchange, Platform

if TYPE_CHECKING:
    from app.models.investment import Investment


class Purchase(Base):
    """
    Records a purchase of an investment.

    Multiple purchases can be made on the same day, differentiated by trade_count.
    """

    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Foreign key to investment
    investment_id: Mapped[int] = mapped_column(
        ForeignKey("investments.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Transaction details
    units: Mapped[float] = mapped_column(Float, nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=False)
    fee: Mapped[float] = mapped_column(Float, default=0.0)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    trade_count: Mapped[int] = mapped_column(Integer, nullable=False)

    # Metadata
    currency: Mapped[str] = mapped_column(String(5), default=Currency.AUD.value)
    exchange: Mapped[str] = mapped_column(String(4), default=Exchange.XASX.value)
    platform: Mapped[str] = mapped_column(String(128), default=Platform.CMC.value)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationship
    investment: Mapped["Investment"] = relationship("Investment", back_populates="purchases")

    # Tax parcels created from this purchase
    tax_parcels: Mapped[list["TaxParcel"]] = relationship(
        "TaxParcel",
        back_populates="purchase",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("investment_id", "date", "trade_count", name="uq_purchase_date_trade"),
    )

    def __repr__(self) -> str:
        return f"<Purchase(id={self.id}, units={self.units}, price={self.price_per_unit}, date={self.date})>"

    @property
    def total_cost(self) -> float:
        """Total cost including fees."""
        return (self.units * self.price_per_unit) + self.fee

    @property
    def cost_base_per_unit(self) -> float:
        """Cost base per unit including fees."""
        if self.units == 0:
            return 0
        return self.total_cost / self.units


class Sale(Base):
    """
    Records a sale of an investment.

    Multiple sales can be made on the same day, differentiated by trade_count.
    """

    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Foreign key to investment
    investment_id: Mapped[int] = mapped_column(
        ForeignKey("investments.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Transaction details
    units: Mapped[float] = mapped_column(Float, nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=False)
    fee: Mapped[float] = mapped_column(Float, default=0.0)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    trade_count: Mapped[int] = mapped_column(Integer, nullable=False)

    # Metadata
    currency: Mapped[str] = mapped_column(String(5), default=Currency.AUD.value)
    exchange: Mapped[str] = mapped_column(String(4), default=Exchange.XASX.value)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationship
    investment: Mapped["Investment"] = relationship("Investment", back_populates="sales")

    # Tax parcel allocations for this sale
    tax_parcel_allocations: Mapped[list["TaxParcelAllocation"]] = relationship(
        "TaxParcelAllocation",
        back_populates="sale",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("investment_id", "date", "trade_count", name="uq_sale_date_trade"),
    )

    def __repr__(self) -> str:
        return f"<Sale(id={self.id}, units={self.units}, price={self.price_per_unit}, date={self.date})>"

    @property
    def total_proceeds(self) -> float:
        """Total proceeds after fees."""
        return (self.units * self.price_per_unit) - self.fee

    @property
    def proceeds_per_unit(self) -> float:
        """Proceeds per unit after fees."""
        if self.units == 0:
            return 0
        return self.total_proceeds / self.units


class TaxParcel(Base):
    """
    Represents an individual tax parcel for CGT tracking.

    Each purchase creates one or more parcels. When a sale occurs,
    the user can select which parcels to sell, enabling specific identification
    for tax optimization.
    """

    __tablename__ = "tax_parcels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Foreign key to investment
    investment_id: Mapped[int] = mapped_column(
        ForeignKey("investments.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Foreign key to purchase (optional, as reinvestments can also create parcels)
    purchase_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("purchases.id", ondelete="SET NULL"),
        nullable=True
    )

    # Parcel details
    acquisition_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    units_acquired: Mapped[float] = mapped_column(Float, nullable=False)
    units_remaining: Mapped[float] = mapped_column(Float, nullable=False)
    cost_base_per_unit: Mapped[float] = mapped_column(Float, nullable=False)
    total_cost_base: Mapped[float] = mapped_column(Float, nullable=False)

    # Parcel metadata
    description: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    investment: Mapped["Investment"] = relationship("Investment")
    purchase: Mapped[Optional["Purchase"]] = relationship("Purchase", back_populates="tax_parcels")
    allocations: Mapped[list["TaxParcelAllocation"]] = relationship(
        "TaxParcelAllocation",
        back_populates="parcel",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<TaxParcel(id={self.id}, date={self.acquisition_date}, "
            f"units_remaining={self.units_remaining}/{self.units_acquired})>"
        )

    @property
    def is_fully_sold(self) -> bool:
        """Check if all units have been sold."""
        return self.units_remaining <= 0

    @property
    def percentage_remaining(self) -> float:
        """Percentage of original units still held."""
        if self.units_acquired == 0:
            return 0
        return (self.units_remaining / self.units_acquired) * 100


class TaxParcelAllocation(Base):
    """
    Links a sale to specific tax parcels, tracking which parcels were sold.

    This enables specific parcel identification for CGT calculations.
    """

    __tablename__ = "tax_parcel_allocations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Foreign keys
    sale_id: Mapped[int] = mapped_column(
        ForeignKey("sales.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    parcel_id: Mapped[int] = mapped_column(
        ForeignKey("tax_parcels.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Allocation details
    units_sold: Mapped[float] = mapped_column(Float, nullable=False)
    cost_base: Mapped[float] = mapped_column(Float, nullable=False)  # Total cost base for units sold
    proceeds: Mapped[float] = mapped_column(Float, nullable=False)  # Proceeds from this allocation

    # Calculated CGT
    capital_gain: Mapped[float] = mapped_column(Float, nullable=False)
    holding_period_days: Mapped[int] = mapped_column(Integer, nullable=False)
    cgt_discount_applied: Mapped[bool] = mapped_column(default=False)
    discounted_capital_gain: Mapped[float] = mapped_column(Float, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships
    sale: Mapped["Sale"] = relationship("Sale", back_populates="tax_parcel_allocations")
    parcel: Mapped["TaxParcel"] = relationship("TaxParcel", back_populates="allocations")

    def __repr__(self) -> str:
        return (
            f"<TaxParcelAllocation(id={self.id}, units={self.units_sold}, "
            f"capital_gain={self.capital_gain})>"
        )
