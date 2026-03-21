import hashlib

def sha256(string):
    return hashlib.sha256(string).digest()

def hash256(string):
    return sha256(sha256(string))

def little_endian_to_int(string):
    return int.from_bytes(string, byteorder='little', signed=False)

def int_to_little_endian(integer, length):
    return int.to_bytes(integer, length=length, byteorder='little', signed=False)

def read_varint(stream):
    integer = little_endian_to_int(stream.read(1))
    if integer < 0xFD :
        return integer
    elif integer == 0xFD:
        return little_endian_to_int(stream.read(2))
    elif integer == 0xFE:
        return little_endian_to_int(stream.read(4))
    elif integer == 0xFF:
        return little_endian_to_int(stream.read(8))