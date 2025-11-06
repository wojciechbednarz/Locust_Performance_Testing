from locust import HttpUser, task, events, Events
from pet_user import PetstoreUser
import logging
from typing import Any

PET_STORE_INVENTORY = 'https://petstore.swagger.io/v2/store/inventory'
PET_STORE_ORDER = 'https://petstore.swagger.io/v2/store/order'
PET_STORE_CREATE_PET = "https://petstore.swagger.io/v2/pet"
PET_STORE_USER = "https://petstore.swagger.io/v2/user"

logger = logging.getLogger(__name__)

@events.init.add_listener
def on_locust_init(environment: Any, **kwargs: Any) -> None:
    """
    Event listener that runs when Locust initializes.
    Adds a new endpoint to the Locust web UI if it's enabled.
    Args:
        environment: The Locust environment instance.
        **kwargs: Additional keyword arguments.
    """
    if environment.web_ui:
        @environment.web_ui.app.route("/new_endpoint")
        def add_new_endpoint() -> str:
            """
            Handler for the custom /new_endpoint route.
            Returns:
                str: A simple message indicating the new endpoint.
            """
            return "New endpoint"

class HelloWorldUser(HttpUser):
    """Test class when user uses web_app Flask app."""
    @task
    def hello_world(self) -> None:
        """
        Task that makes requests to /hello and /world endpoints.
        This simulates a user accessing the hello and world pages
        of the Flask application.
        """
        self.client.get("/hello")
        self.client.get("/world")

class UserBehaviour(PetstoreUser):
    """Test class when user uses web_app Flask app."""
    
    @task
    def test_homepage(self) -> None:
        """
        Task that makes a request to the homepage.
        This simulates a user accessing the root endpoint
        of the application.
        """
        self.client.get("/")

class CheckConditions(Events):
    """Class for checking test performance conditions and setting exit codes."""
    
    @events.quitting.add_listener
    def _(self, environment: Any, **kwargs: Any) -> None:
        """
        Event listener that runs when Locust is quitting.
        Checks performance metrics and sets appropriate exit codes based on:
        - Failure ratio threshold (1%)
        - Average response time threshold (200ms)
        - 95th percentile response time threshold (800ms)
        Args:
            environment: The Locust environment instance containing stats.
            **kwargs: Additional keyword arguments.
        """
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
