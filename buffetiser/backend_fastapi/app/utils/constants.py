"""
Application constants and enumerations.
"""
from enum import Enum


class InvestmentType(str, Enum):
    """Types of investments."""
    SHARES = "Shares"
    CRYPTO = "Crypto"


class Exchange(str, Enum):
    """Global stock exchanges."""
    XASX = "ASX"  # Australian Securities Exchange
    XAMS = "AMS"  # Amsterdam
    XBOM = "BOM"  # Bombay
    XBRU = "BRU"  # Brussels
    XFRA = "FRA"  # Frankfurt
    XHKG = "HKG"  # Hong Kong
    XJPX = "JPX"  # Japan Exchange
    XKOS = "KOS"  # Korea
    XLIS = "LIS"  # Lisbon
    XLON = "LON"  # London
    XMIL = "MIL"  # Milan
    XMSM = "MSM"  # Moscow
    XNAS = "NAS"  # NASDAQ
    XNSE = "NSE"  # National Stock Exchange India
    XNYS = "NYS"  # New York Stock Exchange
    XOSL = "OSL"  # Oslo
    XSAU = "SAU"  # Saudi Arabia
    XSHE = "SHE"  # Shenzhen
    XSHG = "SHG"  # Shanghai
    XSWX = "SWX"  # Swiss Exchange
    XTAI = "TAI"  # Taiwan
    XTSE = "TSE"  # Toronto


class Platform(str, Enum):
    """Trading platforms."""
    CMC = "CMC"
    LINK = "LINK"
    BOARDROOM = "BOARDROOM"
    DIRECT = "DIRECT"
    IPO = "IPO"


class Currency(str, Enum):
    """Supported currencies."""
    AUD = "AUD"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CNY = "CNY"


class TransactionType(str, Enum):
    """Transaction types for reporting."""
    PURCHASE = "purchase"
    SALE = "sale"
    DIVIDEND_PAYMENT = "dividend_payment"
    DIVIDEND_REINVESTMENT = "dividend_reinvestment"


class TaxMethod(str, Enum):
    """Methods for calculating capital gains tax."""
    AVERAGE_COST = "average_cost"
    SPECIFIC_PARCEL = "specific_parcel"  # User selects which parcel to sell
    FIFO = "fifo"  # First In First Out


class CGTTreatment(str, Enum):
    """Capital Gains Tax treatment for Australian tax."""
    SHORT_TERM = "short_term"  # Held < 12 months
    LONG_TERM = "long_term"  # Held >= 12 months, eligible for 50% CGT discount
