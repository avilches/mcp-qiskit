#!/usr/bin/env python3

# Handle different Qiskit versions
try:
    from qiskit_aer import Aer
    HAS_AER = True
except ImportError:
    try:
        from qiskit import Aer
        HAS_AER = True
    except ImportError:
        HAS_AER = False

try:
    from qiskit_ibm_provider import IBMProvider
    HAS_IBM_PROVIDER = True
except ImportError:
    HAS_IBM_PROVIDER = False

def list_available_backends():
    backends = []
    active_account = "No IBM account configured"
    
    if HAS_AER:
        try:
            local_backends = [backend.name() for backend in Aer.backends()]
            backends.extend([f"aer_{backend}" for backend in local_backends])
        except Exception as e:
            backends.append(f"Aer error: {str(e)}")
    else:
        backends.append("No simulators available")
    
    if HAS_IBM_PROVIDER:
        try:
            provider = IBMProvider()
            quantum_backends = [backend.name for backend in provider.backends()]
            backends.extend(quantum_backends)
            active_account = f"IBM account: {provider.active_account()}"
        except Exception as e:
            active_account = f"IBM error: {str(e)}"
    
    return {
        "backends": backends,
        "active_account": active_account
    }