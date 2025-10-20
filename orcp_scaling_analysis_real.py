#!/usr/bin/env python3
"""
ORCP - OpenRed Cryptographic Pattern
Scaling Analysis with Real Implementation
Analyzes the impact of the number of vertices on key generation and verification times
Author : Diego Morales Magri - October 2025
"""
import time
from ORCP import ORCP

def analyze_orcp_scaling(vertices_range):
    """Analyze the impact of the number of vertices on ORCP using real key generation and verification."""
    results = []
    for n in vertices_range:
        orcp = ORCP(vertices=n)
        motif = orcp.generate_motif()
        start_gen = time.time()
        public_key, verification_data = orcp.generate_self_verifiable_key(motif)
        end_gen = time.time()
        gen_time_ms = (end_gen - start_gen) * 1000

        start_ver = time.time()
        is_valid = orcp.verify_signature_without_public_key(motif, verification_data)
        end_ver = time.time()
        ver_time_ms = (end_ver - start_ver) * 1000

        results.append({
            'vertices': n,
            'total_bits': orcp.total_bits,
            'public_key': public_key,
            'gen_time_ms': gen_time_ms,
            'ver_time_ms': ver_time_ms,
            'is_valid': is_valid
        })
    return results

def main():
    # Analyze for different numbers of vertices
    vertices_to_test = [8, 10, 12, 14, 16, 18, 20, 24, 32]
    analysis = analyze_orcp_scaling(vertices_to_test)

    print("=== ORCP SCALING ANALYSIS (Real Implementation) ===\n")
    print(f"{'Vertices':<8} {'Bits':<6} {'GenTime(ms)':<12} {'VerTime(ms)':<12} {'Valid'}")
    print(f"{'--------':<8} {'-----':<6} {'-----------':<12} {'-----------':<12} {'-----'}")
    for r in analysis:
        print(f"{r['vertices']:<8} {r['total_bits']:<6} {r['gen_time_ms']:.2f}      {r['ver_time_ms']:.2f}      {str(r['is_valid'])}")

    print("\n=== RECOMMENDATIONS ===")
    for r in analysis:
        if r['vertices'] == 12:
            print(f"✅ LIGHTWEIGHT OPTIMAL - {r['vertices']} vertices: Ideal for IoT, mobile, fast P2P")
        elif r['vertices'] == 14:
            print(f"✅ BALANCED OPTIMAL - {r['vertices']} vertices: Ideal for robust commercial applications")
        elif r['vertices'] == 16:
            print(f"✅ ROBUST OPTIMAL - {r['vertices']} vertices: Ideal for maximum acceptable security")
    print("\n⚠️ LIMITS:")
    limit_20 = next(r for r in analysis if r['vertices'] == 20)
    print(f"• 20+ vertices: {limit_20['gen_time_ms']:.1f}ms (becomes heavy)")
    limit_24 = next(r for r in analysis if r['vertices'] == 24)
    print(f"• 24+ vertices: {limit_24['gen_time_ms']:.1f}ms (too slow for real-time)")

if __name__ == "__main__":
    main()
