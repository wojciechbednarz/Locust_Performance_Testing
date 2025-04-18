class PetstoreRequests:

    def __init__(self, client):
        self.client = client

    def post_request(self, payload, url: str):
        with self.client.post(url=url, json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                return True
            else:
                response.failure("POST request error")
                return False

    def get_request(self, url: str):
        with self.client.get(url=url, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                content = response.json()
                return True, content
            else:
                response.failure("GET request error")
                return False, None

    def put_request(self, url: str, payload):
        with self.client.put(url=url, json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                return True
            else:
                response.failure("PUT request error")
                return False
