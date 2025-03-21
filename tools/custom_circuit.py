#!/usr/bin/env python3
from qiskit import QuantumCircuit
from qiskit.exceptions import QiskitError

def create_custom_circuit(input_code):
    if not input_code.strip().startswith("OPENQASM"):
        input_code = "OPENQASM 2.0;\ninclude \"qelib1.inc\";\n\n" + input_code
    
    try:
        circuit = QuantumCircuit.from_qasm_str(input_code)
        return circuit
    except QiskitError as e:
        error_msg = str(e)
        if "syntax error" in error_msg.lower():
            line_info = error_msg.split("line")[-1].strip() if "line" in error_msg else ""
            raise ValueError(f"QASM syntax error {line_info}")
        elif "unregistered" in error_msg.lower() and "gate" in error_msg.lower():
            gate = error_msg.split("'")[1] if "'" in error_msg else "gate"
            raise ValueError(f"Unregistered gate '{gate}'")
        elif "not defined" in error_msg.lower():
            item = error_msg.split("'")[1] if "'" in error_msg else "item"
            raise ValueError(f"'{item}' is not defined")
        else:
            raise ValueError(f"QASM error: {error_msg}")
    except Exception as e:
        raise ValueError(f"Processing error: {str(e)}")