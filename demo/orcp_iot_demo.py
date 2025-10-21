"""
ORCP IoT Demonstration
This script presents a technical demonstration of the application of the ORCP protocol in an IoT context.
The script simulates enrollment, authentication, and pattern rotation for a connected device, displaying steps and results in the terminal.
Author: Diego Morales Magri - October 2025
"""
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ORCP import ORCP

# IoT device initialization
orcp_device = ORCP(vertices=14)

# Step 1: Device enrollment
import time as _time
print("[1] IoT device enrollment...")
t_enroll_start = _time.time()
pattern = orcp_device.generate_motif()
public_key, verification_data = orcp_device.generate_self_verifiable_key(pattern)
t_enroll_end = _time.time()
print(f"Generated public key: {public_key}")
print(f"Initial pattern generated: {pattern}")
print(f"Enrollment time: {(t_enroll_end-t_enroll_start)*1000:.2f} ms")

# Step 2: Authentication with the network
print("\n[2] IoT device authentication...")
t_auth_start = _time.time()
auth_result = orcp_device.verify_signature_without_public_key(pattern, verification_data)
t_auth_end = _time.time()
if auth_result:
    print("Authentication successful.")
else:
    print("Authentication failed.")
print(f"Authentication time: {(t_auth_end-t_auth_start)*1000:.2f} ms")

# Step 3: pattern rotation for each session
for session in range(1, 4):
    print(f"\n[3] Session {session}: pattern rotation...")
    t_rot_start = _time.time()
    pattern = orcp_device.generate_motif()
    public_key, verification_data = orcp_device.generate_self_verifiable_key(pattern)
    t_rot_end = _time.time()
    print(f"New pattern: {pattern}")
    t_auth_rot_start = _time.time()
    auth_rot_result = orcp_device.verify_signature_without_public_key(pattern, verification_data)
    t_auth_rot_end = _time.time()
    if auth_rot_result:
        print("Authentication successful with new pattern.")
    else:
        print("Authentication failed.")
    print(f"pattern rotation time: {(t_rot_end-t_rot_start)*1000:.2f} ms")
    print(f"Authentication time: {(t_auth_rot_end-t_auth_rot_start)*1000:.2f} ms")
    time.sleep(1)

print("\nDemonstration finished.")
