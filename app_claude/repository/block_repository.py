import json
import logging

from infrastructure.database import Database
from model.block import Block

logger = logging.getLogger(__name__)


class BlockRepository:

    def __init__(self, db: Database) -> None:
        self._db = db

    def find_by_hash(self, block_hash: str) -> Block | None:
        row = self._db.fetchone(
            "SELECT hash, height, version, prev_hash, merkle_root, timestamp, bits, nonce, tx_count, size, weight, raw"
            " FROM blocks WHERE hash = %s",
            (block_hash,),
        )
        if row is None:
            return None
        return Block(*row[:11], raw=row[11] or {})

    def find_latest_height(self) -> int | None:
        row = self._db.fetchone("SELECT MAX(height) FROM blocks")
        return row[0] if row else None

    def save(self, block: Block) -> None:
        self._db.execute(
            """
            INSERT INTO blocks (hash, height, version, prev_hash, merkle_root, timestamp, bits, nonce, tx_count, size, weight, raw)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (hash) DO NOTHING
            """,
            (
                block.hash,
                block.height,
                block.version,
                block.prev_hash,
                block.merkle_root,
                block.timestamp,
                block.bits,
                block.nonce,
                block.tx_count,
                block.size,
                block.weight,
                json.dumps(block.raw),
            ),
        )
        logger.debug("Saved block #%d %s", block.height, block.hash)
