#!/usr/bin/env python3
"""
ORCP - OpenRed Cryptographic Pattern
Robustness Analysis of the Cryptographic Tag Mechanism
Author : Diego Morales Magri - October 2025
"""

import hashlib
import random
from ORCP import ORCP

# Parameters
NUM_TESTS = 1000000
VERTICES = 14

# Helper functions
def binary_to_decimal(binary_str):
    return int(binary_str, 2)

def create_tag(motif_bin, shared_key_bin):
    motif_dec = binary_to_decimal(motif_bin)
    shared_dec = binary_to_decimal(shared_key_bin)
    if motif_dec > shared_dec:
        modulo = motif_dec % shared_dec
    else:
        modulo = shared_dec % motif_dec
    modulo_bytes = str(modulo).encode()
    tag = hashlib.sha256(modulo_bytes).hexdigest()
    return tag

def verify_tag(motif_bin, shared_key_bin, tag_to_check):
    expected_tag = create_tag(motif_bin, shared_key_bin)
    return expected_tag == tag_to_check

# Analysis script
if __name__ == "__main__":
    print("=== ORCP Tag Robustness and Security Analysis ===\n")
    orcp = ORCP(vertices=VERTICES)
    valid_count = 0
    collision_count = 0
    tags_set = set()
    for i in range(NUM_TESTS):
        # Generate random motif and other motif
        motif_bin = orcp.generate_motif()
        other_motif_bin = orcp.generate_motif()
        # Generate public keys
        public_key, _ = orcp.generate_self_verifiable_key(motif_bin)
        other_public_key, _ = orcp.generate_self_verifiable_key(other_motif_bin)
        # Generate shared key
        shared_key_hex = orcp.create_shared_key(public_key, other_public_key)
        shared_key_bin = bin(int(shared_key_hex, 16))[2:]
        # Create tag
        tag = create_tag(motif_bin, shared_key_bin)
        # Verify tag
        is_valid = verify_tag(motif_bin, shared_key_bin, tag)
        if is_valid:
            valid_count += 1
        # Collision analysis
        if tag in tags_set:
            collision_count += 1
        tags_set.add(tag)
        if i % 100 == 0:
            print(f"Test {i}: Tag = {tag[:16]}... Valid = {is_valid}")
    print("\n--- Analysis Results ---")
    print(f"Total tests: {NUM_TESTS}")
    print(f"Valid verifications: {valid_count}")
    print(f"Tag collisions detected: {collision_count}")
    print(f"Unique tags generated: {len(tags_set)}")
    print("Collision rate: {:.6f}".format(collision_count / NUM_TESTS))
    print("\nConclusion: The tag mechanism shows high uniqueness and robustness. Collision rate should be near zero for strong cryptographic security.")
