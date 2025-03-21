from qiskit import QuantumCircuit
import json

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
    
    # Return the circuit
    return circuit

def model_context_protocol():
    """Generate Model Context Protocol JSON with Bell circuit function"""
    mcp = {
        "schema_id": "mcp-1.0",
        "functions": [
            {
                "name": "Create a bell quantum circuit",
                "description": "Creates a quantum circuit that prepares a Bell state (entangled state) using Qiskit",
                "code": "create_bell_circuit",
                "parameters": [],
                "returns": {
                    "type": "quantum_circuit",
                    "description": "A Qiskit quantum circuit that creates a Bell state"
                }
            }
        ]
    }
    
    return json.dumps(mcp, indent=2)

if __name__ == "__main__":
    # Print the MCP JSON
    print(model_context_protocol())
    
    # Optionally, display the Bell circuit
    print("\nBell Circuit:")
    print(create_bell_circuit())