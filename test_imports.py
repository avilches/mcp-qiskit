"""
Test script to verify imports are working correctly
"""
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)

try:
    logging.info("Testing imports...")
    
    # Test MCP imports
    logging.info("Importing FastMCP...")
    from mcp.server.fastmcp import FastMCP
    logging.info("FastMCP imported successfully")
    
    # Test Qiskit imports
    logging.info("Importing Qiskit...")
    from qiskit import QuantumCircuit
    logging.info("Qiskit imported successfully")
    
    # Test local module imports
    logging.info("Importing local modules...")
    from circuits.ibm_token import load_token
    from circuits.bell_circuit import create_bell_circuit
    logging.info("Local modules imported successfully")
    
    logging.info("All imports successful!")
except Exception as e:
    logging.error(f"Import error: {str(e)}", exc_info=True)
    sys.exit(1)