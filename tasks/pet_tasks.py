from locust import task, TaskSet
from utilities import return_json_payload, get_modified_json_payload, create_pet_fake_name, create_fake_username
from petstore_requests import PetstoreRequests
import logging
from copy import deepcopy

PET_STORE_INVENTORY = 'https://petstore.swagger.io/v2/store/inventory'
PET_STORE_ORDER = 'https://petstore.swagger.io/v2/store/order'
PET_STORE_PET = "https://petstore.swagger.io/v2/pet"
PET_STORE_USER = "https://petstore.swagger.io/v2/user"

logger = logging.getLogger(__name__)

class PetTasks(TaskSet):
    host = 'https://petstore.swagger.io/v2'

    pet_create_payload = deepcopy(return_json_payload("pet_create.json"))
    pet_order_payload = deepcopy(return_json_payload("pet_order.json"))
    user_create_payload = deepcopy(return_json_payload("user_create.json"))
    all_users_payload_data = []
    all_pets_payload_data = []


    def create_pet(self):
        logger.info("Start creation of the pet.")
        pet_name = create_pet_fake_name()
        pet_payload = get_modified_json_payload("pet_create.json", {"name": pet_name})
        self.all_pets_payload_data.append(pet_payload)
        create_pet = self.req.post_request(payload=pet_payload, url=PET_STORE_PET)
        if create_pet:
            logger.info(f"Pet with name {pet_name} created successfully.")
        else:
            logger.error(f"Failed to create pet: {pet_name}")

    def create_user(self):
        logger.info("Start creation of the new user.")
        user_name = create_fake_username()
        user_payload = get_modified_json_payload("user_create.json", {"username": user_name})
        self.all_users_payload_data.append(user_payload)
        create_user = self.req.post_request(payload=user_payload, url=PET_STORE_USER)
        if create_user:
            logger.info(f"User with username {user_name} created successfully.")
        else:
            logger.error(f"Failed to create user with username: {user_name}")

    def on_start(self):
        """
        This will run before each simulated user starts executing tasks.
        It's a better place to create the pet instead of using events.init.
        """
        self.req = PetstoreRequests(self.client)
        self.create_pet()
        self.create_user()

    @task
    def get_main_page(self):
        self.client.get("/")

    @task
    def get_pet_store_inventory_statuses(self):
        response_status, content = self.req.get_request(PET_STORE_INVENTORY)
        if response_status:
            inventory = content
            for status, count in inventory.items():
                logger.info(f"Status: {status}, Count: {count}")
        else:
            logger.error("Failed to get pet store inventory for request.")

    @task
    def place_an_order_for_a_pet(self):
        pet_order = self.req.post_request(self.pet_order_payload, PET_STORE_ORDER)
        if pet_order:
            logger.info(f"Order for purchasing the pet success.")
        else:
            logger.error("Order for purchasing the pet fail.")

    @task
    def update_first_user_data(self):
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
    def delete_non_existing_pet(self):
        ids = [item["id"] for item in self.all_pets_payload_data if "id" in item]
        out_of_range_id = (max(ids) + 1) if ids else 1
        pet_to_delete_url = f"{PET_STORE_PET}/{out_of_range_id}"
        self.req.delete_request_expect_error_404(url=pet_to_delete_url)
