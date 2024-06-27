import hashlib
from os import urandom as generate_bytes

import binascii


def create_token_string(character_length: int) -> str:
    return binascii.hexlify(generate_bytes(int(character_length / 2))).decode()


def hash_token(hash_algorithm, token: str) -> str:
    """
    Calculates the hash of a token.
    Token must contain an even number of hex digits or
    a binascii.Error exception will be raised.
    """
    digest = getattr(hashlib, hash_algorithm)()
    digest.update(make_hex_compatible(token))
    return digest.hexdigest()


def make_hex_compatible(token: str) -> bytes:
    """
    We need to make sure that the token, that is send is hex-compatible.
    When a token prefix is used, we cannot guarantee that.
    """
    return binascii.unhexlify(binascii.hexlify(bytes(token, "utf-8")))
