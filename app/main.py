from src.display import print_block
from src.fetcher import fetch_block_hash
from src.network import BitcoinNode

height = 0
print(f'getting block height: {height}')
hash = fetch_block_hash(height)

print(f'getting block hash from P2P: {hash}')
node = BitcoinNode('seed.bitcoin.sipa.be')
node.handshake()
block = node.get_block(hash)
print_block(height, block)
node.close()