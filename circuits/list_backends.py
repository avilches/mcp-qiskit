"""
Backend Listing Module

This module provides functionality to list available Qiskit backends.
"""
# Try different ways to import Aer based on Qiskit version
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
        HAS_AER = False

try:
    from qiskit_ibm_provider import IBMProvider
    HAS_IBM_PROVIDER = True
except ImportError:
    HAS_IBM_PROVIDER = False

def list_available_backends():
    """
    Lists all available Qiskit backends that the user has access to
    
    Returns:
        Dict containing list of available backends and active account information
    """
    backends = []
    active_account = "No IBMQ account configured"
    
    # Add local simulators if Aer is available
    if HAS_AER:
        try:
            local_backends = [backend.name() for backend in Aer.backends()]
            backends.extend([f"aer_{backend}" for backend in local_backends])
        except Exception as e:
            backends.append(f"Error getting Aer backends: {str(e)}")
    else:
        backends.append("No Aer simulators available - install with: pip install qiskit-aer")
    
    # Try to get IBM Quantum backends if the provider is available
    if HAS_IBM_PROVIDER:
        try:
            # Try to load an account from disk
            provider = IBMProvider()
            quantum_backends = [backend.name for backend in provider.backends()]
            backends.extend(quantum_backends)
            active_account = f"IBM Quantum account: {provider.active_account()}"
        except Exception as e:
            # No saved account or other error
            active_account = f"IBM Quantum error: {str(e)}"
    else:
        active_account += " (qiskit_ibm_provider not installed)"
    
    return {
        "backends": backends,
        "active_account": active_account
    }