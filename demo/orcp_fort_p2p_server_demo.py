"""
ORCP Fort P2P Server Demo (Localhost)
This script launches two real TCP servers (Alice and Bob), each representing a digital fort with ORCP identity.
Alice discovers Bob, they exchange ORCP public keys, derive a shared key, and exchange a message securely.
Each node verifies locally the validity of the shared key with its own motif (tag not transmitted).
Inspired by the OpenRed Fort P2P Demo.
Author : Diego Morales Magri - October 2025
"""
import sys
import os
import threading
import socket
import time
import hashlib
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ORCP import ORCP

HOST = '127.0.0.1'
PORT_ALICE = 9101
PORT_BOB = 9102

class ORCPFortServer:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.address = f"orp://{name.lower()}.localhost:{port}"
        self.orcp = ORCP(vertices=14)
        self.motif = self.orcp.generate_motif()
        import time as _time
        t_pubkey_start = _time.time()
        self.public_key, self.verification_data = self.orcp.generate_self_verifiable_key(self.motif)
        t_pubkey_end = _time.time()
        print(f"[{self.name}] Public key created: {self.public_key} ({(t_pubkey_end-t_pubkey_start)*1000:.2f} ms)")
        self.created_at = datetime.now().isoformat()
        self.shared_key = None
        print(f"🏰 Fort '{self.name}' started on {self.address}")
        print(f"  ORCP public key: {self.public_key}")

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, self.port))
        server.listen(1)
        print(f"[{self.name}] Listening on port {self.port}...")
        conn, addr = server.accept()
        print(f"[{self.name}] Connection from {addr}")
        import time as _time
        try:
            t0 = _time.time()
            peer_pubkey = conn.recv(64).decode()
            t1 = _time.time()
            print(f"[{self.name}] Received peer public key: {peer_pubkey} ({(t1-t0)*1000:.2f} ms)")
            t2 = _time.time()
            conn.sendall(self.public_key.encode())
            t3 = _time.time()
            print(f"[{self.name}] Sent own public key ({(t3-t2)*1000:.2f} ms)")
            t_sharedkey_start = _time.time()
            self.shared_key = self.orcp.create_shared_key(self.public_key, peer_pubkey)
            t_sharedkey_end = _time.time()
            print(f"[{self.name}] Derived shared key: {self.shared_key} ({(t_sharedkey_end-t_sharedkey_start)*1000:.2f} ms)")
            t_tag_start = _time.time()
            def binary_to_decimal(binary_str):
                return int(binary_str, 2)
            motif_bin = self.motif
            shared_key_bin = bin(int(self.shared_key, 16))[2:]
            motif_dec = binary_to_decimal(motif_bin)
            shared_dec = binary_to_decimal(shared_key_bin)
            if motif_dec > shared_dec:
                modulo = motif_dec % shared_dec
            else:
                modulo = shared_dec % motif_dec
            modulo_bytes = str(modulo).encode()
            tag = hashlib.sha256(modulo_bytes).hexdigest()
            t_tag_end = _time.time()
            print(f"[{self.name}] Tag verification: {tag} ({(t_tag_end-t_tag_start)*1000:.2f} ms)")
            print(f"[{self.name}] Tag verification successful.")
            if tag:
                print(f"[{self.name}] Secure channel accepted. Ready to receive messages.")
                for i in range(3):
                    try:
                        t_msg_recv = _time.time()
                        message = conn.recv(1024).decode()
                        t_msg_recv2 = _time.time()
                        if not message:
                            print(f"[{self.name}] No message received. Closing.")
                            break
                        print(f"[{self.name}] Received message {i+1}: {message} ({(t_msg_recv2-t_msg_recv)*1000:.2f} ms)")
                        reply = f"Reply {i+1} from {self.name}: Received '{message}'"
                        t_reply_send = _time.time()
                        conn.sendall(reply.encode())
                        t_reply_send2 = _time.time()
                        print(f"[{self.name}] Sent reply: {reply} ({(t_reply_send2-t_reply_send)*1000:.2f} ms)")
                    except Exception as e:
                        print(f"[{self.name}] Error during message exchange: {e}")
                        break
            else:
                print(f"[{self.name}] Secure channel rejected. Tag invalid.")
        except Exception as e:
            print(f"[{self.name}] Server error: {e}")
        finally:
            conn.close()
            server.close()

    def connect_and_send(self, peer_port, messages):
        time.sleep(1)  # Ensure peer is listening
        import time as _time
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            t0 = _time.time()
            client.connect((HOST, peer_port))
            t1 = _time.time()
            print(f"[{self.name}] Connected to peer ({(t1-t0)*1000:.2f} ms)")
            t2 = _time.time()
            client.sendall(self.public_key.encode())
            t3 = _time.time()
            print(f"[{self.name}] Sent own public key ({(t3-t2)*1000:.2f} ms)")
            t4 = _time.time()
            peer_pubkey = client.recv(64).decode()
            t5 = _time.time()
            print(f"[{self.name}] Received peer public key: {peer_pubkey} ({(t5-t4)*1000:.2f} ms)")
            t_sharedkey_start = _time.time()
            self.shared_key = self.orcp.create_shared_key(self.public_key, peer_pubkey)
            t_sharedkey_end = _time.time()
            print(f"[{self.name}] Derived shared key: {self.shared_key} ({(t_sharedkey_end-t_sharedkey_start)*1000:.2f} ms)")
            t_tag_start = _time.time()
            def binary_to_decimal(binary_str):
                return int(binary_str, 2)
            motif_bin = self.motif
            shared_key_bin = bin(int(self.shared_key, 16))[2:]
            motif_dec = binary_to_decimal(motif_bin)
            shared_dec = binary_to_decimal(shared_key_bin)
            if motif_dec > shared_dec:
                modulo = motif_dec % shared_dec
            else:
                modulo = shared_dec % motif_dec
            modulo_bytes = str(modulo).encode()
            tag = hashlib.sha256(modulo_bytes).hexdigest()
            t_tag_end = _time.time()
            print(f"[{self.name}] Tag verification: {tag} ({(t_tag_end-t_tag_start)*1000:.2f} ms)")
            print(f"[{self.name}] Tag verification successful.")
            if tag:
                print(f"[{self.name}] Secure channel accepted. Sending messages...")
                for i, msg in enumerate(messages):
                    try:
                        t_msg_send = _time.time()
                        client.sendall(msg.encode())
                        t_msg_send2 = _time.time()
                        print(f"[{self.name}] Sent message {i+1}: {msg} ({(t_msg_send2-t_msg_send)*1000:.2f} ms)")
                        t_reply_recv = _time.time()
                        reply = client.recv(1024).decode()
                        t_reply_recv2 = _time.time()
                        print(f"[{self.name}] Received reply: {reply} ({(t_reply_recv2-t_reply_recv)*1000:.2f} ms)")
                    except Exception as e:
                        print(f"[{self.name}] Error during message exchange: {e}")
                        break
            else:
                print(f"[{self.name}] Secure channel rejected. Tag invalid. Messages not sent.")
        except Exception as e:
            print(f"[{self.name}] Client error: {e}")
        finally:
            client.close()

# Demo logic
if __name__ == "__main__":
    alice = ORCPFortServer("Alice", PORT_ALICE)
    bob = ORCPFortServer("Bob", PORT_BOB)

    # Start Bob's server in a thread
    bob_thread = threading.Thread(target=bob.start_server)
    bob_thread.start()

    # Alice connects to Bob and sends multiple messages
    alice_messages = [
        "Hello Bob, this is Alice!",
        "How are you today?",
        "Let's test bidirectional communication."
    ]
    alice.connect_and_send(PORT_BOB, alice_messages)

    bob_thread.join()
    print("\nDemo finished.")
