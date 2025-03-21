"""
IBM Quantum Account Management Module

This module provides functionality to load IBM Quantum API tokens.
"""
import os
import json
from pathlib import Path

try:
    from qiskit_ibm_provider import IBMProvider
    HAS_IBM_PROVIDER = True
except ImportError:
    HAS_IBM_PROVIDER = False

# Define config file path
CONFIG_DIR = Path.home() / '.qiskit'
CONFIG_FILE = CONFIG_DIR / 'config.json'

def load_token():
    """
    Loads the IBM Quantum API token from config file and initializes the provider
    
    Returns:
        Dict containing status and message about the token loading operation
    """
    if not HAS_IBM_PROVIDER:
        return {
            "status": "error",
            "message": "The qiskit_ibm_provider package is not installed. Please install it with 'pip install qiskit-ibm-provider'."
        }
    
    try:
        # Check if token already exists in provider
        try:
            provider = IBMProvider()
            account_info = provider.active_account()
            return {
                "status": "success",
                "message": f"IBM Quantum token loaded from saved credentials. Connected as {account_info.get('email', 'unknown')}."
            }
        except:
            # Try to load from config file
            if CONFIG_FILE.exists():
                try:
                    with open(CONFIG_FILE, 'r') as f:
                        config = json.load(f)
                    
                    if 'ibm_token' in config and config['ibm_token']:
                        token = config['ibm_token']
                        IBMProvider.save_account(token=token, overwrite=True)
                        
                        # Verify the token works
                        provider = IBMProvider()
                        account_info = provider.active_account()
                        
                        # Mask the token for privacy in the response
                        masked_token = token[:5] + "..." + token[-5:] if len(token) > 10 else "***"
                        
                        return {
                            "status": "success",
                            "message": f"IBM Quantum token loaded from config file. Connected as {account_info.get('email', 'unknown')}."
                        }
                    else:
                        return {
                            "status": "warning",
                            "message": "Config file exists but doesn't contain ibm_token."
                        }
                except Exception as e:
                    return {
                        "status": "error",
                        "message": f"Error loading token from config file: {str(e)}"
                    }
            else:
                return {
                    "status": "warning",
                    "message": f"No IBM Quantum token found. Please create a config file at {CONFIG_FILE}"
                }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error loading IBM Quantum token: {str(e)}"
        }

