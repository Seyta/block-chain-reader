"""
BTC Reader - Entry point
"""
import sys
import logging

from config.settings import Settings
from infrastructure.database import Database
from service.sync_service import SyncService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("BTC Reader starting...")

    settings = Settings.from_env()
    db = Database(settings.db_dsn)

    sync = SyncService(settings, db)
    sync.run()


if __name__ == "__main__":
    main()
