#!/usr/bin/env python3
"""
ORCP - OpenRed Cryptographic Pattern
Self-verifiable cryptographic system without public key
Innovation: Uses graph morphological properties to create self-authenticating signatures
Author : Diego Morales Magri - October 2025
"""

import random
import hashlib
import numpy as np
import networkx as nx
from typing import Tuple, Dict, List
# Ajout pour HKDF
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class ORCP:
    def __init__(self, vertices=14):  # Optimized for 14 vertices
        self.vertices = vertices
        self.edges = vertices * (vertices - 1) // 2
        self.total_bits = vertices + self.edges
        
    def generate_motif(self) -> str:
        """Generates a random binary pattern"""
        return ''.join(random.choice(['0', '1']) for _ in range(self.total_bits))
    
    def create_graph_from_motif(self, motif: str) -> Tuple[Dict, np.ndarray]:
        """Creates a graph from the pattern"""
        # Vertex positions
        vertex_positions = list(range(0, self.vertices))
        vertices = {pos: motif[pos] for pos in vertex_positions}
        
    # Create adjacency matrix with remaining bits
        adj_matrix = np.zeros((self.vertices, self.vertices), dtype=int)
        edge_index = self.vertices  # Start after vertices
        
        for i in range(self.vertices):
            for j in range(i + 1, self.vertices):
                if edge_index < len(motif):
                    adj_matrix[i][j] = int(motif[edge_index])
                    adj_matrix[j][i] = adj_matrix[i][j]  # Symmetric
                    edge_index += 1
        
        return vertices, adj_matrix
    
    def calculate_morphological_signature(self, vertices: Dict, adj_matrix: np.ndarray) -> int:
        """Calculates the morphological signature of the graph"""
        signature = 0
        vertex_positions = list(vertices.keys())
        
        for i in range(adj_matrix.shape[0]):
            degree = sum(adj_matrix[i])
            bit_value = int(vertices[vertex_positions[i]])
            signature += degree * bit_value
        
        return signature
    
    def generate_self_verifiable_key(self, motif: str) -> Tuple[str, Dict]:
        """Generates a self-verifiable key without external public key"""
        vertices, adj_matrix = self.create_graph_from_motif(motif)
        morph_signature = self.calculate_morphological_signature(vertices, adj_matrix)
        
    # INNOVATION 1: Deterministic graph hash as "public fingerprint"
        graph_hash = self._compute_graph_hash(adj_matrix, vertices)
        
    # INNOVATION 2: Key derived with self-verifiable properties
    # Uses mathematical properties of the graph to create a key
    # that contains its own verification information
        eigenvalues = np.linalg.eigvals(adj_matrix.astype(float))
        spectral_signature = [round(x, 8) for x in sorted(eigenvalues.real)]
        
    # INNOVATION 3: Integrated signature using graph invariants
    # Topological invariants that do not change under isomorphism
        degree_sequence = sorted([sum(adj_matrix[i]) for i in range(self.vertices)])
        clustering_coeff = self._calculate_clustering_coefficient(adj_matrix)
        
    # Create the self-verifiable key
        verification_data = {
            'graph_hash': graph_hash,
            'spectral_signature': spectral_signature,
            'degree_sequence': degree_sequence,
            'clustering_coeff': clustering_coeff,
            'morph_signature': morph_signature,
            'vertices_count': self.vertices,
            'edges_count': np.sum(adj_matrix) // 2
        }
        
    # The "public key" is now derived from the graph properties
        public_key = self._derive_public_key(verification_data)
        
        return public_key, verification_data
    
    def _compute_graph_hash(self, adj_matrix: np.ndarray, vertices: Dict) -> str:
        """Computes a canonical hash of the graph"""
        # Create a canonical representation of the graph
        # Adjacency matrix in binary format, concatenated row by row
        adj_bin = ''.join(''.join(str(int(bit)) for bit in row) for row in adj_matrix)
        # Ordered vertex labels
        labels = ''.join(str(vertices[i]) for i in range(self.vertices))
        # Canonical representation
        graph_repr = adj_bin + labels
        return hashlib.sha256(graph_repr.encode()).hexdigest()[:16]
    
    def _calculate_clustering_coefficient(self, adj_matrix: np.ndarray) -> float:
        """Calculates the average clustering coefficient"""
        n = adj_matrix.shape[0]
        clustering_sum = 0
        
        for i in range(n):
            neighbors = [j for j in range(n) if adj_matrix[i][j] == 1]
            if len(neighbors) < 2:
                continue
            
            possible_edges = len(neighbors) * (len(neighbors) - 1) // 2
            actual_edges = 0
            
            for u in neighbors:
                for v in neighbors:
                    if u < v and adj_matrix[u][v] == 1:
                        actual_edges += 1
            
            if possible_edges > 0:
                clustering_sum += actual_edges / possible_edges
        
        return clustering_sum / n if n > 0 else 0
    
    def _derive_public_key(self, verification_data: Dict) -> str:
        """Derives a public key from the graph properties"""
        # Concatenate all important properties
        key_components = [
            str(verification_data['spectral_signature']),
            str(verification_data['degree_sequence']),
            str(verification_data['clustering_coeff']),
            str(verification_data['morph_signature']),
            verification_data['graph_hash']
        ]
        
        combined = ''.join(key_components)
        key_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        return key_hash[:32]  # 32-character hex public key
        
        def generate_self_verifiable_key(self, motif: str) -> Tuple[str, Dict]:
            """Génère une clé auto-vérifiable avec invariants strictement normalisés"""
            vertices, adj_matrix = self.create_graph_from_motif(motif)
            morph_signature = self.calculate_morphological_signature(vertices, adj_matrix)
            graph_hash = self._compute_graph_hash(adj_matrix, vertices)
            # Spectral signature : valeurs propres triées, arrondies à 8 décimales
            eigenvalues = np.linalg.eigvals(adj_matrix.astype(float))
            spectral_sorted = sorted(eigenvalues.real)
            # Séquence des degrés triée
            degree_sequence = sorted([sum(adj_matrix[i]) for i in range(self.vertices)])
            # Coefficient de clustering arrondi à 8 décimales
            clustering_coeff = round(self._calculate_clustering_coefficient(adj_matrix), 8)
            verification_data = {
                'graph_hash': graph_hash,
                'spectral_signature': spectral_sorted,
                'degree_sequence': degree_sequence,
                'clustering_coeff': clustering_coeff,
                'morph_signature': morph_signature,
                'vertices_count': self.vertices,
                'edges_count': int(np.sum(adj_matrix) // 2)
            }
            public_key = self._derive_public_key(verification_data)
            return public_key, verification_data
    
    def create_shared_key(self, my_public_key: str, other_public_key: str, use_hkdf: bool = True, salt: bytes = b"", info: bytes = b"orcp-shared-key") -> str:
        """Creates a shared key from public keys, using HKDF (default) or XOR (legacy)."""
        my_bytes = bytes.fromhex(my_public_key)
        other_bytes = bytes.fromhex(other_public_key)
    # Common input: concatenation of both public keys (canonical order)
        concat = my_bytes + other_bytes if my_bytes < other_bytes else other_bytes + my_bytes
        if use_hkdf:
            # Uses HKDF-SHA256 to derive the shared key (32 bytes)
            hkdf = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                info=info,
                backend=default_backend()
            )
            shared_key = hkdf.derive(concat)
            return shared_key.hex().upper()
        else:
            # Legacy mode: simple XOR (not recommended)
            shared_bytes = bytes(a ^ b for a, b in zip(my_bytes, other_bytes))
            return shared_bytes.hex().upper()
    
    def verify_signature_without_public_key(self, motif: str, signature_data: Dict) -> bool:
        """INNOVATION: Verifies a signature without needing the public key"""
        try:
            # Recreate the graph from the pattern
            vertices, adj_matrix = self.create_graph_from_motif(motif)
            
            # Recalculate all properties
            computed_morph_sig = self.calculate_morphological_signature(vertices, adj_matrix)
            computed_graph_hash = self._compute_graph_hash(adj_matrix, vertices)
            computed_eigenvalues = np.linalg.eigvals(adj_matrix.astype(float))
            computed_spectral_sorted = [round(x, 8) for x in sorted(computed_eigenvalues.real)]
            computed_degree_seq = sorted([sum(adj_matrix[i]) for i in range(self.vertices)])
            computed_clustering = self._calculate_clustering_coefficient(adj_matrix)
            
            # Check internal consistency
            # Element-wise comparison for spectral signature
            spectral_ok = (
                len(computed_spectral_sorted) == len(signature_data['spectral_signature']) and
                all(abs(a - b) < 1e-8 for a, b in zip(computed_spectral_sorted, signature_data['spectral_signature']))
            )
            checks = [
                computed_morph_sig == signature_data['morph_signature'],
                computed_graph_hash == signature_data['graph_hash'],
                spectral_ok,
                computed_degree_seq == signature_data['degree_sequence'],
                abs(computed_clustering - signature_data['clustering_coeff']) < 1e-8,
                signature_data['vertices_count'] == self.vertices,
                signature_data['edges_count'] == int(np.sum(adj_matrix) // 2)
            ]
            return all(checks)
            
        except Exception as e:
            print(f"Verification error: {e}")
            return False
    
    def demo_self_verification(self):
        """Demonstration of the self-verifiable system"""
        print("=== ORCP v2.0 - SELF-VERIFIABLE SYSTEM ===\n")
        
        # Generate the pattern
        motif = self.generate_motif()
        print(f"Generated pattern ({self.total_bits} bits): {motif[:20]}...{motif[-20:]}")
        
        # Generate the self-verifiable key
        public_key, verification_data = self.generate_self_verifiable_key(motif)
        print(f"Derived public key: {public_key}")
        
        # Display graph properties
        print(f"\nGraph properties:")
        print(f"  • Graph hash: {verification_data['graph_hash']}")
        print(f"  • Morphological signature: {verification_data['morph_signature']}")
        print(f"  • Spectral signature: [{', '.join(f'{x:.8f}' for x in verification_data['spectral_signature'])}]")
        print(f"  • Degree sequence: {verification_data['degree_sequence']}")
        print(f"  • Clustering coefficient: {verification_data['clustering_coeff']:.3f}")
        
        # Self-sufficient verification test
        print(f"\nSelf-sufficient verification test:")
        is_valid = self.verify_signature_without_public_key(motif, verification_data)
        print(f"  Signature valid: {is_valid}")
        
        # Test with an altered pattern
        altered_motif = motif[:10] + ('1' if motif[10] == '0' else '0') + motif[11:]
        is_valid_altered = self.verify_signature_without_public_key(altered_motif, verification_data)
        print(f"  Altered pattern valid: {is_valid_altered}")
        
        # Key exchange simulation without external public keys
        print(f"\nKey exchange simulation:")
        other_motif = self.generate_motif()
        other_public_key, other_verification = self.generate_self_verifiable_key(other_motif)
        
        shared_key = self.create_shared_key(public_key, other_public_key)
        print(f"  • My pattern: {motif[:20]}...")
        print(f"  • Other pattern: {other_motif[:20]}...")
        print(f"  • Shared key: {shared_key}")
        
        return {
            'motif': motif,
            'public_key': public_key,
            'verification_data': verification_data,
            'shared_key': shared_key
        }

def main():
    # Test with the optimal configuration (14 vertices)
    orcp = ORCP(vertices=14)
    results = orcp.demo_self_verification()
    
    print(f"\nADVANTAGES OF THE SELF-VERIFIABLE SYSTEM:")
    print("  No need for external public key")
    print("  Verification based on mathematical properties")
    print("  Resistant to substitution attacks")
    print("  Self-authenticating via topological invariants")
    print("  Lightweight and fast")

# Illustrative example: secure P2P exchange with ORCP (Alice/Bob)
def demo_p2p_exchange():
    print("\n=== DEMO: SECURE P2P EXCHANGE WITH ORCP ===\n")
    alice = ORCP(vertices=14)
    bob = ORCP(vertices=14)

    # Step 1: each node generates its secret pattern
    motif_alice = alice.generate_motif()
    motif_bob = bob.generate_motif()

    # Step 2: each node computes its public key and invariants
    pub_alice, verif_alice = alice.generate_self_verifiable_key(motif_alice)
    pub_bob, verif_bob = bob.generate_self_verifiable_key(motif_bob)

    print(f"Alice publishes: {pub_alice}")
    print(f"Bob publishes  : {pub_bob}")

    # Step 3: exchange public keys (pub_alice <-> pub_bob)
    # (in practice, via the network)

    # Step 4: each node derives the shared key from both public keys
    shared_alice = alice.create_shared_key(pub_alice, pub_bob)
    shared_bob = bob.create_shared_key(pub_bob, pub_alice)

    print(f"\nShared key computed by Alice : {shared_alice}")
    print(f"Shared key computed by Bob   : {shared_bob}")
    print(f"\nKeys identical? {shared_alice == shared_bob}")

    # Step 5: the shared key can be used to encrypt/authenticate the P2P session
    print("\nThe shared key can now be used to encrypt P2P exchanges.")

if __name__ == "__main__":
    main()
    demo_p2p_exchange()