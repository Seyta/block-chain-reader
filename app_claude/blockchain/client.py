"""
Bitcoin Core RPC client - stdlib only (http.client + json + base64).
"""
import base64
import json
import http.client
import logging
from typing import Any

logger = logging.getLogger(__name__)


class BitcoinRPCError(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(f"RPC error {code}: {message}")
        self.code = code


class BitcoinClient:
    """
    JSON-RPC 1.1 client for Bitcoin Core.
    Utilise uniquement la stdlib Python (http.client).
    """

    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        self._host = host
        self._port = port
        self._auth = base64.b64encode(f"{user}:{password}".encode()).decode()
        self._id = 0

    # ------------------------------------------------------------------ #
    # Low-level call                                                       #
    # ------------------------------------------------------------------ #

    def call(self, method: str, *params: Any) -> Any:
        self._id += 1
        payload = json.dumps(
            {"jsonrpc": "1.1", "id": self._id, "method": method, "params": list(params)}
        ).encode()

        conn = http.client.HTTPConnection(self._host, self._port, timeout=30)
        try:
            conn.request(
                "POST",
                "/",
                body=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Basic {self._auth}",
                },
            )
            response = conn.getresponse()
            raw = response.read()
        finally:
            conn.close()

        data = json.loads(raw)

        if data.get("error"):
            err = data["error"]
            raise BitcoinRPCError(err["code"], err["message"])

        return data["result"]

    # ------------------------------------------------------------------ #
    # High-level helpers                                                   #
    # ------------------------------------------------------------------ #

    def get_block_count(self) -> int:
        return self.call("getblockcount")

    def get_block_hash(self, height: int) -> str:
        return self.call("getblockhash", height)

    def get_block(self, block_hash: str, verbosity: int = 2) -> dict:
        """verbosity=2 → full tx objects"""
        return self.call("getblock", block_hash, verbosity)

    def get_raw_transaction(self, txid: str, verbose: bool = True) -> dict:
        return self.call("getrawtransaction", txid, verbose)

    def get_blockchain_info(self) -> dict:
        return self.call("getblockchaininfo")
