#!/usr/bin/env python3
'''
Qiskit MCP Server
'''

import json
import sys
import logging
from typing import Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)

logger = logging.getLogger("qiskit-mcp")

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    logger.error(f"FastMCP import failed: {e}")
    sys.exit(1)

from tools.ibm_token import load_token
from tools.bell_circuit import create_bell_circuit, get_bell_circuit_ascii
from tools.custom_circuit import create_custom_circuit
from tools.execute_circuit import execute_circuit
from tools.list_backends import list_available_backends

# Create MCP server
mcp = FastMCP(
    "qiskit", 
    instructions="Quantum computing API for circuit creation and execution", 
    host="0.0.0.0", 
    port=8000
)

# Load token if available
try:
    token_status = load_token()
    logger.info(f"IBM token: {token_status['status']}")
except Exception as e:
    logger.warning(f"Token loading failed: {e}")

# Register MCP tools
@mcp.tool(name="list_backends", description="Lists available Qiskit backends")
def list_backends() -> Dict:
    return list_available_backends()

@mcp.tool(name="create_bell_circuit", description="Creates a Bell state entanglement circuit")
def bell_circuit() -> Dict:
    circuit = create_bell_circuit()
    return {
        "circuit_representation": str(circuit),
        "circuit_drawing": get_bell_circuit_ascii()
    }

@mcp.tool(name="create_custom_circuit", description="Creates a circuit from OpenQASM 2.0 code")
def custom_circuit(instructions: str) -> Dict:
    circuit = create_custom_circuit(instructions)
    circuit_drawing = str(circuit.draw(output='text'))
    return {
        "circuit_representation": str(circuit),
        "circuit_drawing": circuit_drawing,
        "num_qubits": circuit.num_qubits,
        "num_clbits": circuit.num_clbits
    }

@mcp.tool(name="execute_circuit", description="Runs a circuit on a Qiskit backend")
def run_circuit(qasm_code: str, shots: int = 1024, backend: str = "aer_simulator") -> Dict:
    return execute_circuit(qasm_code, shots, backend)

if __name__ == "__main__":
    try:
        logger.info("Starting Qiskit MCP server")
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)