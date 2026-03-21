import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # Bitcoin node RPC
    btc_rpc_host: str
    btc_rpc_port: int
    btc_rpc_user: str
    btc_rpc_password: str

    # Database
    db_dsn: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            btc_rpc_host=os.environ.get("BTC_RPC_HOST", "127.0.0.1"),
            btc_rpc_port=int(os.environ.get("BTC_RPC_PORT", "8332")),
            btc_rpc_user=os.environ.get("BTC_RPC_USER", "bitcoin"),
            btc_rpc_password=os.environ.get("BTC_RPC_PASSWORD", ""),
            db_dsn=os.environ.get(
                "DATABASE_URL",
                "postgresql://btc_user:secret@db:5432/btc_reader",
            ),
        )
