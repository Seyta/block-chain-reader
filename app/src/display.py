from src.address import hash_to_address
from src.block import Block
from src.script import parse_script
from src.transaction import Transaction
from datetime import datetime

def print_transaction(transaction: Transaction) -> None:
    print(f"TXID : {transaction.transaction_id()}")
    print('Inputs : ')
    for i, input in enumerate(transaction.inputs):
        print(f"  [{i}] : {input.prev_tx.hex()}")

    print('Outputs : ')
    for i, output in enumerate(transaction.outputs):
        script_type, hash_bytes = parse_script(output.script_pubkey)
        address = (hash_to_address(script_type, hash_bytes))
        print(f"  [{i}] : {output.amount / 100_000_000:.8f} BTC -> {address}")

    print('---')

def print_block(bloc_height: int, block: Block) -> None:
    date = datetime.fromtimestamp(block.timestamp)
    print('Bloc :')
    print(f'=== BLOC #{bloc_height} ===')
    print(f'Hash: {block.hash()}')
    print(f'Timestamp : {date}')
    print(f'Version : {block.version}')
    print(f'PoW : {block.check_pow()}')
    print(f'Merkle : {block.check_merkle_root() == block.merkle_root}')
    print(f'Transactions : {len(block.transactions)}')

    print('Par transaction :')
    for transaction in block.transactions:
        print_transaction(transaction)