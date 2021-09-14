from typing import List
import math

# importing Qiskit
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute

# import basic plot tools
from qiskit.visualization import plot_bloch_multivector

"""
Task 1

Design a quantum circuit that considers as input the following vector of integers numbers: 

[1,5,7,10]

returns a quantum state which is a superposition of indices of the target solution, obtaining 
in the output the indices of the inputs where two adjacent bits will always have different values. 
In this case the output should be: |01> + |11>, as the correct indices are 1 and 3.
"""

qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(4, 'c')
qc = QuantumCircuit(qreg_q, creg_c)

qc.reset(qreg_q[0])
qc.reset(qreg_q[1])
qc.h(qreg_q[1])
qc.h(qreg_q[0])
qc.s(qreg_q[1])
qc.s(qreg_q[0])
qc.h(qreg_q[1])
qc.h(qreg_q[0])
qc.barrier(qreg_q)

# ! Not happy with c_if using bits
qc.tdg(qreg_q[0]).c_if(qc, 1)
qc.t(qreg_q[0]).c_if(creg_c[1], 1)
qc.tdg(qreg_q[0]).c_if(creg_c[2], 1)
qc.t(qreg_q[0]).c_if(creg_c[3], 1)
qc.h(qreg_q[0])
qc.tdg(qreg_q[1]).c_if(creg_c[0], 1)
qc.tdg(qreg_q[1]).c_if(creg_c[1], 1)
qc.t(qreg_q[1]).c_if(creg_c[2], 1)
qc.t(qreg_q[1]).c_if(creg_c[3], 1)
qc.h(qreg_q[1])

qc.draw()

def getIndices(inputs) -> List[int]:
	indices = []

	for index, i in enumerate(inputs):
		# ! Wild expression to determine if bits are alternating: O(1) !
		if (math.log2((i ^ ((i << 1) + (0 if i % 2 else 1))) + 1) % 1 == 0) and i > 3:
			indices.append(index)
	return indices

def getQB(inputs):
	assert len(inputs) <= 4, "Can only support up to 4 inputs at a time"
	indices = getIndices(inputs)
	if not len(indices):
		return None
	backend_sim = Aer.get_backend('statevector_simulator')
	result = execute(qc, backend_sim).result()
	state = result.get_statevector(qc)
	plot_bloch_multivector(state)

if __name__ == '__main__':
	vec = [1, 5, 7, 10]
	getQB(vec)