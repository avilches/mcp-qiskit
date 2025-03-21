#!/usr/bin/env python3
"""
Test Client for the MCP Qiskit API

This script tests the MCP API by calling its endpoints with various circuit creation and execution requests.
The client supports two test modes: basic (without IBM Quantum token) and full (with IBM Quantum token).
"""

import requests
import json
import sys
import argparse

def test_mcp_definition(base_url):
    """Get and print the MCP definition
    
    Args:
        base_url: Base URL of the MCP server (e.g., http://localhost:3000)
    """
    # Get the MCP definition
    mcp_url = f"{base_url}/mcp.json"
    try:
        mcp_response = requests.get(mcp_url)
        print("MCP Definition Response:")
        print(json.dumps(mcp_response.json(), indent=2))
        print("\n" + "-"*50 + "\n")
        return True
    except Exception as e:
        print(f"Error getting MCP definition: {e}")
        return False


def list_backends(base_url):
    """List available quantum backends
    
    Args:
        base_url: Base URL of the MCP server
    Returns:
        list: List of available backends or None if error
    """
    print("TESTING LIST BACKENDS FUNCTION\n" + "-"*30)
    
    function_url = f"{base_url}/function"
    function_data = {
        "name": "List available backends"
    }
    
    try:
        function_response = requests.post(function_url, json=function_data)
        if function_response.status_code == 200:
            result = function_response.json()
            
            print("Available backends:")
            backends = result.get("backends", [])
            for backend in backends:
                print(f"  - {backend}")
                
            print(f"\nAccount information:")
            print(f"  {result.get('active_account', 'No account information')}")
            
            print("\n" + "="*50 + "\n")
            return backends
        else:
            print(f"Error: HTTP {function_response.status_code}")
            print(function_response.text)
            
            print("\n" + "="*50 + "\n")
            return None
    except Exception as e:
        print(f"Error listing backends: {e}")
        print("\n" + "="*50 + "\n")
        return None

def create_bell_circuit(base_url):
    """Create a Bell circuit
    
    Args:
        base_url: Base URL of the MCP server
    """
    print("TESTING BELL CIRCUIT FUNCTION\n" + "-"*30)
    
    function_url = f"{base_url}/function"
    function_data = {
        "name": "Create a bell quantum circuit"
    }
    
    try:
        function_response = requests.post(function_url, json=function_data)
        if function_response.status_code == 200:
            result = function_response.json()
            
            print("Function Response:")
            print(json.dumps(result, indent=2))
            
            # Display the circuit drawing specially
            if "circuit_drawing" in result:
                print("\nCircuit Drawing:")
                print(result["circuit_drawing"])
        else:
            print(f"Error: HTTP {function_response.status_code}")
            print(function_response.text)
            
        print("\n" + "="*50 + "\n")
        return function_response.status_code == 200
    except Exception as e:
        print(f"Error calling Bell circuit function: {e}")
        print("\n" + "="*50 + "\n")
        return False

def create_custom_circuit(base_url):
    """Create a custom circuit
    
    Args:
        base_url: Base URL of the MCP server
    """
    print("TESTING CUSTOM CIRCUIT WITH OPENQASM\n" + "-"*30)
    
    # Create a GHZ state using OpenQASM
    qasm_code = """OPENQASM 2.0;
include "qelib1.inc";

// GHZ state preparation for 3 qubits
qreg q[3];
creg c[3];

// Apply Hadamard to the first qubit
h q[0];

// Apply CNOTs to entangle all qubits
cx q[0], q[1];
cx q[0], q[2];

// Measure all qubits
measure q -> c;"""
    
    function_url = f"{base_url}/function"
    function_data = {
        "name": "Create a custom quantum circuit",
        "parameters": {
            "instructions": qasm_code
        }
    }
    
    try:
        function_response = requests.post(function_url, json=function_data)
        if function_response.status_code == 200:
            result = function_response.json()
            
            print("Function Response:")
            # Print QASM code used
            print("QASM code used:")
            print(qasm_code)
            print()
            print(json.dumps(result, indent=2))
            
            # Display the circuit drawing specially
            if "circuit_drawing" in result:
                print("\nCircuit Drawing:")
                print(result["circuit_drawing"])
        else:
            print(f"Error: HTTP {function_response.status_code}")
            print(function_response.text)
            
        print("\n" + "="*50 + "\n")
        return function_response.status_code == 200, qasm_code
    except Exception as e:
        print(f"Error calling custom circuit function with QASM: {e}")
        print("\n" + "="*50 + "\n")
        return False, None

