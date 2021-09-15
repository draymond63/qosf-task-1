from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
from qiskit.visualization import plot_bloch_multivector
from typing import List
import math
import matplotlib.pyplot as plt

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
qc.tdg(qreg_q[0]).c_if(creg_c[0], 1)
qc.t  (qreg_q[0]).c_if(creg_c[1], 1)
qc.tdg(qreg_q[0]).c_if(creg_c[2], 1)
qc.t  (qreg_q[0]).c_if(creg_c[3], 1)
qc.tdg(qreg_q[1]).c_if(creg_c[0], 1)
qc.tdg(qreg_q[1]).c_if(creg_c[1], 1)
qc.t  (qreg_q[1]).c_if(creg_c[2], 1)
qc.t  (qreg_q[1]).c_if(creg_c[3], 1)
qc.barrier(qreg_q)

# If only one index is active, move the state to 100% probablity
qc.tdg(qreg_q[0]).c_if(creg_c, 0b0001)
qc.t  (qreg_q[0]).c_if(creg_c, 0b0010)
qc.tdg(qreg_q[0]).c_if(creg_c, 0b0100)
qc.t  (qreg_q[0]).c_if(creg_c, 0b1000)
qc.tdg(qreg_q[1]).c_if(creg_c, 0b0001)
qc.tdg(qreg_q[1]).c_if(creg_c, 0b0010)
qc.t  (qreg_q[1]).c_if(creg_c, 0b0100)
qc.t  (qreg_q[1]).c_if(creg_c, 0b1000)

qc.h(qreg_q[0])
qc.h(qreg_q[1])

print(qc.draw())

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
	# TODO: Put indices into the cbit
	# Get bloch
	backend_sim = Aer.get_backend('statevector_simulator')
	result = execute(qc, backend_sim).result()
	state = result.get_statevector(qc)
	plot_bloch_multivector(state)
	plt.show()

if __name__ == '__main__':
	vec = [1, 5, 7, 10]
	getQB(vec)