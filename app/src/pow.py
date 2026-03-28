from src.utils import int_to_little_endian
from src.utils import little_endian_to_int

def bits_to_target(bits):
    target_bits = int_to_little_endian(bits, 4)
    exposant = target_bits[3]
    coefficient = little_endian_to_int(target_bits[:3])
    return coefficient * 256 ** (exposant - 3)

def check_pow(block):
    int_hash = int(block.hash(), 16)
    target = bits_to_target(block.bits)

    return int_hash < target