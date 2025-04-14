import os
import json
import logging

logger = logging.getLogger(__name__)

def return_json_payload(file_name):
    try:
        file_path = os.path.join(os.path.dirname(__file__), "json", file_name)
        with open(file_path, "r") as f:
            payload = json.load(f)
        return payload
    except FileNotFoundError as exc:
        logger.error(f"Provided file: {file_name} was not found. Error: {exc}")
