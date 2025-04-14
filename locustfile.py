from locust import HttpUser, task, events
from utilities import return_json_payload
import logging

PET_STORE_INVENTORY = 'https://petstore.swagger.io/v2/store/inventory'
PET_STORE_ORDER = 'https://petstore.swagger.io/v2/store/order'
PET_STORE_UPDATE = "https://petstore.swagger.io/v2/pet"

logger = logging.getLogger(__name__)

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

class UserBehaviour(HttpUser):
    @task
    def test_homepage(self):
        self.client.get("/")


class SwaggerPetStore(HttpUser):
    host = 'https://petstore.swagger.io/v2'

    def on_start(self):
        """
        This will run before each simulated user starts executing tasks.
        It's a better place to create the pet instead of using events.init.
        """
        payload = return_json_payload("pet_update.json")
        with self.client.post(PET_STORE_UPDATE, json=payload, catch_response=True) as response:
            if response.status_code == 200:
                logger.info("Pet created successfully.")
                response.success()
            else:
                logger.error(f"Failed to create pet: {response.status_code} | {response.text}")
                response.failure(f"Create pet failed: {response.status_code}")

    @task
    def get_main_page(self):
        self.client.get("/")

    @task
    def get_pet_store_inventory_statuses(self):
        with self.client.get(PET_STORE_INVENTORY, name=PET_STORE_INVENTORY, catch_response=True) as response:
            if response.status_code == 200:
                inventory = response.json()
                for status, count in inventory.items():
                    logger.info(f"Status: {status}, Count: {count}")
                response.success()
            else:
                logger.error("Failed to get pet store inventory for request.")
                response.failure("Success")
    @task
    def place_an_order_for_a_pet(self):
        payload = return_json_payload("pet_order.json")
        with self.client.post(PET_STORE_ORDER, json=payload, catch_response=True) as response:
            if response.status_code == 200:
                logger.info(f"Order for purchasing the pet success.")
                response.success()
            else:
                logger.error("Order for purchasing the pet fail.")
                response.failure(f"Order failed with status code {response.status_code} and body: {response.text}")