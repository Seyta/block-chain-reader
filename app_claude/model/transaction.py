from dataclasses import dataclass, field
from typing import Any


@dataclass
class Transaction:
    txid: str
    block_hash: str | None
    block_height: int | None
    version: int
    locktime: int
    size: int | None = None
    weight: int | None = None
    fee: int | None = None        # satoshis
    raw: dict[str, Any] = field(default_factory=dict)
