from src.utils import int_to_little_endian
from src.utils import little_endian_to_int

def check_pow(block):
    int_hash = int(block.hash(), 16)
    target_bits = int_to_little_endian(block.bits, 4)
    exposant = target_bits[3]
    coefficient = little_endian_to_int(target_bits[:3])
    target = coefficient * 256 ** (exposant - 3)

    return int_hash < target