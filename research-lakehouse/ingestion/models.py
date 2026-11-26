from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# normalize market event types across equities and crypto
class EventType(str, Enum):
    NEW_LIMIT_ORDER = "NEW_LIMIT_ORDER"
    CANCEL = "CANCEL"
    DELETE = "DELETE"
    EXECUTE = "EXECUTE"
    HIDDEN_EXECUTE = "HIDDEN_EXECUTE"
    TRADE = "TRADE"
    BOOK_SNAPSHOT = "BOOK_SNAPSHOT"


class OrderSide(str, Enum):
    BID = "BID"
    ASK = "ASK"
    UNKNOWN = "UNKNOWN"


class Venue(str, Enum):
    LOBSTER_NASDAQ = "LOBSTER_NASDAQ"
    BINANCE_SPOT = "BINANCE_SPOT"


# make it immutable
@dataclass(frozen=True)
class MarketEvent:
    symbol: str
    exchange_time_ns: int 
    ingestion_time: datetime 
    event_type: EventType
    order_id: int
    side: OrderSide
    price: float
    quantity: float
