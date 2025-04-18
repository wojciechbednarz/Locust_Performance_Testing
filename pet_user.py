from locust import HttpUser, between
from tasks.pet_tasks import PetTasks

class PetstoreUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [PetTasks]
