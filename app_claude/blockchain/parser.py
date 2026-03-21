"""
Raw block / transaction parsing helpers.
"""
from model.block import Block
from model.transaction import Transaction


def parse_block(raw: dict) -> Block:
    return Block(
        hash=raw["hash"],
        height=raw["height"],
        version=raw["version"],
        prev_hash=raw.get("previousblockhash"),
        merkle_root=raw["merkleroot"],
        timestamp=raw["time"],
        bits=raw["bits"],
        nonce=raw["nonce"],
        tx_count=raw["nTx"],
        size=raw.get("size"),
        weight=raw.get("weight"),
        raw=raw,
    )


def parse_transaction(raw: dict, block_hash: str | None = None, block_height: int | None = None) -> Transaction:
    return Transaction(
        txid=raw["txid"],
        block_hash=block_hash,
        block_height=block_height,
        version=raw["version"],
        locktime=raw["locktime"],
        size=raw.get("size"),
        weight=raw.get("weight"),
        fee=raw.get("fee"),
        raw=raw,
    )
