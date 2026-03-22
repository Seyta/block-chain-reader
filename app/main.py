import io

from src.block import Block
from src.display import print_block
from src.fetcher import fetch_block_hash
from src.fetcher import fetch_raw_block

#block_raw = fetch_raw_block('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f')
#block_raw = fetch_raw_block('00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048')

block_hash = fetch_block_hash(800000)
block_raw = fetch_raw_block(block_hash)

block_stream = io.BytesIO(block_raw)
block = Block.parse(block_stream)

print_block(800000, block)