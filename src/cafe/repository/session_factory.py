"""Engine und die Factory für Sessions konfigurieren."""

from typing import Final

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cafe.config.db import (
    db_connect_args,
    db_log_statements,
    db_url,
)

__all__ = ["Session", "engine"]

# isolation_level= "SERIALIZABLE","REPEATABLE READ","READ COMMITTED","READ UNCOMMITTED"
# Default Isolation Level "READ COMMITTED": Schreibsperren und keine Lesesperren
# pool_size=5
engine: Final = create_engine(
    db_url,
    connect_args=db_connect_args,
    echo=db_log_statements,
)
"""'Engine' für SQLAlchemy, um DB-Verbindungen und Sessions zu erstellen."""

logger.info("Engine fuer SQLAlchemy erzeugt")


Session = sessionmaker(bind=engine, autoflush=False)
"""Factory für Sessions, um generierte SQL-Anweisungen in Transaktionen abzusetzen."""

logger.info("Session-Factory fuer SQLAlchemy erzeugt")
