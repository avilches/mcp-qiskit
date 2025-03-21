#!/bin/bash

# Full path to the project directory
PROJECT_DIR="/Users/avilches/Work/Proy/IBM/mcp-qiskit2/mcp-qiskit"

# Activate virtual environment and run the Python script
source "${PROJECT_DIR}/venv_pip/bin/activate"
export PYTHONPATH="${PROJECT_DIR}"
cd "${PROJECT_DIR}"
python "${PROJECT_DIR}/main.py"