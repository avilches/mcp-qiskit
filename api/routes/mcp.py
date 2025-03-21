"""MCP API Routes

Routes for serving the MCP schema definition and function endpoints.
"""
import json
import os
from typing import Union
from fastapi import APIRouter, HTTPException
from ..models import (
    FunctionRequest, CircuitResponse, CustomCircuitResponse, 
    CircuitExecutionResponse, BackendsListResponse, ErrorResponse
)
from circuits.bell_circuit import create_bell_circuit, get_bell_circuit_ascii
from circuits.custom_circuit import create_custom_circuit
from circuits.execute_circuit import execute_circuit
from circuits.list_backends import list_available_backends
from circuits.ibm_token import load_token

router = APIRouter()

@router.get("/mcp.json", response_model=dict)
async def get_mcp():
    """Returns the MCP schema definition"""
    # Load MCP definition from JSON file
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "mcp_definition.json")
    with open(json_path, 'r') as f:
        return json.load(f)

@router.post(
    "/function", 
    response_model=Union[CircuitResponse, CustomCircuitResponse, CircuitExecutionResponse, BackendsListResponse], 
    responses={400: {"model": ErrorResponse}}
)
async def call_function(request: FunctionRequest):
    """Execute a function based on the MCP function name and parameters"""
    function_name = request.name
    parameters = request.parameters or {}
    
    # Handle List Backends function
    if function_name == "List available backends":
        try:
            result = list_available_backends()
            return result
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error listing backends: {str(e)}")
            
    # Handle Bell circuit function
    elif function_name == "Create a bell quantum circuit":
        try:
            circuit = create_bell_circuit()
            return {
                "circuit_representation": str(circuit),
                "circuit_drawing": get_bell_circuit_ascii()
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating Bell circuit: {str(e)}")
    
    # Handle custom circuit function
    elif function_name == "Create a custom quantum circuit":
        try:
            instructions = parameters.get("instructions", "")
            
            if not instructions:
                raise ValueError("Instructions parameter is required")
            
            circuit = create_custom_circuit(instructions)
            
            # Generate the circuit drawing as a string
            circuit_drawing = str(circuit.draw(output='text'))
            
            return {
                "circuit_representation": str(circuit),
                "circuit_drawing": circuit_drawing,
                "num_qubits": circuit.num_qubits,
                "num_clbits": circuit.num_clbits
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating custom circuit: {str(e)}")
    
    # Handle circuit execution function
    elif function_name == "Execute quantum circuit":
        try:
            qasm_code = parameters.get("qasm_code", "")
            if not qasm_code:
                raise ValueError("qasm_code parameter is required")
            
            shots = parameters.get("shots", 1024)
            backend = parameters.get("backend", "aer_simulator")
            
            # Execute the circuit and return the result directly
            # Our updated model will handle both success and error responses
            return execute_circuit(qasm_code, shots, backend)
            
        except Exception as e:
            # If we get an unexpected exception, create a response with error information
            error_message = f"Error executing circuit: {str(e)}"
            return {
                "status": "error",
                "message": error_message,
                "error": error_message,
                "circuit_drawing": "Error: Could not generate circuit drawing",
                "backend_name": backend,
                "execution_time": None,
                "counts": None
            }
    
    # Handle unknown function
    else:
        raise HTTPException(status_code=400, detail=f"Unknown function: {function_name}")