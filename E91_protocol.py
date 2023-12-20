# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 14:34:44 2023

@author: user
"""

import numpy as np
import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.quantum_info import state_fidelity

def create_entangled_pair():
    qc = QuantumCircuit(2, 2)  # 2 qubits and 2 classical bits
    qc.h(0)
    qc.cx(0, 1)
    return qc

def measure_in_basis(qc, basis, qubit):
    if basis == "X":
        qc.h(qubit)
    elif basis == "Y":
        qc.sdg(qubit)
        qc.h(qubit)
    # For Z basis, no need to add anything
    qc.measure(qubit, qubit)

# Setup
np.random.seed(42)  # for reproducibility
num_bits = 100
alice_bases = np.random.choice(['X', 'Y', 'Z'], num_bits)
bob_bases = np.random.choice(['X', 'Y', 'Z'], num_bits)

# Create and measure entangled pairs
results_alice = []
results_bob = []
for i in range(num_bits):
    qc = create_entangled_pair()
    qc.barrier()
    measure_in_basis(qc, alice_bases[i], 0)
    measure_in_basis(qc, bob_bases[i], 1)
    qc.barrier()

    # Execute the circuit
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=1, memory=True).result()
    measured_bits = result.get_memory()[0]
    results_alice.append(int(measured_bits[1]))  # Changed to [1] for Alice's result
    results_bob.append(int(measured_bits[0]))  # Changed to [0] for Bob's result

# Sift the key
sifted_key_alice = []
sifted_key_bob = []
for i in range(num_bits):
    if alice_bases[i] == bob_bases[i]:
        sifted_key_alice.append(results_alice[i])
        sifted_key_bob.append(results_bob[i])

# Test for eavesdropping (simplified check)
if sifted_key_alice != sifted_key_bob:
    print("Eavesdropping detected")
else:
    print("Key successfully shared")