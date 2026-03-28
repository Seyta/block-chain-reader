import io
import queue
import socket
import threading
from src.peer_connection import PeerConnection
from src.network import NetworkMessage
from src.utils import little_endian_to_int, int_to_little_endian, read_varint, int_to_varint

class NodeManager:

    def __init__(self):
        self.peers = []
        self.peers_lock = threading.Lock()
        self.new_block_queue = queue.Queue()

    def start(self, num_peers = 3):
        seeds = ['seed.bitcoin.sipa.be', 'dnsseed.bluematt.me']
        for seed in seeds:
            ips = socket.getaddrinfo(seed, 8333)
            if ips is None:
                continue
            ip = ips[0][4][0]
            peer_connection = PeerConnection(ip, 8333, self._on_message)
            try:
                peer_connection.connect()
            except:
                continue
            self.peers.append(peer_connection)

            if len(self.peers) >= num_peers:
                break

    def _on_message(self, peer, command, payload):
        print(f"[{peer.host}] {command}")
        if command == 'ping':
            peer.send(NetworkMessage('pong', payload))
        elif command == 'inv':
            self._handle_inv(payload)

    def _handle_inv(self, payload):
        stream = io.BytesIO(payload)
        count = read_varint(stream)
        for i in range(count):
            type = stream.read(4)
            hash = stream.read(32)

            if little_endian_to_int(type) == 2 : #MSG_BLOCK
                print(f"Nouveau bloc : {hash[::-1].hex()}")
                self.new_block_queue.put({'hash': hash[::-1].hex()})

    def broadcast(self, message):
        with self.peers_lock:
            for peer in self.peers:
                if peer.is_alive:
                    peer.send(message)

    def submit_block(self, header_bytes, coinbase_bytes):
        payload = header_bytes + int_to_varint(1) + coinbase_bytes
        self.broadcast(NetworkMessage('block', payload))

    def stop(self):
        with self.peers_lock:
            for peer in self.peers:
                peer.close()