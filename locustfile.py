from locust import HttpUser, task, events, Events
from pet_user import PetstoreUser
import logging

PET_STORE_INVENTORY = 'https://petstore.swagger.io/v2/store/inventory'
PET_STORE_ORDER = 'https://petstore.swagger.io/v2/store/order'
PET_STORE_CREATE_PET = "https://petstore.swagger.io/v2/pet"
PET_STORE_USER = "https://petstore.swagger.io/v2/user"

logger = logging.getLogger(__name__)

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if environment.web_ui:
        @environment.web_ui.app.route("/new_endpoint")
        def add_new_endpoint():
            return "New endpoint"

class HelloWorldUser(HttpUser):
    """ Test class when user uses web_app Flask app. """
    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

class UserBehaviour(PetstoreUser):
    """ Test class when user uses web_app Flask app. """
    @task
    def test_homepage(self):
        self.client.get("/")

class CheckConditions(Events):
    @events.quitting.add_listener
    def _(self, environment, **kwargs):
        if environment.stats.total.fail_ratio > 0.01:
            logger.error("Test failed due to failure ratio > 1%")
            environment.process.exit_code = 1
        elif environment.stats.total.avg_response_time > 200:
            logger.error("Test failed due to average response time ratio > 200 ms")
            environment.process_exit_code = 1
        elif environment.stats.total.get_response_time_percentile(0.95) > 800:
            logger.error("Test failed due to 95th percentile response time > 800 ms")
            environment.process_exit_code = 1
        else:
            environment.process_exit_code = 0
