"""API Data Models

Pydantic models for request/response validation and documentation.
"""
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field

# Request Models
class FunctionRequest(BaseModel):
    """Base model for function requests"""
    name: str = Field(..., description="The name of the function to call")
    parameters: Optional[Dict[str, Any]] = Field(default={}, description="Function parameters")

# Response Models
class CircuitResponse(BaseModel):
    """Response model for quantum circuit functions"""
    circuit_representation: str = Field(..., description="String representation of the quantum circuit")
    circuit_drawing: str = Field(..., description="ASCII art representation of the circuit")
    
class CustomCircuitResponse(CircuitResponse):
    """Response model for custom quantum circuit functions with additional metadata"""
    num_qubits: int = Field(..., description="Number of qubits in the circuit")
    num_clbits: int = Field(..., description="Number of classical bits in the circuit")

class CircuitExecutionResponse(BaseModel):
    """Response model for quantum circuit execution"""
    status: Optional[str] = Field(default="success", description="Status of the execution (success or error)")
    counts: Optional[Dict[str, int]] = Field(default=None, description="Measurement results as a dictionary of bit strings and counts")
    circuit_drawing: str = Field(..., description="ASCII art representation of the executed circuit")
    backend_name: str = Field(..., description="Name of the backend used for execution")
    execution_time: Optional[float] = Field(default=None, description="Time taken to execute the circuit in seconds")
    message: Optional[str] = Field(default=None, description="Error message if status is error")
    error: Optional[str] = Field(default=None, description="Error message if status is error (alternative format)")
    
class BackendsListResponse(BaseModel):
    """Response model for listing available backends"""
    backends: List[str] = Field(..., description="List of available backend names")
    active_account: str = Field(..., description="Information about the currently active account, if any")
    

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")