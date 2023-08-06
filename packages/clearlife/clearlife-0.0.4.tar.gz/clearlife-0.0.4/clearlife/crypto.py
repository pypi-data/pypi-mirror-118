"""Basic functions to create cryptographic keys, and to encrypt string data.

Basic cryptographic functions to aid in key management for the user.
"""

import nacl.bindings
import logging

from aries_cloudagent.wallet.crypto import (create_keypair, bytes_to_b58, validate_seed,
                                            verify_signed_message, b58_to_bytes)

log = logging.getLogger(__name__)


def create_did(seed: bytes):
    """Creates a DID and verkey from the given seed.

    Args:
        seed (bytes): the secret seed to use in generating the verkey.

    Returns:
        tuple: `(did, verkey)`.
    """
    seed = validate_seed(seed)
    verkey, _ = create_keypair(seed)
    did = bytes_to_b58(verkey[:16])
    return did, bytes_to_b58(verkey)


def verify_signature(signature, verkey, message=None):
    """Verifies a signature cryptographically.

    Args:
        agent (str): name of the agent whose master key should be used.
        signature (str): hex-encoded signature that should be verified.
        verkey (str): public key to use in verifying the signature.
    """
    s, v = bytes.fromhex(signature), b58_to_bytes(verkey)
    if message is not None:
        if isinstance(message, bytes):
            return verify_signed_message(s + message, v)
        else:
            return verify_signed_message(s + message.encode("UTF-8"), v)
    else:
        return verify_signed_message(s, v)


def anon_crypt_message(message: bytes, pk: bytes) -> bytes:
    """Apply anon_crypt to a binary message.

    Args:
        message: The message to encrypt
        pk: The verkey to encrypt the message for

    Returns:
        The anon encrypted message
    """
    _pk = nacl.bindings.crypto_sign_ed25519_pk_to_curve25519(pk)
    enc_message = nacl.bindings.crypto_box_seal(message, _pk)
    return enc_message


def anon_decrypt_message(enc_message: bytes, pk: bytes, sk: bytes) -> bytes:
    """Apply anon_decrypt to a binary message.

    Args:
        enc_message: The encrypted message
        pk: public key that the message was encrypted for.
        sk: private key that the message was encrypted for.

    Returns:
        The decrypted message
    """
    _pk = nacl.bindings.crypto_sign_ed25519_pk_to_curve25519(pk)
    _sk = nacl.bindings.crypto_sign_ed25519_sk_to_curve25519(sk)

    message = nacl.bindings.crypto_box_seal_open(enc_message, _pk, _sk)
    return message


def generate_keys(seed):
    """Generates keys from a given seed.

    Args:
        seed (str): of `32` characters or less. 32 characters encodes a 128-bit seed. If fewer
            than `32` are specified, it will be front-padded with zeros.
    """
    if isinstance(seed, bytes):
        byte_seed = seed
    else:
        byte_seed = f"{seed:0<32}".encode()
    pk, sk = create_keypair(byte_seed)
    did, verkey = create_did(byte_seed)
    return {    
        "seed": bytes_to_b58(seed) if isinstance(seed, bytes) else seed,
        "did": did, 
        "public": verkey, 
        "secret": sk.hex()
    }    