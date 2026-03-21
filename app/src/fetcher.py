import urllib.request
import json

def fetch_raw_block(block_hash):
    url = f"https://blockstream.info/api/block/{block_hash}/raw"
    return urllib.request.urlopen(url).read()

def fetch_block_hash(height):
    url = f"https://blockstream.info/api/block-height/{height}"
    return urllib.request.urlopen(url).read().decode('utf-8')

def fetch_block_json(block_hash):
    url = f"https://blockstream.info/api/block/{block_hash}"
    return json.loads(urllib.request.urlopen(url).read().decode('utf-8'))