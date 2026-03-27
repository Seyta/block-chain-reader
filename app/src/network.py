import io
import os
import socket
import time

from src.block import Block
from src.utils import hash256
from src.utils import int_to_little_endian
from src.utils import int_to_varint
from src.utils import little_endian_to_int


class NetworkMessage:
    def __init__(self, command, payload):
        self.command = command
        self.payload = payload

    def serialize(self):
        magic = b'\xf9\xbe\xb4\xd9'
        command = self.command.encode('ascii').ljust(12, b'\x00')
        length = int_to_little_endian(len(self.payload), 4)
        checksum = hash256(self.payload)[:4]

        return magic + command + length + checksum + self.payload

def create_version_message():
    version = int_to_little_endian(70015, 4)
    services = int_to_little_endian(0, 8)
    timestamp = int_to_little_endian(int(time.time()), 8)
    addr_recv = b'\x00' * 26
    addr_from = b'\x00' * 26
    nonce = os.urandom(8)
    user_agent = '/btc-reader:0.1/'
    user_agent = int_to_varint(len(user_agent)) + user_agent.encode('ascii')
    start_height = int_to_little_endian(0, 4)
    payload = version + services + timestamp + addr_recv + addr_from + nonce + user_agent + start_height

    return NetworkMessage('version', payload)

class BitcoinNode:
    def __init__(self, host, port=8333):
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.settimeout(10)

    def send(self, message):
        self.socket.sendall(message.serialize())

    def recv_all(self, n):
        data = b''
        while len(data) < n:
            chunk = self.socket.recv(n - len(data))
            if not chunk:
                raise ConnectionError('Connexion fermée')
            data += chunk
        return data

    def receive(self):
        header = self.socket.recv(24)
        #print(f'header brut: {header.hex()}')
        command = header[4:16].decode('ascii', errors='ignore').strip('\x00')
        length = little_endian_to_int(header[16:20])
        payload = self.recv_all(length)
        return command, payload

    def handshake(self):
        self.connect()
        self.send(create_version_message())
        self.receive()
        self.send(NetworkMessage('verack', b''))
        self.receive()
        print("Handshake réussi !")

    def get_block(self, block_hash_hex):
        block_hash = bytes.fromhex(block_hash_hex)[::-1]
        payload = int_to_varint(1) + int_to_little_endian(2,4) + block_hash
        message = NetworkMessage('getdata', payload)
        self.send(message)

        while True:
            command, data = self.receive()
            #print(command)
            if command == 'block':
                return Block.parse(io.BytesIO(data))

    def close(self):
        self.socket.close()