from dataclasses import dataclass, field
from typing import Any


@dataclass
class Block:
    hash: str
    height: int
    version: int
    prev_hash: str | None
    merkle_root: str
    timestamp: int
    bits: str
    nonce: int
    tx_count: int
    size: int | None = None
    weight: int | None = None
    raw: dict[str, Any] = field(default_factory=dict)
