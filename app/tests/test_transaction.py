import unittest
import io
from src.block import Block

class TransactionTest(unittest.TestCase):

    genesis_block = b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00;\xa3\xed\xfdz{\x12\xb2z\xc7,>gv\x8fa\x7f\xc8\x1b\xc3\x88\x8aQ2:\x9f\xb8\xaaK\x1e^J)\xab_I\xff\xff\x00\x1d\x1d\xac+|\x01\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xffM\x04\xff\xff\x00\x1d\x01\x04EThe Times 03/Jan/2009 Chancellor on brink of second bailout for banks\xff\xff\xff\xff\x01\x00\xf2\x05*\x01\x00\x00\x00CA\x04g\x8a\xfd\xb0\xfeUH'\x19g\xf1\xa6q0\xb7\x10\\\xd6\xa8(\xe09\t\xa6yb\xe0\xea\x1fa\xde\xb6I\xf6\xbc?L\xef8\xc4\xf3U\x04\xe5\x1e\xc1\x12\xde\\8M\xf7\xba\x0b\x8dW\x8aLp+k\xf1\x1d_\xac\x00\x00\x00\x00"

    def test_parse_genesis(self):
        stream = io.BytesIO(self.genesis_block)
        block = Block.parse(stream)
        transaction = block.transactions[0]

        self.assertEqual(transaction.version, 1)
        self.assertEqual(transaction.segwit, False)
        self.assertEqual(len(transaction.inputs), 1)
        self.assertEqual(len(transaction.outputs), 1)

    def test_transaction_id(self):
        stream = io.BytesIO(self.genesis_block)
        block = Block.parse(stream)
        transaction = block.transactions[0]

        self.assertEqual(
            '4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b',
            transaction.transaction_id()
        )

    def test_output_amount(self):
        stream = io.BytesIO(self.genesis_block)
        block = Block.parse(stream)
        transaction = block.transactions[0]

        self.assertEqual(
            5000000000,
            transaction.outputs[0].amount
        )

    def test_output_prev_transaction(self):
        stream = io.BytesIO(self.genesis_block)
        block = Block.parse(stream)
        transaction = block.transactions[0]

        expected = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        expected += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.assertEqual(expected, transaction.inputs[0].prev_tx)

    def test_segwit_false(self):
        stream = io.BytesIO(self.genesis_block)
        block = Block.parse(stream)
        transaction = block.transactions[0]

        self.assertFalse(transaction.segwit)