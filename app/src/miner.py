import time

from src.transaction import TransactionInput
from src.transaction import TransactionOutput
from src.utils import hash256, little_endian_to_int
from src.utils import int_to_little_endian
from src.utils import int_to_varint
from src.pow import bits_to_target


def build_coinbase(address):
    full = 0xFFFFFFFF
    sig = b'hello there'
    transaction_input = TransactionInput(
        b'\x00' * 32,
        full,
        sig,
        full
    )

    transaction_output = TransactionOutput(
        312500000,
        b'\x76\xa9\x14' + bytes.fromhex('62e907b15cbf27d5425399ebf6f0fb50ebb88f18') + b'\x88\xac' #hash160 of 1A1zP1eP5QGefi2DMPTfTL5SLmv7Divfna (satoshi)
    )

    version = int_to_little_endian(1, 4)
    truc = int_to_varint(1)
    locktime = int_to_little_endian(0, 4)

    return version + truc + transaction_input.to_bytes() + truc + transaction_output.to_bytes() + locktime

def build_block_header(prev_hash, coinbase_bytes, bits):
    version = int_to_little_endian(0x20000000, 4)
    prev_hash = bytes.fromhex(prev_hash)[::-1]
    merkle_root = hash256(coinbase_bytes)[::-1]
    timestamp = int_to_little_endian(int(time.time()), 4)
    bits = int_to_little_endian(bits, 4)
    nonce = int_to_little_endian(0, 4)

    return version + prev_hash + merkle_root + timestamp + bits + nonce

def mine(header_bytes, target, nonce_range):
    target = bits_to_target(little_endian_to_int(header_bytes[72:76]))
    for nonce in range(nonce_range):
        header_candidate = header_bytes[:76] + int_to_little_endian(nonce, 4)
        hash = hash256(header_candidate)
        hash_int = int.from_bytes(hash, 'little')
        if hash_int < target:
            return nonce, hash

    return None, None

def mine_batch(header_bytes, start_nonce, nonce_count):
    target = bits_to_target(little_endian_to_int(header_bytes[72:76]))
    for nonce in range(start_nonce, start_nonce+nonce_count):
        header_candidate = header_bytes[:76] + int_to_little_endian(nonce, 4)
        hash = hash256(header_candidate)
        hash_int = int.from_bytes(hash, 'little')
        if hash_int < target:
            return nonce, hash

    return None, None

