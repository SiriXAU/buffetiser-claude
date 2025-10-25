"""
Pydantic schemas for request/response validation.
"""
from app.schemas.dividend import (
    DividendPaymentCreate,
    DividendPaymentResponse,
    DividendReinvestmentCreate,
    DividendReinvestmentResponse,
)
from app.schemas.investment import (
    InvestmentCreate,
    InvestmentDetail,
    InvestmentResponse,
    InvestmentUpdate,
)
from app.schemas.tax import (
    CGTEvent,
    CGTSummary,
    TaxParcelCreate,
    TaxParcelResponse,
    TaxReportResponse,
)
from app.schemas.transaction import (
    PurchaseCreate,
    PurchaseResponse,
    SaleCreate,
    SaleResponse,
    SaleWithParcelSelection,
)

__all__ = [
    "InvestmentCreate",
    "InvestmentUpdate",
    "InvestmentResponse",
    "InvestmentDetail",
    "PurchaseCreate",
    "PurchaseResponse",
    "SaleCreate",
    "SaleResponse",
    "SaleWithParcelSelection",
    "DividendPaymentCreate",
    "DividendPaymentResponse",
    "DividendReinvestmentCreate",
    "DividendReinvestmentResponse",
    "TaxParcelCreate",
    "TaxParcelResponse",
    "CGTEvent",
    "CGTSummary",
    "TaxReportResponse",
]
