from locust import task, TaskSet
from utilities import return_json_payload, get_modified_json_payload, create_pet_fake_name, create_fake_username
from petstore_requests import PetstoreRequests
import logging
from copy import deepcopy
from typing import List, Dict, Any

PET_STORE_INVENTORY = 'https://petstore.swagger.io/v2/store/inventory'
PET_STORE_ORDER = 'https://petstore.swagger.io/v2/store/order'
PET_STORE_PET = "https://petstore.swagger.io/v2/pet"
PET_STORE_USER = "https://petstore.swagger.io/v2/user"

logger = logging.getLogger(__name__)

class PetTasks(TaskSet):
    """
    TaskSet for Petstore API load testing.
    Contains tasks for creating, reading, updating, and deleting pets and users
    in the Petstore API. Tracks created entities for cleanup and testing.
    Attributes:
        host: Base URL for the Petstore API.
        pet_create_payload: Template payload for creating pets.
        pet_order_payload: Template payload for ordering pets.
        user_create_payload: Template payload for creating users.
        all_users_payload_data: List storing all created user payloads.
        all_pets_payload_data: List storing all created pet payloads.
        req: PetstoreRequests instance for making HTTP requests.
    """
    host = 'https://petstore.swagger.io/v2'

    pet_create_payload: Dict[str, Any] = deepcopy(return_json_payload("pet_create.json"))
    pet_order_payload: Dict[str, Any] = deepcopy(return_json_payload("pet_order.json"))
    user_create_payload: Dict[str, Any] = deepcopy(return_json_payload("user_create.json"))
    all_users_payload_data: List[Dict[str, Any]] = []
    all_pets_payload_data: List[Dict[str, Any]] = []


    def create_pet(self) -> None:
        """
        Create a new pet in the Petstore API.
        Generates a fake pet name, creates a pet payload, stores it in the
        all_pets_payload_data list, and makes a POST request to create the pet.
        Logs success or failure of the operation.
        """
        logger.info("Start creation of the pet.")
        pet_name = create_pet_fake_name()
        pet_payload = get_modified_json_payload("pet_create.json", {"name": pet_name})
        self.all_pets_payload_data.append(pet_payload)
        create_pet = self.req.post_request(payload=pet_payload, url=PET_STORE_PET)
        if create_pet:
            logger.info(f"Pet with name {pet_name} created successfully.")
        else:
            logger.error(f"Failed to create pet: {pet_name}")

    def create_user(self) -> None:
        """
        Create a new user in the Petstore API.
        Generates a fake username, creates a user payload, stores it in the
        all_users_payload_data list, and makes a POST request to create the user.
        Logs success or failure of the operation.
        """
        logger.info("Start creation of the new user.")
        user_name = create_fake_username()
        user_payload = get_modified_json_payload("user_create.json", {"username": user_name})
        self.all_users_payload_data.append(user_payload)
        create_user = self.req.post_request(payload=user_payload, url=PET_STORE_USER)
        if create_user:
            logger.info(f"User with username {user_name} created successfully.")
        else:
            logger.error(f"Failed to create user with username: {user_name}")

    def on_start(self) -> None:
        """
        Initialize the user session before executing tasks.
        This method runs once per simulated user when they start. It creates
        the PetstoreRequests instance and sets up initial test data by creating
        a pet and a user.
        """
        self.req = PetstoreRequests(self.client)
        self.create_pet()
        self.create_user()

    @task
    def get_main_page(self) -> None:
        """
        Task to request the main page of the API.
        Makes a GET request to the root endpoint to simulate browsing
        the main page.
        """
        self.client.get("/")

    @task
    def get_pet_store_inventory_statuses(self) -> None:
        """
        Task to retrieve and log pet store inventory statuses.
        Makes a GET request to the inventory endpoint, retrieves the status
        counts, and logs each status with its count. Logs an error if the
        request fails.
        """
        response_status, content = self.req.get_request(PET_STORE_INVENTORY)
        if response_status:
            inventory = content
            for status, count in inventory.items():
                logger.info(f"Status: {status}, Count: {count}")
        else:
            logger.error("Failed to get pet store inventory for request.")

    @task
    def place_an_order_for_a_pet(self) -> None:
        """
        Task to place an order for a pet.
        Makes a POST request with the pet order payload to simulate
        purchasing a pet. Logs the success or failure of the order.
        """
        pet_order = self.req.post_request(self.pet_order_payload, PET_STORE_ORDER)
        if pet_order:
            logger.info("Order for purchasing the pet success.")
        else:
            logger.error("Order for purchasing the pet fail.")

    @task
    def update_first_user_data(self) -> None:
        """
        Task to update the first created user's data.
        Modifies the first user in the all_users_payload_data list by
        updating their first name to "Adam". Makes a PUT request to apply
        the changes. Logs success or failure.
        """
        logger.info("Start updating user data.")
        user_id = 1
        if len(self.all_users_payload_data) != 0:
            user_name_to_modify = self.all_users_payload_data[0]["username"]
            url_to_modify = f"{PET_STORE_USER}/{user_name_to_modify}"
            payload = {"id": user_id, "firstName": "Adam"}
            modify_user_name = (self.req.
                                put_request(payload=payload, url=url_to_modify))
            if modify_user_name:
                logger.info(f"User with id {user_id} modified successfully.")
            else:
                logger.error(f"Failed to modify user with id: {user_id}.")

    @task
    def delete_non_existing_pet(self) -> None:
        """
        Task to attempt deleting a non-existing pet (negative test).
        Calculates an ID that doesn't exist (max ID + 1) and attempts to
        delete it, expecting a 404 response. This validates error handling
        for non-existent resources.
        """
        ids = [item["id"] for item in self.all_pets_payload_data if "id" in item]
        out_of_range_id = (max(ids) + 1) if ids else 1
        pet_to_delete_url = f"{PET_STORE_PET}/{out_of_range_id}"
        self.req.delete_request_expect_error_404(url=pet_to_delete_url)
