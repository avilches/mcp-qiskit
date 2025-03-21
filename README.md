# MCP Qiskit 

A FastMCP server that exposes quantum circuit functionality as Model Context Protocol (MCP) endpoints.

## Overview

This project provides a FastMCP server that allows you to interact with quantum circuits through a simple API. It leverages Qiskit to create, manipulate, and execute quantum circuits, and exposes these capabilities through the Model Context Protocol (MCP).

## Features

- Create Bell state quantum circuits
- Create custom quantum circuits using OpenQASM 2.0 code
- Execute quantum circuits on local simulators or real IBM Quantum backends
- List available Qiskit backends

## Requirements

- Python 3.10 or newer
- Qiskit
- FastMCP (mcp[cli])
- httpx

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/mcp-qiskit.git
cd mcp-qiskit
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

To start the MCP server, run:

```bash
python main.py
```

The server will start at `http://0.0.0.0:3000`.

### Testing the Server

A test client is included to verify the functionality of the server. You can run it with:

```bash
python test_client.py
```

By default, it runs only the basic tests that don't require an IBM Quantum token. To include IBM Quantum tests, you can provide a token:

```bash
python test_client.py --mode all --token YOUR_IBM_QUANTUM_TOKEN
```

## MCP Functions

The server exposes the following functions through the MCP schema:

1. **List available backends** - List all available Qiskit backends
2. **Create a bell quantum circuit** - Create a Bell state circuit (a basic entanglement circuit)
3. **Create a custom quantum circuit** - Create a circuit from OpenQASM 2.0 code
4. **Execute quantum circuit** - Run a circuit on a Qiskit backend and get measurement results

## API

The API follows the MCP specification. You can get the full MCP schema by sending a GET request to `/mcp.json`.

To call a function, send a POST request to `/function` with a JSON payload containing the function name and parameters.

Example:

```bash
curl -X POST http://localhost:3000/function \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Create a bell quantum circuit",
    "parameters": {}
  }'
```

## License

[MIT License](LICENSE)