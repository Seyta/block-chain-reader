from src.utils import little_endian_to_int


class Block:
    def __init__(self, version, prev_block, merkle_root, timestamp, bits, nonce):
        self.version = version
        self.prev_block = prev_block
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce

    @classmethod
    def parse(cls, stream):
        version = little_endian_to_int(stream.read(4))
        prev_block = stream.read(32)
        merkle_root = stream.read(32)
        timestamp = little_endian_to_int(stream.read(4))
        bits = little_endian_to_int(stream.read(4))
        nonce = little_endian_to_int(stream.read(4))
        return cls(version, prev_block, merkle_root, timestamp, bits, nonce)