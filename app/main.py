from src.display import print_block
from src.fetcher import fetch_block_hash
from src.fetcher import fetch_block_json
from src.fetcher import fetch_tip_hash
from src.network import BitcoinNode
from src.miner import build_coinbase, mine
from src.miner import build_block_header

#height = 0
#print(f'getting block height: {height}')
#hash = fetch_block_hash(height)
#
#print(f'getting block hash from P2P: {hash}')
#node = BitcoinNode('seed.bitcoin.sipa.be')
#node.handshake()
#block = node.get_block(hash)
#print_block(height, block)
#node.close()

tip_hash = fetch_tip_hash()
json_block = fetch_block_json(tip_hash)
bits = json_block['bits']

coinbase = build_coinbase(None)
print(coinbase.hex())

header = build_block_header(tip_hash, coinbase, bits)
print(header.hex())

nonce, hash = mine(header, None, 100_000)
if nonce is None :
    print("Rien trouvé sur 100 000 nonces")
    exit(0)

print(nonce, hash.hex())

#node = BitcoinNode('seed.bitcoin.sipa.be')
#node.handshake()
#node.submit_block(header, coinbase)
#node.close()