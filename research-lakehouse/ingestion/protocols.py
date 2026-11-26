from datetime import datetime
from typing import ContextManager, Iterable, Iterator, Protocol, runtime_checkable

from ingestion.models import MarketEvent, Venue
 

@runtime_checkable
class IDataSource(Protocol):
    def open_stream(self) -> ContextManager[Iterable[str]]:
        ...


@runtime_checkable
class IEventParser(Protocol):
    @property
    def supported_venue(self) -> Venue:
        ...

    def parse(
        self,
        stream: Iterable[str],
        symbol: str,
        date_anchor: datetime,
    ) -> Iterator[MarketEvent]:
        ...


@runtime_checkable
class IEventSink(Protocol):
    def write(self, events: Iterable[MarketEvent]) -> int:
        ...