def execute_circuit_local(base_url, qasm_code=None):
    """Execute a circuit on a local simulator
    
    Args:
        base_url: Base URL of the MCP server
        qasm_code: OpenQASM code to execute (optional)
    """
    print("TESTING EXECUTE CIRCUIT ON LOCAL SIMULATOR\n" + "-"*30)
    
    # Use provided QASM code or create a Bell state for execution
    if qasm_code is None:
        qasm_code = """OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];
creg c[2];

h q[0];
cx q[0], q[1];
measure q -> c;"""
    
    function_url = f"{base_url}/function"
    function_data = {
        "name": "Execute quantum circuit",
        "parameters": {
            "qasm_code": qasm_code,
            "shots": 1024,
            "backend": "aer_simulator"
        }
    }
    
    try:
        function_response = requests.post(function_url, json=function_data)
        if function_response.status_code == 200:
            result = function_response.json()
            
            print("Function Response:")
            # Print QASM code used
            print("QASM code used:")
            print(qasm_code)
            print()
            
            status = result.get("status", "")
            if status == "error":
                # Handle error response
                error_message = result.get("message") or result.get("error", "Unknown error")
                print(f"ERROR: {error_message}")
                print()
                print(f"Backend: {result.get('backend_name')}")
                
                # Display the circuit drawing if available
                if "circuit_drawing" in result:
                    print("\nCircuit Drawing:")
                    print(result["circuit_drawing"])
            else:
                # Display successful execution results
                # Format the counts as a table
                print("Execution Results:")
                counts = result.get("counts", {})
                if counts:
                    for state, count in counts.items():
                        print(f"  {state}: {count}")
                else:
                    print("  No counts available")
                
                print(f"\nBackend: {result.get('backend_name')}")
                execution_time = result.get("execution_time")
                if execution_time is not None:
                    print(f"Execution time: {execution_time:.6f} seconds")
                
                # Display the circuit drawing
                if "circuit_drawing" in result:
                    print("\nCircuit Drawing:")
                    print(result["circuit_drawing"])
        else:
            print(f"Error: HTTP {function_response.status_code}")
            print(function_response.text)
            
        print("\n" + "="*50 + "\n")
        return function_response.status_code == 200
    except Exception as e:
        print(f"Error executing quantum circuit: {e}")
        print("\n" + "="*50 + "\n")
        return False

def execute_circuit_ibm(base_url, backend_name, qasm_code=None):
    """Execute a circuit on an IBM Quantum backend
    
    Args:
        base_url: Base URL of the MCP server
        backend_name: Name of the IBM Quantum backend to use
        qasm_code: OpenQASM code to execute (optional)
    """
    print(f"TESTING EXECUTE CIRCUIT ON IBM BACKEND: {backend_name}\n" + "-"*30)
    
    # Use provided QASM code or create a Bell state for execution
    if qasm_code is None:
        qasm_code = """OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];
creg c[2];

h q[0];
cx q[0], q[1];
measure q -> c;"""
    
    function_url = f"{base_url}/function"
    function_data = {
        "name": "Execute quantum circuit",
        "parameters": {
            "qasm_code": qasm_code,
            "shots": 1024,
            "backend": backend_name
        }
    }
    
    try:
        function_response = requests.post(function_url, json=function_data)
        if function_response.status_code == 200:
            result = function_response.json()
            
            print("Function Response:")
            # Print QASM code used
            print("QASM code used:")
            print(qasm_code)
            print()
            
            status = result.get("status", "")
            if status == "error":
                # Handle error response
                error_message = result.get("message") or result.get("error", "Unknown error")
                print(f"ERROR: {error_message}")
                print()
                print(f"Backend: {result.get('backend_name')}")
                
                # Display the circuit drawing if available
                if "circuit_drawing" in result:
                    print("\nCircuit Drawing:")
                    print(result["circuit_drawing"])
            else:
                # Display successful execution results
                # Format the counts as a table
                print("Execution Results:")
                counts = result.get("counts", {})
                if counts:
                    for state, count in counts.items():
                        print(f"  {state}: {count}")
                else:
                    print("  No counts available")
                
                print(f"\nBackend: {result.get('backend_name')}")
                execution_time = result.get("execution_time")
                if execution_time is not None:
                    print(f"Execution time: {execution_time:.6f} seconds")
                
                # Display the circuit drawing
                if "circuit_drawing" in result:
                    print("\nCircuit Drawing:")
                    print(result["circuit_drawing"])
        else:
            print(f"Error: HTTP {function_response.status_code}")
            print(function_response.text)
            
        print("\n" + "="*50 + "\n")
        return function_response.status_code == 200
    except Exception as e:
        print(f"Error executing quantum circuit on IBM backend: {e}")
        print("\n" + "="*50 + "\n")
        return False

