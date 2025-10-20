#!/usr/bin/env python3
"""
ORCP - OpenRed Cryptographic Pattern
Security Validation Test Script
Validates the detection of alterations in patterns
Author : Diego Morales Magri - October 2025
"""

import numpy as np
from Test_crypt.ORCP import ORCP

def security_validation(runs=100, verbose=False):
    orcp = ORCP(vertices=14)
    total_tests = 0
    undetected = 0
    for _ in range(runs):
        pattern = orcp.generate_motif()
        vertices, adj_matrix = orcp.create_graph_from_motif(pattern)
        public_key, verification_data = orcp.generate_self_verifiable_key(pattern)
        for i in range(orcp.total_bits):
            # Flip bit i
            altered = list(pattern)
            altered[i] = '1' if pattern[i] == '0' else '0'
            altered_pattern = ''.join(altered)
            detected = not orcp.verify_signature_without_public_key(altered_pattern, verification_data)
            total_tests += 1
            if not detected:
                undetected += 1
                if verbose:
                    print(f"Undetected alteration at bit {i} for pattern {pattern}")
    print(f"Total tests: {total_tests}")
    print(f"Undetected alterations: {undetected}")
    print(f"Detection rate: {(total_tests-undetected)/total_tests*100:.2f}%")

if __name__ == '__main__':
    security_validation(runs=100)
