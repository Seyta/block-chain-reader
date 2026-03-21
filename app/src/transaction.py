from src.utils import little_endian_to_int
from src.utils import read_varint
from src.utils import hash256
import io

class Transaction:
    def __init__(self, version, inputs, outputs, locktime, segwit, raw):
        self.version = version
        self.inputs = inputs
        self.outputs = outputs
        self.locktime = locktime
        self.segwit = segwit
        self.raw = raw

    @classmethod
    def parse(cls, stream):
        beginning = stream.tell()
        version_bytes = stream.read(4)
        version = little_endian_to_int(version_bytes)
        raw_segwit = stream.read(2)
        if raw_segwit == b'\x00\x01':
            bool_segwit = True
        else:
            bool_segwit = False
            stream = io.BytesIO(version_bytes + raw_segwit + stream.read())
            stream.read(4)
            beginning = 0
        count_inputs = read_varint(stream)
        inputs = []
        for i in range(count_inputs):
            inputs.append(TransactionInput.parse(stream))
        count_outputs = read_varint(stream)
        outputs = []
        for i in range(count_outputs):
            outputs.append(TransactionOutput.parse(stream))
        if (bool_segwit):
            for i in range(count_inputs):
                count_items = read_varint(stream)
                for j in range(count_items):
                    item_size = read_varint(stream)
                    item = stream.read(item_size)
        locktime = little_endian_to_int(stream.read(4))
        end = stream.tell()
        stream.seek(beginning)
        raw = stream.read(end - beginning)
        return cls(version, inputs, outputs, locktime, bool_segwit, raw)

    def transaction_id(self):
        hash = hash256(self.raw)
        inverted = hash[::-1].hex()
        return inverted

class TransactionInput:
    def __init__(self, prev_tx, prev_index, script_sig, sequence):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        self.script_sig = script_sig
        self.sequence = sequence

    @classmethod
    def parse(cls, stream):
        prev_tx = stream.read(32)
        prev_index = little_endian_to_int(stream.read(4))
        script_sig = read_varint(stream)
        script_sig = stream.read(script_sig)
        sequence = little_endian_to_int(stream.read(4))
        return cls(prev_tx, prev_index, script_sig, sequence)

class TransactionOutput:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    @classmethod
    def parse(cls, stream):
        amount = little_endian_to_int(stream.read(8))
        script_pubkey = read_varint(stream)
        script_pubkey = stream.read(script_pubkey)
        return cls(amount, script_pubkey)