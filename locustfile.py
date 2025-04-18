from locust import HttpUser, task
from pet_user import PetstoreUser
import logging

PET_STORE_INVENTORY = 'https://petstore.swagger.io/v2/store/inventory'
PET_STORE_ORDER = 'https://petstore.swagger.io/v2/store/order'
PET_STORE_CREATE_PET = "https://petstore.swagger.io/v2/pet"
PET_STORE_USER = "https://petstore.swagger.io/v2/user"

logger = logging.getLogger(__name__)

class HelloWorldUser(HttpUser):
    """ Test class when user uses web_app Flask app. Commented task decorator to prevent it from running. """
    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

class UserBehaviour(PetstoreUser):
    """ Test class when user uses web_app Flask app. Commented task decorator to prevent it from running. """
    @task
    def test_homepage(self):
        self.client.get("/")
