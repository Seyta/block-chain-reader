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

def convertbits(data, frombits, tobits):
    acc = 0
    bits = 0
    result = []

    for byte in data :
        acc = (acc << frombits) | byte # concatenate bytes
        bits += frombits # count bytes
        while bits >= tobits:
            bits -= tobits
            result.append((acc >> bits) & ((1 << tobits) - 1))  # extrait tobits bits

    return result

def bech32_polymod(values):
    chk = 1
    for value in values :
        b = chk >> 25
        chk = ((chk & 0x1ffffff) << 5) ^ value
        for i, c in enumerate([0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]) :
            if (b >> i) & 1 :
                chk ^= c
    return chk

def bech32_create_checksum(hrp, data):
    values = [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp] + data + [0, 0, 0, 0, 0, 0]
    polymod = bech32_polymod(values) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]

def bech32_encode(hrp, data):
    alphabet = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
    data5 = convertbits(data, 8, 5)
    combined = [0] + data5
    checksum = bech32_create_checksum(hrp, combined)
    return hrp + '1' + ''.join([alphabet[d] for d in combined + checksum])

def hash_to_address(script_type, hash_bytes):
    if script_type == 'P2PKH' :
        return base58check_encode(b'\x00' + hash_bytes)
    elif script_type == 'P2SH' :
        return base58check_encode(b'\x05' + hash_bytes)
    elif script_type == 'P2WPKH' :
        return bech32_encode('bc', hash_bytes)
    else:
        return 'unknown'