def test_basic_functions(base_url):
    """Test basic Qiskit functions that don't require an IBM Quantum token
    
    Args:
        base_url: Base URL of the MCP server
    """
    print("\n\n==== TESTING BASIC FUNCTIONS (NO IBM TOKEN REQUIRED) ====\n\n")
    
    if not test_mcp_definition(base_url):
        print("Failed to get MCP definition, stopping tests.")
        return False
    
    # Test creating a Bell circuit
    create_bell_circuit(base_url)
    
    # Test creating a custom circuit
    success, qasm_code = create_custom_circuit(base_url)
    
    # Test executing a circuit on local simulator
    if success and qasm_code:
        execute_circuit_local(base_url, qasm_code)
    else:
        execute_circuit_local(base_url)
    
    return True

def test_ibm_functions(base_url):
    """Test IBM Quantum functions that require a token
    
    Args:
        base_url: Base URL of the MCP server
    """
    print("\n\n==== TESTING IBM QUANTUM FUNCTIONS (TOKEN REQUIRED) ====\n\n")
    
    # Use existing token from ~/.qiskit/config.json if available
    print("Using token from ~/.qiskit/config.json if available.")
    
    # List available backends
    backends = list_backends(base_url)
    if not backends:
        print("Failed to list backends, skipping IBM execution test.")
        return False
    
    # Find an IBM backend to use
    ibm_backend = None
    real_backends = []
    
    for backend in backends:
        # Skip error messages or warnings that might be in the backends list
        if isinstance(backend, str) and not backend.startswith("Error") and not backend.startswith("No Aer"):
            # Identify real quantum backends (not local simulators)
            if not backend.startswith('aer_') and backend != 'qasm_simulator':
                real_backends.append(backend)
    
    if real_backends:
        ibm_backend = real_backends[0]
        print(f"Found {len(real_backends)} IBM backend(s). Using: {ibm_backend}")
    else:
        print("No IBM real backends found, falling back to simulator.")
        # Fall back to simulator if no real backends found
        for backend in backends:
            if isinstance(backend, str) and (backend.startswith('aer_') or backend == 'qasm_simulator'):
                ibm_backend = backend
                break
    
    if not ibm_backend:
        print("No usable backends found, skipping execution test.")
        return False
    
    # Create a custom circuit for IBM execution
    success, qasm_code = create_custom_circuit(base_url)
    
    # Execute the circuit on an IBM backend
    if success and qasm_code:
        execute_circuit_ibm(base_url, ibm_backend, qasm_code)
    else:
        execute_circuit_ibm(base_url, ibm_backend)
    
    return True

def main():
    """Main function that parses command line arguments and runs the tests"""
    parser = argparse.ArgumentParser(description="Test the MCP Qiskit API")
    parser.add_argument("--url", default="http://localhost:3000", help="Base URL of the MCP server")
    parser.add_argument("--mode", default="basic", choices=["basic", "ibm", "all"], 
                        help="Test mode: basic (no token required), ibm (token required), or all")
    parser.add_argument("--token", help="IBM Quantum API token not needed anymore as you can't save it via API. Token will be loaded from ~/.qiskit/config.json if available", dest="unused_token")
    
    args = parser.parse_args()
    
    print(f"Testing MCP server at {args.url}")
    
    if args.mode == "basic" or args.mode == "all":
        test_basic_functions(args.url)
    
    if args.mode == "ibm" or args.mode == "all":
        test_ibm_functions(args.url)

if __name__ == "__main__":
    main()