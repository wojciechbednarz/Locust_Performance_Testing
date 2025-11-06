from locust import HttpUser, between
from tasks.pet_tasks import PetTasks

class PetstoreUser(HttpUser):
    """
    Locust HttpUser class for simulating Petstore API users.
    This class configures user behavior for load testing the Petstore API,
    including wait times between tasks and the task set to execute.
    Attributes:
        wait_time: Random wait time between 1-2 seconds between tasks.
        tasks: List of task sets to be executed by this user.
    """
    wait_time = between(1, 2)
    tasks = [PetTasks]
