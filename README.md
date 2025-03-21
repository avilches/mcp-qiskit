# Qiskit MCP

Quantum circuit integration using Model Context Protocol (MCP) endpoints.

## About

This project connects quantum computing capabilities to LLMs through a simple MCP interface. Built with Qiskit, it lets you create and run quantum circuits from natural language instructions.

## Key capabilities

- Bell state circuit generation
- OpenQASM 2.0 circuit creation
- Circuit execution on simulators or IBM Quantum hardware
- Backend discovery

## Prerequisites

- Python 3.10+
- Qiskit libraries
- FastMCP
- httpx

## Setup

1. Clone the repo:

```bash
git clone https://github.com/yourusername/mcp-qiskit.git
cd mcp-qiskit
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running

Launch the server with:

```bash
python main.py
```

## Claude Desktop integration

To use with Claude Desktop:

1. Add to your Claude config:

```json
{
  "mcp_servers": [
    {
      "name": "Qiskit",
      "path": "/path/to/mcp-qiskit/run_server.sh"
    }
  ]
}
```

2. Restart Claude Desktop

## MCP endpoints

The server provides these functions:

- `list_backends` - Shows available Qiskit backends
- `create_bell_circuit` - Creates a basic entanglement circuit
- `create_custom_circuit` - Builds a circuit from OpenQASM code
- `execute_circuit` - Runs circuits and returns measurement results


## License

CC0 (Creative Commons Zero)