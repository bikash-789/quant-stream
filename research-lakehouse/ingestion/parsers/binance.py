import csv
from datetime import datetime, timezone
import logging
from typing import Iterable, Iterator

from ingestion.models import EventType, MarketEvent, OrderSide, Venue
from ingestion.protocols import IEventParser

logger = logging.getLogger("BinanceParser")


class BinanceTradesParser(IEventParser):
    @property
    def supported_venue(self) -> Venue:
        return Venue.BINANCE_SPOT

    def parse(
        self,
        stream: Iterable[str],
        symbol: str,
        date_anchor: datetime,
    ) -> Iterator[MarketEvent]:
    
        now_utc = datetime.now(timezone.utc)
        reader = csv.reader(stream)

        for row_num, row in enumerate(reader, start=1):
            if not row or len(row) < 7:
                continue

            try:
                trade_id = int(row[0])
                price = float(row[1])
                qty = float(row[2])
                time_val = int(row[4])
                # convert milliseconds -> nanoseconds
                time_ns = time_val * 1_000_000
                is_buyer_maker = str(row[5]).strip().lower() == "true"
            except (ValueError, IndexError) as e:
                logger.warning(f"Skipping malformed data in Binance row {row_num}: {row} (error: {e})")
                continue

            side = OrderSide.ASK if is_buyer_maker else OrderSide.BID

            yield MarketEvent(
                symbol=symbol,
                exchange_time_ns=time_ns,
                ingestion_time=now_utc,
                event_type=EventType.TRADE,
                order_id=trade_id,
                side=side,
                price=price,
                quantity=qty,
            )

