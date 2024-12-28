
import hashlib

import requests
from tqdm import tqdm

def download_file(url, fname, chunk_size=1024):
    """Download a file, with progress bar"""

    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)

def checksum_file(path, chunk_size=2**16):
    """Compute checksum/hash of a file"""

    hasher = hashlib.sha1()
    with open(path, 'rb') as source:
      block = source.read(chunk_size)
      while len(block) != 0:
        hasher.update(block)
        block = source.read(chunk_size)

    return hasher.hexdigest()

