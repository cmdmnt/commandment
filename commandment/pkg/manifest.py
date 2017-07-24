from typing import List, Union
import hashlib
import io

# Required for InstallApplication to work.
DEFAULT_MD5_CHUNK_SIZE = 10485760


def chunked_hash(stream: Union[io.RawIOBase, io.BufferedIOBase], chunk_size: int = DEFAULT_MD5_CHUNK_SIZE) -> List[bytes]:
    """Create a list of hashes of chunk_size size in bytes.

    Args:
          stream (Union[io.RawIOBase, io.BufferedIOBase]): The steam containing the bytes to be hashed.
          chunk_size (int): The md5 chunk size. Default is 10485760 (which is required for InstallApplication).

    Returns:
          List[str]: A list of md5 hashes calculated for each chunk
    """
    chunk = stream.read(chunk_size)
    hashes = []

    while chunk is not None:
        h = hashlib.md5()
        h.update(chunk)
        md5 = h.digest()
        hashes.append(md5)
        chunk = stream.read(chunk_size)

    return hashes
