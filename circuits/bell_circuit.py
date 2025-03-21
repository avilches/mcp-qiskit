from qiskit import QuantumCircuit

def create_bell_circuit():
    """Create a Bell state quantum circuit using Qiskit"""
    # Create a quantum circuit with 2 qubits
    circuit = QuantumCircuit(2, 2)
    
    # Apply Hadamard gate to the first qubit
    circuit.h(0)
    
    # Apply CNOT gate with control qubit 0 and target qubit 1
    circuit.cx(0, 1)
    
    # Measure both qubits
    circuit.measure([0, 1], [0, 1])
    
    return circuit

def get_bell_circuit_ascii():
    """Returns a pre-formatted ASCII art of the Bell circuit
    
    This avoids issues with rendering the circuit in different Qiskit versions
    """
    return """     ┌───┐     ┌─┐   
q_0: ┤ H ├──■──┤M├───
     └───┘┌─┴─┐└╥┘┌─┐
q_1: ─────┤ X ├─╫─┤M├
          └───┘ ║ └╥┘
c: 2/═══════════╩══╩═
                0  1"""