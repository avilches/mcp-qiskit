"""
Circuit Execution Module

This module provides functionality to execute quantum circuits on Qiskit backends.
"""
import time
from qiskit import QuantumCircuit, transpile
from qiskit.exceptions import QiskitError

try:
    # For newer versions of Qiskit
    from qiskit_aer import Aer
    HAS_AER = True
except ImportError:
    try:
        # For older versions of Qiskit
        from qiskit import Aer
        HAS_AER = True
    except ImportError:
        # If neither works, we'll handle this later
        Aer = None
        HAS_AER = False

try:
    from qiskit_ibm_provider import IBMProvider
    try:
        # Import the Runtime primitives - these are needed for real quantum devices
        from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler
        HAS_IBM_RUNTIME = True
    except ImportError:
        HAS_IBM_RUNTIME = False
    HAS_IBM_PROVIDER = True
except ImportError:
    HAS_IBM_PROVIDER = False
    HAS_IBM_RUNTIME = False

def execute_circuit(qasm_code, shots=1024, backend_name="aer_simulator"):
    """
    Execute a quantum circuit on a Qiskit backend

    Args:
        qasm_code: OpenQASM 2.0 code for the circuit to execute
        shots: Number of times to run the circuit (default: 1024)
        backend_name: Name of the backend to use (default: aer_simulator)

    Returns:
        Dict containing execution results including counts, circuit drawing,
        backend name, and execution time
    """
    try:
        # Create circuit from QASM
        circuit = QuantumCircuit.from_qasm_str(qasm_code)
        
        # Generate circuit drawing early so it's available even if there's an error
        try:
            circuit_drawing = circuit.draw(output='text').single_string()
        except:
            # Fallback for older Qiskit versions
            circuit_drawing = str(circuit.draw(output='text'))
        
        # Determine if using IBM backend or local Aer
        if backend_name.startswith("aer_") or backend_name == "qasm_simulator":
            # Check if Aer is available
            if not HAS_AER:
                # Return a user-friendly response instead of raising an exception
                return {
                    "status": "error",
                    "message": "Local simulator not available. Please install qiskit-aer with: pip install qiskit-aer",
                    "circuit_drawing": circuit_drawing,
                    "backend_name": backend_name
                }
            
            # Get the available backend
            try:
                backend = Aer.get_backend(backend_name)
            except Exception as e:
                # If the requested backend isn't available, fall back to qasm_simulator
                if backend_name != "qasm_simulator":
                    try:
                        backend = Aer.get_backend("qasm_simulator")
                        backend_name = "qasm_simulator (fallback)"
                    except Exception as fallback_error:
                        # If even qasm_simulator is not available
                        return {
                            "status": "error",
                            "message": f"No simulator available: {str(fallback_error)}. Please check your qiskit-aer installation.",
                            "circuit_drawing": circuit_drawing,
                            "backend_name": backend_name
                        }
                else:
                    # If specifically qasm_simulator was requested but not available
                    return {
                        "status": "error",
                        "message": f"Requested simulator '{backend_name}' not available: {str(e)}. Please check your qiskit-aer installation.",
                        "circuit_drawing": circuit_drawing,
                        "backend_name": backend_name
                    }
            
            # Record the start time
            start_time = time.time()

            # Transpile the circuit for the backend
            transpiled_circuit = transpile(circuit, backend)

            # Execute the circuit - Updated for Qiskit 1.0+
            job = backend.run(transpiled_circuit, shots=shots)

            # Get the results
            result = job.result()

            # Calculate execution time
            execution_time = time.time() - start_time

            # Get counts from the result
            counts = result.get_counts(transpiled_circuit)
            
            return {
                "status": "success",
                "counts": counts,
                "circuit_drawing": circuit_drawing,
                "backend_name": backend_name,
                "execution_time": execution_time
            }
            
        else:
            # Using a real IBM quantum device - need to use the new Runtime primitives
            
            # Check if IBM provider is available
            if not HAS_IBM_PROVIDER:
                # Return a user-friendly response instead of raising an exception
                return {
                    "status": "error",
                    "message": "IBM Quantum provider not available. Please install with: pip install qiskit-ibm-provider",
                    "circuit_drawing": circuit_drawing,
                    "backend_name": backend_name
                }
            
            # Check if IBM Runtime is available
            if not HAS_IBM_RUNTIME:
                return {
                    "status": "error",
                    "message": "IBM Quantum Runtime not available. Please install with: pip install qiskit-ibm-runtime",
                    "circuit_drawing": circuit_drawing,
                    "backend_name": backend_name
                }
            
            # Get the IBM backend using the new Runtime service
            try:
                # Initialize the runtime service
                service = QiskitRuntimeService()
                
                # Record the start time
                start_time = time.time()
                
                # Execute using the Sampler primitive in a session
                with Session(service=service, backend=backend_name):
                    sampler = Sampler()
                    job = sampler.run(circuits=circuit, shots=shots)
                    result = job.result()
                
                # Calculate execution time
                execution_time = time.time() - start_time
                
                # Extract counts from the Sampler result
                counts = result.quasi_dists[0]
                # Convert to the traditional Qiskit format
                formatted_counts = {}
                for bitstring, probability in counts.items():
                    # Convert integer keys to bitstrings and multiply by shots to get counts
                    count = int(round(probability * shots))
                    if count > 0:  # Only include non-zero counts
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
                    "message": f"Error using IBM Quantum Runtime: {str(e)}. Make sure you have the right access permissions.",
                    "circuit_drawing": circuit_drawing,
                    "backend_name": backend_name
                }
    
    except QiskitError as e:
        # Create a more user-friendly error message
        error_message = f"Qiskit error: {str(e)}"
        try:
            # Try to get the circuit drawing even if there was an error
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
        error_message = f"Error executing circuit: {str(e)}"
        try:
            # Try to get the circuit drawing even if there was an error
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