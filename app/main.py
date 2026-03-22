from operator import invert

from src.fetcher import fetch_block_hash
from src.fetcher import fetch_raw_block
from src.block import Block
from src.transaction import Transaction
from src.utils import read_varint
from src.pow import check_pow
from src.merkle import merkle_root
from src.script import parse_script
from src.address import hash_to_address
import io

block_raw = fetch_raw_block('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f')
block_raw = fetch_raw_block('00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048')

block_hash = fetch_block_hash(170)
block_raw = fetch_raw_block(block_hash)

block_hash = fetch_block_hash(500000)
block_raw = fetch_raw_block(block_hash)

print(block_raw)
block_stream = io.BytesIO(block_raw)
block = Block.parse(block_stream)

print(block.version)
print(block.timestamp)
print(block.nonce)

transaction_count = read_varint(block_stream)

transactions = []
transaction_ids = []
for i in range(transaction_count):
    transaction = Transaction.parse(block_stream)
    print(transaction.version)
    print(transaction.segwit)
    print(len(transaction.inputs))
    print(len(transaction.outputs))

    transactions.append(transaction)
    transaction_ids.append(bytes.fromhex(transaction.transaction_id())[::-1])

print('Pow')
print(check_pow(block))

merkle = merkle_root(transaction_ids)
print(merkle)
print(block.merkle_root)
print(merkle == block.merkle_root)

print('Address')
for transaction in transactions:
    for output in transaction.outputs:
        script_type, hash_bytes = parse_script(output.script_pubkey)
        print(hash_to_address(script_type, hash_bytes))