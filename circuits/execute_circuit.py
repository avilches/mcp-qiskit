#!/usr/bin/env python3
import time
from qiskit import QuantumCircuit, transpile
from qiskit.exceptions import QiskitError

# Handle different Qiskit versions
try:
    from qiskit_aer import Aer
    HAS_AER = True
except ImportError:
    try:
        from qiskit import Aer
        HAS_AER = True
    except ImportError:
        Aer = None
        HAS_AER = False

try:
    from qiskit_ibm_provider import IBMProvider
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler
        HAS_IBM_RUNTIME = True
    except ImportError:
        HAS_IBM_RUNTIME = False
    HAS_IBM_PROVIDER = True
except ImportError:
    HAS_IBM_PROVIDER = False
    HAS_IBM_RUNTIME = False

def execute_circuit(qasm_code, shots=1024, backend_name="aer_simulator"):
    try:
        circuit = QuantumCircuit.from_qasm_str(qasm_code)
        
        try:
            circuit_drawing = circuit.draw(output='text').single_string()
        except:
            circuit_drawing = str(circuit.draw(output='text'))
        
        if backend_name.startswith("aer_") or backend_name == "qasm_simulator":
            if not HAS_AER:
                return {
                    "status": "error",
                    "message": "Local simulator not available",
                    "circuit_drawing": circuit_drawing,
                    "backend_name": backend_name
                }
            
            try:
                backend = Aer.get_backend(backend_name)
            except Exception:
                try:
                    backend = Aer.get_backend("qasm_simulator")
                    backend_name = "qasm_simulator (fallback)"
                except Exception as fallback_error:
                    return {
                        "status": "error",
                        "message": str(fallback_error),
                        "circuit_drawing": circuit_drawing,
                        "backend_name": backend_name
                    }
            
            start_time = time.time()
            transpiled_circuit = transpile(circuit, backend)
            job = backend.run(transpiled_circuit, shots=shots)
            result = job.result()
            execution_time = time.time() - start_time
            counts = result.get_counts(transpiled_circuit)
            
            return {
                "status": "success",
                "counts": counts,
                "circuit_drawing": circuit_drawing,
                "backend_name": backend_name,
                "execution_time": execution_time
            }
            
        else:
            if not HAS_IBM_PROVIDER or not HAS_IBM_RUNTIME:
                return {
                    "status": "error",
                    "message": "IBM Quantum provider not available",
                    "circuit_drawing": circuit_drawing,
                    "backend_name": backend_name
                }
            
            try:
                service = QiskitRuntimeService()
                start_time = time.time()
                
                with Session(service=service, backend=backend_name):
                    sampler = Sampler()
                    job = sampler.run(circuits=circuit, shots=shots)
                    result = job.result()
                
                execution_time = time.time() - start_time
                counts = result.quasi_dists[0]
                
                formatted_counts = {}
                for bitstring, probability in counts.items():
                    count = int(round(probability * shots))
                    if count > 0:
                        binary = format(bitstring, f'0{circuit.num_clbits}b')
                        formatted_counts[binary] = count
                
                return {
                    "status": "success",
                    "counts": formatted_counts,
                    "circuit_drawing": circuit_drawing,
                    "backend_name": backend_name,
                    "execution_time": execution_time
                }
                
            except Exception as e:
                return {
                    "status": "error",
                    "message": str(e),
                    "circuit_drawing": circuit_drawing,
                    "backend_name": backend_name
                }
    
    except QiskitError as e:
        error_message = str(e)
        try:
            circuit = QuantumCircuit.from_qasm_str(qasm_code)
            circuit_drawing = str(circuit.draw(output='text'))
        except:
            circuit_drawing = "Could not generate circuit drawing"
        
        return {
            "status": "error",
            "message": error_message,
            "circuit_drawing": circuit_drawing,
            "backend_name": backend_name
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "circuit_drawing": "Could not generate circuit drawing",
            "backend_name": backend_name
        }