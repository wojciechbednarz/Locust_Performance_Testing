import os
import json
import logging
import contextlib
from typing import Dict, Any, Iterator, Union, List
from faker import Faker

logger = logging.getLogger(__name__)

def return_json_payload(file_name: str) -> Dict[str, Any]:
    """
    Returns JSON payload from a file located in the 'json' directory.
    Args:
        file_name: Name of the JSON file to load.
    Returns:
        Dict[str, Any]: The parsed JSON data as a dictionary.  
    Raises:
        FileNotFoundError: If the specified file doesn't exist.
    """
    try:
        file_path = os.path.join(os.path.dirname(__file__), "json", file_name)
        with open(file_path, "r") as f:
            payload = json.load(f)
        return payload
    except FileNotFoundError as exc:
        logger.error(f"Provided file: {file_name} was not found. Error: {exc}")

def increment_ids(my_data: Union[Dict[str, Any], List[Any]]) -> None:
    """
    Recursively increment all 'id' fields in a nested data structure.
    Traverses dictionaries and lists to find integer 'id' fields and increments
    them by 1. Modifies the data structure in place.
    Args:
        my_data: A dictionary or list that may contain 'id' fields to increment.
    """
    if isinstance(my_data, dict):
        for key, value in my_data.items():
            if key == "id" and isinstance(value, int):
                my_data[key] = value + 1
            else:
                increment_ids(value)
    elif isinstance(my_data , list):
        for item in my_data:
            increment_ids(item)

def get_modified_json_payload(file_name: str, substitution: Dict[str, Any]) -> Dict[str, Any]:
    """
    Load JSON payload, apply substitutions, and increment IDs.
    Args:
        file_name: Name of the JSON file to load from the 'json' directory.
        substitution: Dictionary of key-value pairs to substitute in the payload.
    Returns:
        Dict[str, Any]: Modified JSON payload with substitutions applied and IDs incremented.
    """
    data = return_json_payload(file_name)
    for key, value in substitution.items():
        if key in data:
            data[key] = value
    increment_ids(data)
    return data

@contextlib.contextmanager
def change_data_in_the_json_file(file_name: str, substitution: Dict[str, Any]) -> Iterator[None]:
    """
    Context manager for temporarily modifying a JSON file.
    Reads a JSON file, applies substitutions, increments IDs, and writes back
    to the file. This modifies the file on disk.
    Args:
        file_name: Name of the JSON file in the 'json' directory.
        substitution: Dictionary of key-value pairs to substitute in the file.
    Yields:
        None
    Raises:
        FileNotFoundError: If the specified file doesn't exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    file_path = os.path.join(os.path.dirname(__file__), "json", file_name)
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        for key, value in substitution.items():
            if key in data:
                data[key] = value
        increment_ids(data)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=1)
        yield
    except FileNotFoundError as exc:
        logger.error(f"Provided file: {file_path} was not found. Error: {exc}")
        raise
    except json.JSONDecodeError as exc:
        logger.error(f"JSON decode error in file {file_path}. Error: {exc}")
        raise

def create_pet_fake_name() -> str:
    """
    Generate a random fake first name for a pet.
    
    Uses the Faker library to create a realistic first name.
    
    Returns:
        str: A randomly generated first name.
    """
    faker = Faker()
    fake_name = faker.first_name()
    return fake_name

def create_fake_username() -> str:
    """
    Generate a random fake username.
    
    Uses the Faker library to create a realistic username.
    
    Returns:
        str: A randomly generated username.
    """
    faker = Faker()
    fake_user_name = faker.user_name()
    return fake_user_name
