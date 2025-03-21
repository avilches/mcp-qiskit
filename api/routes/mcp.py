#!/usr/bin/env python3
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

router = APIRouter()

@router.get("/mcp.json", response_model=dict)
async def get_mcp():
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "mcp_definition.json")
    with open(json_path, 'r') as f:
        return json.load(f)

@router.post(
    "/function", 
    response_model=Union[CircuitResponse, CustomCircuitResponse, CircuitExecutionResponse, BackendsListResponse], 
    responses={400: {"model": ErrorResponse}}
)
async def call_function(request: FunctionRequest):
    function_name = request.name
    parameters = request.parameters or {}
    
    if function_name == "List available backends":
        try:
            return list_available_backends()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
            
    elif function_name == "Create a bell quantum circuit":
        try:
            circuit = create_bell_circuit()
            return {
                "circuit_representation": str(circuit),
                "circuit_drawing": get_bell_circuit_ascii()
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    elif function_name == "Create a custom quantum circuit":
        try:
            instructions = parameters.get("instructions", "")
            
            if not instructions:
                raise ValueError("Missing instructions parameter")
            
            circuit = create_custom_circuit(instructions)
            circuit_drawing = str(circuit.draw(output='text'))
            
            return {
                "circuit_representation": str(circuit),
                "circuit_drawing": circuit_drawing,
                "num_qubits": circuit.num_qubits,
                "num_clbits": circuit.num_clbits
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    elif function_name == "Execute quantum circuit":
        try:
            qasm_code = parameters.get("qasm_code", "")
            if not qasm_code:
                raise ValueError("Missing qasm_code parameter")
            
            shots = parameters.get("shots", 1024)
            backend = parameters.get("backend", "aer_simulator")
            
            return execute_circuit(qasm_code, shots, backend)
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "circuit_drawing": "Could not generate circuit drawing",
                "backend_name": parameters.get("backend", "aer_simulator"),
                "execution_time": None,
                "counts": None
            }
    
    else:
        raise HTTPException(status_code=400, detail=f"Unknown function: {function_name}")