#!/usr/bin/env python3
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class FunctionRequest(BaseModel):
    name: str = Field(..., description="Function name")
    parameters: Optional[Dict[str, Any]] = Field(default={}, description="Parameters")

class CircuitResponse(BaseModel):
    circuit_representation: str = Field(..., description="Circuit string representation")
    circuit_drawing: str = Field(..., description="ASCII circuit diagram")
    
class CustomCircuitResponse(CircuitResponse):
    num_qubits: int = Field(..., description="Qubit count")
    num_clbits: int = Field(..., description="Classical bit count")

class CircuitExecutionResponse(BaseModel):
    status: Optional[str] = Field(default="success", description="Execution status")
    counts: Optional[Dict[str, int]] = Field(default=None, description="Measurement counts")
    circuit_drawing: str = Field(..., description="Circuit diagram")
    backend_name: str = Field(..., description="Backend name")
    execution_time: Optional[float] = Field(default=None, description="Execution time (s)")
    message: Optional[str] = Field(default=None, description="Error details")
    
class BackendsListResponse(BaseModel):
    backends: List[str] = Field(..., description="Available backends")
    active_account: str = Field(..., description="Active account info")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")