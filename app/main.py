from operator import invert

from src.fetcher import fetch_raw_block
from src.block import Block
from src.transaction import Transaction
from src.utils import read_varint
from src.pow import check_pow
from src.merkle import merkle_root
import io

block_raw = fetch_raw_block('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f')
print(block_raw)
block_stream = io.BytesIO(block_raw)
block = Block.parse(block_stream)

print(block.version)
print(block.timestamp)
print(block.nonce)

transaction_count = read_varint(block_stream)

transaction = Transaction.parse(block_stream)
print(transaction.version)
print(transaction.segwit)
print(len(transaction.inputs))
print(len(transaction.outputs))

print(block.hash())
print(transaction.transaction_id())

print(check_pow(block))

transaction_id = bytes.fromhex(transaction.transaction_id())[::-1]
merkle = merkle_root([transaction_id])

print(merkle)
print(block.merkle_root)
print(merkle == block.merkle_root)