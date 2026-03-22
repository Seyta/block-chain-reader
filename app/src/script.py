def parse_script(script_bytes):
    if script_bytes[:3] == b'\x76\xa9\x14' and script_bytes[-2:] == b'\x88\xac' :
        return 'P2PKH', script_bytes[3:-2]
    elif script_bytes[:2] == b'\xa9\x14' and script_bytes[-1:] == b'\x87' :
        return 'P2SH', script_bytes[2:-1]
    elif script_bytes[:2] == b'\x00\x14' :
        return 'P2WPKH', script_bytes[2:]
    elif script_bytes[:1] == b'\x6a' :
        return 'OP_RETURN', script_bytes[1:]
    else:
        return 'unknown', None