from qiskit import QuantumCircuit
from qiskit.exceptions import QiskitError

def create_custom_circuit(input_code):
    """Create a custom quantum circuit using OpenQASM code.
    
    This function accepts OpenQASM 2.0 code:
    ```
    OPENQASM 2.0;
    include "qelib1.inc";
    
    qreg q[3];
    creg c[3];
    
    h q[0];
    cx q[0], q[1];
    cx q[0], q[2];
    measure q -> c;
    ```
    """
    return _create_circuit_from_qasm(input_code)


def _create_circuit_from_qasm(qasm_code):
    """Create a quantum circuit from OpenQASM code."""
    from qiskit import QuantumCircuit
    from qiskit.exceptions import QiskitError
    
    try:
        # Check if the QASM code has the required header
        if not qasm_code.strip().startswith("OPENQASM"):
            # Add the QASM header if not present
            qasm_code = "OPENQASM 2.0;\ninclude \"qelib1.inc\";\n\n" + qasm_code
        
        # Use QuantumCircuit.from_qasm_str which is available in most Qiskit versions
        circuit = QuantumCircuit.from_qasm_str(qasm_code)
        return circuit
    
    except QiskitError as e:
        # Provide more user-friendly error messages for common QASM errors
        error_msg = str(e)
        if "syntax error" in error_msg.lower():
            line_info = error_msg.split("line")[-1].strip() if "line" in error_msg else ""
            raise ValueError(f"QASM syntax error {line_info}. Please check your QASM code.")
        elif "unregistered" in error_msg.lower() and "gate" in error_msg.lower():
            gate = error_msg.split("'")[1] if "'" in error_msg else "gate"
            raise ValueError(f"Unregistered gate '{gate}'. Make sure to include 'qelib1.inc' for standard gates.")
        elif "not defined" in error_msg.lower():
            item = error_msg.split("'")[1] if "'" in error_msg else "item"
            raise ValueError(f"'{item}' is not defined. Make sure all registers are declared before use.")
        else:
            # Pass through the original error if we don't have a better message
            raise ValueError(f"Error in QASM code: {error_msg}")
    
    except Exception as e:
        # Catch all other exceptions
        raise ValueError(f"Error processing QASM code: {str(e)}")
