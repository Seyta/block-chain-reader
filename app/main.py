import logging
import queue
from src.fetcher import fetch_tip_hash, fetch_block_json
from src.miner import build_coinbase, build_block_header, mine_batch
from src.node_manager import NodeManager
from src.utils import int_to_little_endian
from src.address import bech32_decode

logging.basicConfig(
    filename='/app/data/network.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

myaddress = bech32_decode('bc1q4djqwazqkjmjpqrmz85da6snsz6ctxyhuajjze').hex()
BATCH = 100_000

node = NodeManager()
node.start(num_peers=2)

tip_hash = fetch_tip_hash()
bits = fetch_block_json(tip_hash)['bits']
coinbase = build_coinbase(myaddress)

try:
    header = build_block_header(tip_hash, coinbase, bits)
    nonce = 0
    while True:
        try:
            event = node.new_block_queue.get_nowait()
            tip_hash = event['hash']
            bits = fetch_block_json(tip_hash)['bits']
            coinbase = build_coinbase(myaddress)
            header = build_block_header(tip_hash, coinbase, bits)
            nonce = 0
            print(f"Nouveau bloc détecté !")
        except queue.Empty:
            pass
        correct_nonce, hash = mine_batch(header, nonce, BATCH)
        if correct_nonce is not None :
           print("Nonce trouvé !!")
           node.submit_block(header[:76] + int_to_little_endian(correct_nonce, 4), coinbase)
        else :
            nonce += BATCH
            print(f"Nonce not founds, starting new nonce range {nonce:,} - {nonce + BATCH:,}")
            if nonce >= 0xFFFFFFFF:
                header = build_block_header(tip_hash, coinbase, bits)
                nonce = 0

except KeyboardInterrupt:
    try:
        node.stop()
    except KeyboardInterrupt:
        pass
