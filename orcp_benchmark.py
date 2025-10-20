#!/usr/bin/env python3
"""
ORCP - OpenRed Cryptographic Pattern
Benchmarking Script for Verification Performance
Measures verification time over multiple runs
Author : Diego Morales Magri - October 2025
"""

import time
import numpy as np
from Test_crypt.ORCP import ORCP

def run_benchmark(runs=10000):
    orcp = ORCP(vertices=14)
    valid_count = 0
    times = []
    for _ in range(runs):
        pattern = orcp.generate_motif()
        vertices, adj_matrix = orcp.create_graph_from_motif(pattern)
        public_key, verification_data = orcp.generate_self_verifiable_key(pattern)
        start = time.perf_counter()
        is_valid = orcp.verify_signature_without_public_key(pattern, verification_data)
        end = time.perf_counter()
        times.append(end - start)
        if is_valid:
            valid_count += 1
    print(f"Runs: {runs}")
    print(f"Valid verifications: {valid_count}")
    print(f"False positives: {runs - valid_count}")
    print(f"Mean verification time: {np.mean(times)*1000:.4f} ms")
    print(f"Std deviation: {np.std(times)*1000:.4f} ms")

if __name__ == '__main__':
    run_benchmark()
