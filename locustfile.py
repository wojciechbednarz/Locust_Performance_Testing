from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

class UserBehaviour(HttpUser):
    @task
    def test_homepage(self):
        self.client.get("/")