from typing import Any, Dict, Iterable, List
from ingestion.models import MarketEvent
from ingestion.protocols import IEventSink


class MemoryEventSink(IEventSink):
    def __init__(self):
        self._events: List[MarketEvent] = []

    def write(self, events: Iterable[MarketEvent]) -> int:
        initial_len = len(self._events)
        self._events.extend(events)
        return len(self._events) - initial_len

    @property
    def events(self) -> List[MarketEvent]:
        return self._events

    def clear(self) -> None:
        self._events.clear()

    def to_columnar_dict(self) -> Dict[str, List[Any]]:
        return {
            "symbol": [e.symbol for e in self._events],
            "exchange_time_ns": [e.exchange_time_ns for e in self._events],
            "ingestion_time": [e.ingestion_time for e in self._events],
            "event_type": [e.event_type.value for e in self._events],
            "order_id": [e.order_id for e in self._events],
            "side": [e.side.value for e in self._events],
            "price": [e.price for e in self._events],
            "quantity": [e.quantity for e in self._events],
        }
