-- BTC Reader - Initial Schema

CREATE TABLE IF NOT EXISTS blocks (
    id          SERIAL PRIMARY KEY,
    hash        VARCHAR(64)  NOT NULL UNIQUE,
    height      INTEGER      NOT NULL UNIQUE,
    version     INTEGER      NOT NULL,
    prev_hash   VARCHAR(64),
    merkle_root VARCHAR(64)  NOT NULL,
    timestamp   BIGINT       NOT NULL,
    bits        VARCHAR(16)  NOT NULL,
    nonce       BIGINT       NOT NULL,
    tx_count    INTEGER      NOT NULL DEFAULT 0,
    size        INTEGER,
    weight      INTEGER,
    raw         JSONB,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS transactions (
    id          SERIAL PRIMARY KEY,
    txid        VARCHAR(64)  NOT NULL UNIQUE,
    block_hash  VARCHAR(64)  REFERENCES blocks(hash) ON DELETE SET NULL,
    block_height INTEGER,
    version     INTEGER      NOT NULL,
    locktime    BIGINT       NOT NULL,
    size        INTEGER,
    weight      INTEGER,
    fee         BIGINT,
    raw         JSONB,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_blocks_height      ON blocks(height);
CREATE INDEX IF NOT EXISTS idx_blocks_timestamp   ON blocks(timestamp);
CREATE INDEX IF NOT EXISTS idx_tx_block_hash      ON transactions(block_hash);
CREATE INDEX IF NOT EXISTS idx_tx_block_height    ON transactions(block_height);
