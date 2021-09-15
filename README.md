# QOSF Task 1
## Hello!
This is my attempt at task 1.

**It doesn't work for two reasons** :)

1. My circuit involved conditionals based on bits within the classical register. However, I have learned the c_if function does not accepts bits, only full register. As a result, it can only do full registers equivalences. I could probably get around this by have 4 separate 1-bit classical registers, but that seemed too messy to be worth implementing. 

2. I tried to do a combined solution, using standard python to calculate the indices entries with alternating bits and a quantum circuit to generate the 2 qubits with the correct states. However, I ran into trouble when trying to interface the two. I couldn't figure out how to initialize the 4 classical bits in the circuit to contain the information about which indices to encoded. As a result, they always default to zero, which does nothing. 

If I were to restart, I would use the QRAM solution suggested in the context for task 1. I wanted to make a solution that didn't require it, but it does make the most sense for implementing a pure quantum solution.

## Thanks for the challenge!