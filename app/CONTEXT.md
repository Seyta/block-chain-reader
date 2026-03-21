# Bitcoin Blockchain Parser — Project Context

## Objectif

Projet éducatif : construire from scratch un parser de blockchain Bitcoin en Python.
Le but est de **comprendre** le fonctionnement interne de Bitcoin en codant tout soi-même.

## Règles du projet

- **Aucune lib externe blockchain** : pas de `python-bitcoinlib`, pas de `bitcoin-utils`, rien.
- **Stdlib Python uniquement** : `hashlib`, `struct`, `socket`, `urllib.request`, `json`, `io`, etc.
- Tout le décodage / parsing / hashing est écrit à la main.
- Le code doit être lisible, bien commenté, orienté apprentissage.

## Stack technique

- **Langage** : Python 3.12+
- **Dépendances** : aucune (stdlib only)
- **Environnement** : Docker Compose
- **Source de données** : API publique Blockstream (`blockstream.info/api`) pour récupérer les blocs bruts (raw bytes), identiques aux données d'un nœud Bitcoin Core.

## Architecture prévue

```
btc-parser/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt          # vide (stdlib only), présent par convention
├── src/
│   ├── __init__.py
│   ├── fetcher.py            # Récupération de blocs bruts via API
│   ├── block.py              # Parser de block header + structure bloc
│   ├── transaction.py        # Décodage des transactions (inputs, outputs)
│   ├── script.py             # Interpréteur de scripts Bitcoin (opcodes)
│   ├── address.py            # Décodage d'adresses (Base58Check, Bech32)
│   ├── merkle.py             # Construction / vérification Merkle Tree
│   ├── pow.py                # Vérification Proof of Work
│   ├── utils.py              # Helpers : hash256, little-endian, hex, etc.
│   └── network.py            # (futur) Connexion P2P au réseau Bitcoin
├── tests/
│   ├── test_block.py
│   ├── test_transaction.py
│   ├── test_script.py
│   ├── test_merkle.py
│   └── test_pow.py
├── data/                     # Blocs bruts sauvegardés localement (cache)
├── main.py                   # Point d'entrée / démos
└── CONTEXT.md                # Ce fichier
```

## Source de données — API Blockstream

L'API retourne les blocs en bytes bruts (format sérialisé identique au réseau Bitcoin / fichiers blk*.dat).

Endpoints utiles :
- `GET /api/block/{hash}/raw` → bloc complet en binaire (bytes)
- `GET /api/block/{hash}` → métadonnées du bloc en JSON
- `GET /api/block-height/{height}` → hash du bloc à une hauteur donnée
- `GET /api/blocks/tip/hash` → hash du dernier bloc

Exemple d'usage :
```python
import urllib.request

block_hash = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"  # bloc genesis
url = f"https://blockstream.info/api/block/{block_hash}/raw"
raw_block = urllib.request.urlopen(url).read()  # bytes bruts du bloc
```

## Format d'un bloc Bitcoin (binaire, little-endian)

### Block Header (80 bytes)
| Champ          | Taille   | Description                          |
|----------------|----------|--------------------------------------|
| version        | 4 bytes  | Version du bloc                      |
| prev_block     | 32 bytes | Hash du bloc précédent               |
| merkle_root    | 32 bytes | Racine de l'arbre de Merkle          |
| timestamp      | 4 bytes  | Unix timestamp                       |
| bits           | 4 bytes  | Target de difficulté (compact)       |
| nonce          | 4 bytes  | Nonce utilisé pour le mining         |

### Après le header
| Champ          | Taille     | Description                        |
|----------------|------------|------------------------------------|
| tx_count       | varint     | Nombre de transactions             |
| transactions   | variable   | Liste des transactions sérialisées |

### Format VarInt Bitcoin
| Valeur         | Préfixe | Lecture                              |
|----------------|---------|--------------------------------------|
| < 0xFD         | aucun   | 1 byte direct                        |
| <= 0xFFFF      | 0xFD    | 2 bytes little-endian après préfixe  |
| <= 0xFFFFFFFF  | 0xFE    | 4 bytes little-endian après préfixe  |
| > 0xFFFFFFFF   | 0xFF    | 8 bytes little-endian après préfixe  |

### Format d'une transaction
| Champ          | Taille     | Description                        |
|----------------|------------|------------------------------------|
| version        | 4 bytes    | Version de la transaction          |
| flag           | 2 bytes    | (optionnel) 0x0001 = SegWit        |
| input_count    | varint     | Nombre d'inputs                    |
| inputs         | variable   | Liste des inputs                   |
| output_count   | varint     | Nombre d'outputs                   |
| outputs        | variable   | Liste des outputs                  |
| witness        | variable   | (si SegWit) Données witness        |
| locktime       | 4 bytes    | Locktime de la transaction         |

## Roadmap de développement

### Phase 1 — Fondations
1. Setup Docker Compose (Python 3.12, environnement isolé)
2. `utils.py` — helpers : double SHA-256, lecture little-endian, varint, hex reverse
3. `fetcher.py` — fetch un bloc brut depuis l'API Blockstream
4. `block.py` — parser le header (80 bytes) et afficher les champs

### Phase 2 — Transactions
5. `transaction.py` — décoder une transaction complète (inputs, outputs, montants)
6. Gérer le format SegWit (flag, witness data)
7. Calculer le txid (hash de la transaction)

### Phase 3 — Vérifications
8. `pow.py` — vérifier le Proof of Work (hash < target)
9. `merkle.py` — construire le Merkle Tree et vérifier la racine
10. `script.py` — parser les scripts, identifier les types (P2PKH, P2SH, P2WPKH)

### Phase 4 — Adresses
11. `address.py` — dériver les adresses depuis les scripts
12. Base58Check encoding/decoding
13. Bech32 encoding/decoding

### Phase 5 — Réseau P2P (optionnel, avancé)
14. `network.py` — connexion TCP à un nœud Bitcoin
15. Handshake version/verack
16. Requêter des blocs via le protocole P2P

## Notes importantes

- Tous les entiers dans le protocole Bitcoin sont en **little-endian**.
- Les hashes sont affichés en **byte-reversed** (l'humain lit le hash à l'envers par rapport au stockage).
- Le hash d'un bloc = `SHA256(SHA256(header_80_bytes))` affiché en reversed.
- Le bloc Genesis a le hash : `000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f`
- La coinbase transaction (première tx d'un bloc) a des règles spéciales (input = hash nul).

## Commande pour Claude Code

> Lis ce fichier CONTEXT.md. Commence par créer l'environnement Docker Compose selon l'architecture décrite, puis implémente les modules dans l'ordre de la roadmap.