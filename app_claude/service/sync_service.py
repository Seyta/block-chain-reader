"""
Synchronises blocks from the Bitcoin node into the database.
"""
import logging

from blockchain.client import BitcoinClient, BitcoinRPCError
from blockchain.parser import parse_block, parse_transaction
from config.settings import Settings
from infrastructure.database import Database
from repository.block_repository import BlockRepository
from repository.transaction_repository import TransactionRepository

logger = logging.getLogger(__name__)


class SyncService:

    def __init__(self, settings: Settings, db: Database) -> None:
        self._client = BitcoinClient(
            host=settings.btc_rpc_host,
            port=settings.btc_rpc_port,
            user=settings.btc_rpc_user,
            password=settings.btc_rpc_password,
        )
        self._blocks = BlockRepository(db)
        self._txs = TransactionRepository(db)

    def run(self) -> None:
        logger.info("Fetching blockchain info...")
        try:
            info = self._client.get_blockchain_info()
            tip = info["blocks"]
            logger.info("Node tip: block #%d", tip)
        except (BitcoinRPCError, Exception) as exc:
            logger.error("Cannot reach Bitcoin node: %s", exc)
            logger.info("Running in offline/stub mode.")
            return

        last_local = self._blocks.find_latest_height() or 0
        logger.info("Local tip: block #%d — syncing %d blocks", last_local, tip - last_local)

        for height in range(last_local + 1, tip + 1):
            self._sync_block(height)

        logger.info("Sync complete.")

    def _sync_block(self, height: int) -> None:
        block_hash = self._client.get_block_hash(height)
        raw_block = self._client.get_block(block_hash, verbosity=2)

        block = parse_block(raw_block)
        self._blocks.save(block)

        for raw_tx in raw_block.get("tx", []):
            tx = parse_transaction(raw_tx, block_hash=block.hash, block_height=block.height)
            self._txs.save(tx)

        logger.info("Synced block #%d (%d txs)", height, block.tx_count)
