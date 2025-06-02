"""
Configuration module for environment variables
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Tuya API Configuration
TUYA_CONFIG = {
    "CLIENT_ID": os.getenv("TUYA_CLIENT_ID"),
    "CLIENT_SECRET": os.getenv("TUYA_CLIENT_SECRET"),
    "API_ENDPOINT": os.getenv("TUYA_API_ENDPOINT", "https://openapi.tuyain.com"),
    "DEVICE_ID": os.getenv("TUYA_DEVICE_ID"),
}

OPENAI_CONFIG = {
    "API_KEY": os.getenv("OPENAI_API_KEY"),
}


# Validate required environment variables
def validate_config():
    """Validate that all required environment variables are set"""
    missing_vars = []

    # Check Tuya configuration
    for key, value in TUYA_CONFIG.items():
        if value is None:
            missing_vars.append(f"TUYA_{key}")

    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}. "
            "Please set them in the .env file."
        )


# Validate on module import
validate_config()
