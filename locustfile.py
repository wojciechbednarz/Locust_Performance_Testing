from locust import HttpUser, task
from utilities import return_json_payload, change_data_in_the_json_file, create_pet_fake_name, create_fake_username
import logging
from copy import deepcopy

PET_STORE_INVENTORY = '/store/inventory'
PET_STORE_ORDER = '/store/order'
PET_STORE_CREATE_PET = "/pet"
PET_STORE_USER = "/user"

logger = logging.getLogger(__name__)

# class HelloWorldUser(HttpUser):
#     """ Test class when user uses web_app Flask app. task(0) to prevent it from running. """
#     abstract = True
#     @task(0)
#     def hello_world(self):
#         self.client.get("/hello")
#         self.client.get("/world")
#
# class UserBehaviour(HttpUser):
#     """ Test class when user uses web_app Flask app. task(0) to prevent it from running. """
#     @task(0)
#     def test_homepage(self):
#         self.client.get("/")


class SwaggerPetStore(HttpUser):
    host = 'https://petstore.swagger.io/v2'

    pet_create_payload = deepcopy(return_json_payload("pet_create.json"))
    pet_order_payload = deepcopy(return_json_payload("pet_order.json"))
    user_create_payload = deepcopy(return_json_payload("user_create.json"))

    def post_request(self, payload, url: str):
        with self.client.post(url=url, json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success("")
                return True
            else:
                response.failure("")
                return False

    def get_request(self, url: str, response=False):
        with self.client.get(url=url, catch_response=True) as response:
            if response.status_code == 200:
                response.success("")
                content = response.json()
                if response:
                    return True, content
                else:
                    return True
            else:
                response.failure("")
                return False

    def put_request(self, url: str, payload):
        with self.client.put(url=url, json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success("")
                return True
            else:
                response.failure("")
                return False

    def create_pet(self):
        logger.info("Start creation of the pet.")
        pet_name = create_pet_fake_name()
        with change_data_in_the_json_file("pet_create.json", {"name": pet_name}):
            create_pet = self.post_request(payload=self.pet_create_payload, url=PET_STORE_CREATE_PET)
            if create_pet:
                logger.info(f"Pet with name {pet_name} created successfully.")
            else:
                logger.error(f"Failed to create pet: {pet_name}")

    def create_user(self):
        logger.info("Start creation of the new user.")
        user_name = create_fake_username()
        with change_data_in_the_json_file("user_create.json", {"username": user_name}):
            create_user = self.post_request(payload=self.user_create_payload, url=PET_STORE_USER)
            if create_user:
                logger.info(f"User with username {user_name} created successfully.")
            else:
                logger.error(f"Failed to create user with username: {user_name}")

    def on_start(self):
        """
        This will run before each simulated user starts executing tasks.
        It's a better place to create the pet instead of using events.init.
        """
        self.create_pet()
        self.create_user()

    @task
    def get_main_page(self):
        self.client.get("/")

    @task
    def get_pet_store_inventory_statuses(self):
        response_status, content = self.get_request(PET_STORE_INVENTORY, response=True)
        if response_status:
            inventory = content
            for status, count in inventory.items():
                logger.info(f"Status: {status}, Count: {count}")
        else:
            logger.error("Failed to get pet store inventory for request.")


    @task
    def place_an_order_for_a_pet(self):
        pet_order = self.post_request(self.pet_order_payload, PET_STORE_ORDER)
        if pet_order:
            logger.info(f"Order for purchasing the pet success.")
        else:
            logger.error("Order for purchasing the pet fail.")

    @task
    def update_user_data(self):
        logger.info("Start updating user data.")
        user_id = 0
        payload = {"id": user_id, "firstName": "Adam"}
        modify_user_name = self.put_request(payload=payload, url=PET_STORE_USER)
        if modify_user_name:
            logger.info(f"User with id {user_id} modified successfully.")
        else:
            logger.error(f"Failed to modify user with id: {user_id}.")
