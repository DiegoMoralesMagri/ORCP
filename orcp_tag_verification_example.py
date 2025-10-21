#!/usr/bin/env python3
"""
ORCP - OpenRed Cryptographic Pattern
Cryptographic Tag Verification Example
Author : Diego Morales Magri - October 2025
"""

import hashlib
from ORCP import ORCP

def binary_to_decimal(binary_str):
    """Converts a binary string to a decimal integer."""
    return int(binary_str, 2)

def create_tag(motif_bin, shared_key_bin):
    """
    Creates a mathematical tag from the binary motif and shared key.
    1. Converts both to decimal.
    2. Divides the larger by the smaller, takes the modulo.
    3. Hashes the result to obtain the tag.
    """
    motif_dec = binary_to_decimal(motif_bin)
    shared_dec = binary_to_decimal(shared_key_bin)
    if motif_dec > shared_dec:
        modulo = motif_dec % shared_dec
    else:
        modulo = shared_dec % motif_dec
    # Converts the modulo to bytes for hashing
    modulo_bytes = str(modulo).encode()
    tag = hashlib.sha256(modulo_bytes).hexdigest()
    return tag

def verify_tag(motif_bin, shared_key_bin, tag_to_check):
    """
    Checks if the tag computed from the motif and shared key matches the expected tag.
    """
    expected_tag = create_tag(motif_bin, shared_key_bin)
    return expected_tag == tag_to_check

# Example usage
if __name__ == "__main__":
    # Use the ORCP class to generate motifs and keys
    orcp = ORCP(vertices=14)
    # Generate motifs
    motif_bin = orcp.generate_motif()
    other_motif_bin = orcp.generate_motif()
    # Generate public keys
    public_key, _ = orcp.generate_self_verifiable_key(motif_bin)
    other_public_key, _ = orcp.generate_self_verifiable_key(other_motif_bin)
    # Generate shared key
    shared_key_hex = orcp.create_shared_key(public_key, other_public_key)
    # Convert shared key to binary
    shared_key_bin = bin(int(shared_key_hex, 16))[2:]
    # Create mathematical tag
    tag = create_tag(motif_bin, shared_key_bin)
    print(f"Binary motif: {motif_bin}")
    print(f"Public key: {public_key}")
    print(f"Shared key (hex): {shared_key_hex}")
    print(f"Shared key (bin): {shared_key_bin}")
    print(f"Generated mathematical tag: {tag}")
    # Verification
    is_valid = verify_tag(motif_bin, shared_key_bin, tag)
    print(f"Tag verification: {'OK' if is_valid else 'NOT VALID'}")
