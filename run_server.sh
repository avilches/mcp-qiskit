#!/bin/bash
# Script to run the MCP server directly with full output

echo "Starting MCP server..."

# Set up Python path
export PYTHONPATH="/Users/avilches/Work/Proy/IBM/mcp-qiskit2/mcp-qiskit"

# Run the server
/Users/avilches/.local/share/uv/python/cpython-3.10.13-macos-aarch64-none/bin/python3.10 \
    /Users/avilches/Work/Proy/IBM/mcp-qiskit2/mcp-qiskit/main.py