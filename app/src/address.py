from src.utils import hash256

def base58check_encode(payload):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    checksum = hash256(payload)[:4]
    data = payload + checksum

    integer = int.from_bytes(data, byteorder='big')
    result = ''
    while integer > 0 :
        result += alphabet[integer % 58]
        integer //= 58
    result = result[::-1]

    for byte in data :
        if byte == 0 :
            result = '1' + result
        else :
            break

    return result

def hash_to_address(script_type, hash_bytes):
    if script_type == 'P2PKH' :
        return base58check_encode(b'\x00' + hash_bytes)
    elif script_type == 'P2SH' :
        return base58check_encode(b'\x05' + hash_bytes)
    else:
        return 'unknown'