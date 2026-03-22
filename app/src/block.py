from src.utils import little_endian_to_int
from src.utils import int_to_little_endian
from src.utils import read_varint
from src.utils import hash256
from src.transaction import Transaction
from src.merkle import merkle_root
from src.pow import check_pow

class Block:
    def __init__(self, version, prev_block, merkle_root, timestamp, bits, nonce, transactions=None, transaction_ids=None):
        self.version = version
        self.prev_block = prev_block
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce
        self.transactions = transactions if transactions is not None else []
        self.transaction_ids = transaction_ids if transaction_ids is not None else []

    @classmethod
    def parse(cls, stream):
        #Block headers 80 bytes
        version = little_endian_to_int(stream.read(4))
        prev_block = stream.read(32)
        merkle_root = stream.read(32)
        timestamp = little_endian_to_int(stream.read(4))
        bits = little_endian_to_int(stream.read(4))
        nonce = little_endian_to_int(stream.read(4))

        # number of transactions
        transaction_count = read_varint(stream)
        transactions = []
        transaction_ids = []
        for i in range(transaction_count):
            transaction = Transaction.parse(stream)
            transactions.append(transaction)
            transaction_ids.append(bytes.fromhex(transaction.transaction_id())[::-1])

        return cls(version, prev_block, merkle_root, timestamp, bits, nonce, transactions, transaction_ids)

    def hash(self):
        hash = hash256(
            int_to_little_endian(self.version, 4)
            + self.prev_block
            + self.merkle_root
            + int_to_little_endian(self.timestamp, 4)
            + int_to_little_endian(self.bits, 4)
            + int_to_little_endian(self.nonce, 4)
        )
        inverted = hash[::-1].hex()
        return inverted

    def check_merkle_root(self):
        return merkle_root(self.transaction_ids)

    def check_pow(self):
        return check_pow(self)