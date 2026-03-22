from operator import invert

from src.fetcher import fetch_block_hash
from src.fetcher import fetch_raw_block
from src.block import Block
from src.script import parse_script
from src.address import hash_to_address
import io

block_raw = fetch_raw_block('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f')
block_raw = fetch_raw_block('00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048')

block_hash = fetch_block_hash(170)
block_raw = fetch_raw_block(block_hash)

block_hash = fetch_block_hash(500000)
block_raw = fetch_raw_block(block_hash)

block_hash = fetch_block_hash(800000)
block_raw = fetch_raw_block(block_hash)

block_stream = io.BytesIO(block_raw)
block = Block.parse(block_stream)

print(block.version)
print(block.timestamp)
print(block.nonce)

print('Checks')
print(f'Pow {block.check_pow()}')
print(f'Merkle {block.check_merkle_root()}')

print('Address')
for transaction in block.transactions:
    for output in transaction.outputs:
        script_type, hash_bytes = parse_script(output.script_pubkey)
        address = (hash_to_address(script_type, hash_bytes))
        amount = output.amount
        print(f'{address} - {amount / 100_000_000} BTC')