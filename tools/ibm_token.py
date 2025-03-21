#!/usr/bin/env python3
import os
import json
from pathlib import Path

try:
    from qiskit_ibm_provider import IBMProvider
    HAS_IBM_PROVIDER = True
except ImportError:
    HAS_IBM_PROVIDER = False

CONFIG_DIR = Path.home() / '.qiskit'
CONFIG_FILE = CONFIG_DIR / 'config.json'

def load_token():
    if not HAS_IBM_PROVIDER:
        return {
            "status": "error",
            "message": "qiskit_ibm_provider not installed"
        }
    
    try:
        try:
            provider = IBMProvider()
            account_info = provider.active_account()
            return {
                "status": "success",
                "message": f"Using saved credentials: {account_info.get('email', 'unknown')}"
            }
        except:
            if CONFIG_FILE.exists():
                try:
                    with open(CONFIG_FILE, 'r') as f:
                        config = json.load(f)
                    
                    if 'ibm_token' in config and config['ibm_token']:
                        token = config['ibm_token']
                        IBMProvider.save_account(token=token, overwrite=True)
                        
                        provider = IBMProvider()
                        account_info = provider.active_account()
                        
                        return {
                            "status": "success",
                            "message": f"Token loaded from config: {account_info.get('email', 'unknown')}"
                        }
                    else:
                        return {
                            "status": "warning",
                            "message": "Config exists but no token found"
                        }
                except Exception as e:
                    return {
                        "status": "error",
                        "message": f"Token loading error: {str(e)}"
                    }
            else:
                return {
                    "status": "warning",
                    "message": "No IBM token found"
                }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Token error: {str(e)}"
        }