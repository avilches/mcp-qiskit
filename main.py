"""
Qiskit MCP Server

A FastMCP server that exposes quantum circuit functionality as Model Context Protocol (MCP) endpoints.
"""

from typing import Any, Dict
import json
import httpx
import sys
import logging

# Set up logging to stdout and stderr
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)

# Create specific logger
logger = logging.getLogger("qiskit-mcp")
logger.setLevel(logging.DEBUG)

try:
    from mcp.server.fastmcp import FastMCP
    logger.info("Successfully imported FastMCP")
except ImportError as e:
    logger.error(f"Failed to import FastMCP: {e}")
    sys.exit(1)
from circuits.ibm_token import load_token
from circuits.bell_circuit import create_bell_circuit, get_bell_circuit_ascii
from circuits.custom_circuit import create_custom_circuit
from circuits.execute_circuit import execute_circuit
from circuits.list_backends import list_available_backends

# Initialize FastMCP server
mcp = FastMCP("qiskit", instructions="A quantum computing API that allows you to create and execute quantum circuits using Qiskit.")

# Load IBM Quantum token at startup
try:
    token_status = load_token()
    logger.info(f"IBM Quantum token status: {token_status['status']} - {token_status['message']}")
except Exception as e:
    logger.error(f"Error loading IBM Quantum token: {str(e)}", exc_info=True)

# Register tools with FastMCP

@mcp.tool(name="list_backends", description="Lists all available Qiskit backends that the user has access to")
def list_backends() -> Dict:
    """List all available Qiskit backends."""
    return list_available_backends()

@mcp.tool(name="create_bell_circuit", description="Creates a quantum circuit that prepares a Bell state (entangled state)")
def bell_circuit() -> Dict:
    """Create a Bell state quantum circuit."""
    circuit = create_bell_circuit()
    return {
        "circuit_representation": str(circuit),
        "circuit_drawing": get_bell_circuit_ascii()
    }

@mcp.tool(name="create_custom_circuit", description="Creates a custom quantum circuit based on OpenQASM 2.0 code")
def custom_circuit(instructions: str) -> Dict:
    """Create a custom quantum circuit from OpenQASM 2.0 instructions."""
    circuit = create_custom_circuit(instructions)
    circuit_drawing = str(circuit.draw(output='text'))
    return {
        "circuit_representation": str(circuit),
        "circuit_drawing": circuit_drawing,
        "num_qubits": circuit.num_qubits,
        "num_clbits": circuit.num_clbits
    }

@mcp.tool(name="execute_circuit", description="Executes a quantum circuit on a Qiskit backend and returns the results")
def run_circuit(qasm_code: str, shots: int = 1024, backend: str = "aer_simulator") -> Dict:
    """Execute a quantum circuit on a specified backend."""
    return execute_circuit(qasm_code, shots, backend)

if __name__ == "__main__":
    try:
        # Run the FastMCP server with SSE transport
        logger.info("Starting FastMCP server with SSE transport")
        mcp.run(transport="sse")
    except Exception as e:
        logger.error(f"Error running MCP server: {str(e)}", exc_info=True)
        sys.exit(1)
