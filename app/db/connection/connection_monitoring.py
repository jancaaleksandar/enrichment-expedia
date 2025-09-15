from typing import Any

from sqlalchemy import Engine, event
from sqlalchemy.pool.base import ConnectionPoolEntry, PoolProxiedConnection


def setup_connection_monitoring(engine: Engine) -> None:
    """
    Set up event listeners to track connection usage.
    """
    connection_count = 0

    @event.listens_for(engine, "checkout")
    def receive_checkout(
        dbapi_connection: Any,
        connection_record: ConnectionPoolEntry,
        connection_proxy: PoolProxiedConnection,
    ) -> None:  # pyright: ignore[reportUnusedFunction]
        nonlocal connection_count
        connection_count += 1
        print(f"Connection checkout: Active connections: {connection_count}")

    @event.listens_for(engine, "checkin")
    def receive_checkin(
        dbapi_connection: Any,
        connection_record: ConnectionPoolEntry,
    ) -> None:  # pyright: ignore[reportUnusedFunction]
        nonlocal connection_count
        connection_count -= 1
        print(f"Connection checkin: Active connections: {connection_count}")

    # Mark nested listener functions as used for static analyzers/linters
    _ = (receive_checkout, receive_checkin)
