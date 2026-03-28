import logging
import socket
import threading
from src.network import NetworkMessage, create_version_message
from src.utils import little_endian_to_int

logger = logging.getLogger(__name__)

class PeerConnection :

    def __init__(self, host, port, message_callback):
        self.host = host
        self.port = port
        self.message_callback = message_callback
        self._socket = None
        self._running = threading.Event()
        self._send_lock = threading.Lock()
        self._thread = None

    def connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.host, self.port))
        self._socket.settimeout(10)

        self.send(create_version_message())
        self._receive()
        self.send(NetworkMessage('verack', b''))
        self._receive()
        logger.info(f"Handshake réussi avec {self.host}")

        self._running.set()
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
        logger.info(f"Connecté à {self.host}")

    def send(self, message):
        with self._send_lock:
            self._socket.sendall(message.serialize())

    def recv_all(self, n):
        data = b''
        while len(data) < n:
            chunk = self._socket.recv(n - len(data))
            if not chunk:
                raise ConnectionError('Connexion fermée')
            data += chunk
        return data

    def _receive(self):
        header = self._socket.recv(24)
        #print(f'header brut: {header.hex()}')
        command = header[4:16].decode('ascii', errors='ignore').strip('\x00')
        length = little_endian_to_int(header[16:20])
        payload = self.recv_all(length)
        return command, payload

    def _listen_loop(self):
        while self._running.is_set():
            try:
                command, payload = self._receive()
                if command :
                    self.message_callback(self, command, payload)
            except (OSError, socket.timeout):
                logger.warning(f"Déconnecté de {self.host}")
                self._running.clear()
                break

    def close(self):
        self._running.clear()
        self._socket.close()
        if self._thread is not None:
            self._thread.join(timeout=3)

    @property
    def is_alive(self):
        return self._running.is_set()
