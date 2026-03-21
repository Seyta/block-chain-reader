"""
Database connection - uses only stdlib urllib.parse + socket-level psycopg2-free approach.
Note: add psycopg2-binary when ready to install dependencies.
"""
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class Database:
    """
    Thin wrapper around a PostgreSQL connection.
    Connexion réelle via psycopg2 (à ajouter aux dépendances).
    """

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._conn = None
        self._connect()

    def _connect(self) -> None:
        parsed = urlparse(self._dsn)
        logger.info(
            "Connecting to database %s@%s:%s/%s",
            parsed.username,
            parsed.hostname,
            parsed.port,
            parsed.path.lstrip("/"),
        )
        # TODO: import psycopg2 and open the real connection
        # import psycopg2
        # self._conn = psycopg2.connect(self._dsn)
        logger.warning("Database stub: no real connection (psycopg2 not yet installed)")

    def execute(self, query: str, params: tuple = ()) -> None:
        if self._conn is None:
            logger.warning("No DB connection, skipping query.")
            return
        with self._conn.cursor() as cur:
            cur.execute(query, params)
        self._conn.commit()

    def fetchone(self, query: str, params: tuple = ()):
        if self._conn is None:
            return None
        with self._conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()

    def fetchall(self, query: str, params: tuple = ()):
        if self._conn is None:
            return []
        with self._conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

    def close(self) -> None:
        if self._conn:
            self._conn.close()
