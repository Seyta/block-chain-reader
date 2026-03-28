from src.utils import little_endian_to_int
from src.utils import int_to_little_endian
from src.utils import int_to_varint
from src.utils import read_varint
from src.utils import hash256

class Transaction:
    def __init__(self, version, inputs, outputs, locktime, segwit):
        self.version = version
        self.inputs = inputs
        self.outputs = outputs
        self.locktime = locktime
        self.segwit = segwit

    @classmethod
    def parse(cls, stream):
        version_bytes = stream.read(4)
        version = little_endian_to_int(version_bytes)
        raw_segwit = stream.read(2)
        if raw_segwit == b'\x00\x01':
            bool_segwit = True
        else:
            bool_segwit = False
            stream.seek(stream.tell() - 2)
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
        return cls(version, inputs, outputs, locktime, bool_segwit)

    def transaction_id(self):
        hash = int_to_little_endian(self.version, 4)

        hash += int_to_varint(len(self.inputs))
        for input in self.inputs:
            hash += input.prev_tx
            hash += int_to_little_endian(input.prev_index, 4)
            hash += int_to_varint(len(input.script_sig))
            hash += input.script_sig
            hash += int_to_little_endian(input.sequence, 4)

        hash += int_to_varint(len(self.outputs))
        for output in self.outputs:
            hash += int_to_little_endian(output.amount, 8)
            hash += int_to_varint(len(output.script_pubkey))
            hash += output.script_pubkey

        hash += int_to_little_endian(self.locktime, 4)

        hash = hash256(hash)
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

    def to_bytes(self):
        return (self.prev_tx + int_to_little_endian(self.prev_index, 4) + int_to_varint(len(self.script_sig))
                + self.script_sig + int_to_little_endian(self.sequence, 4))

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

    def to_bytes(self):
        return int_to_little_endian(self.amount, 8) + int_to_varint(len(self.script_pubkey)) + self.script_pubkey