import json
import logging

from infrastructure.database import Database
from model.transaction import Transaction

logger = logging.getLogger(__name__)


class TransactionRepository:

    def __init__(self, db: Database) -> None:
        self._db = db

    def find_by_txid(self, txid: str) -> Transaction | None:
        row = self._db.fetchone(
            "SELECT txid, block_hash, block_height, version, locktime, size, weight, fee, raw"
            " FROM transactions WHERE txid = %s",
            (txid,),
        )
        if row is None:
            return None
        return Transaction(*row[:8], raw=row[8] or {})

    def save(self, tx: Transaction) -> None:
        self._db.execute(
            """
            INSERT INTO transactions (txid, block_hash, block_height, version, locktime, size, weight, fee, raw)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (txid) DO NOTHING
            """,
            (
                tx.txid,
                tx.block_hash,
                tx.block_height,
                tx.version,
                tx.locktime,
                tx.size,
                tx.weight,
                tx.fee,
                json.dumps(tx.raw),
            ),
        )
        logger.debug("Saved tx %s", tx.txid)
