import os
import json
import logging
import contextlib
from faker import Faker

logger = logging.getLogger(__name__)

def return_json_payload(file_name):
    try:
        file_path = os.path.join(os.path.dirname(__file__), "json", file_name)
        with open(file_path, "r") as f:
            payload = json.load(f)
        return payload
    except FileNotFoundError as exc:
        logger.error(f"Provided file: {file_name} was not found. Error: {exc}")

def increment_ids(my_data):
    if isinstance(my_data, dict):
        for key, value in my_data.items():
            if key == "id" and isinstance(value, int):
                my_data[key] = value + 1
            else:
                increment_ids(value)
    elif isinstance(my_data , list):
        for item in my_data:
            increment_ids(item)

def get_modified_json_payload(file_name, substitution):
    data = return_json_payload(file_name)
    for key, value in substitution.items():
        if key in data:
            data[key] = value
    increment_ids(data)
    return data

@contextlib.contextmanager
def change_data_in_the_json_file(file_name, substitution):
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

def create_pet_fake_name():
    faker = Faker()
    fake_name = faker.first_name()
    return fake_name

def create_fake_username():
    faker = Faker()
    fake_user_name = faker.user_name()
    return fake_user_name

