from typing import Tuple, Optional, Any, Dict

class PetstoreRequests:
    """
    A wrapper class for making HTTP requests to the Petstore API.
    This class provides methods for common HTTP operations (GET, POST, PUT, DELETE)
    with built-in response handling and logging.
    Attributes:
        client: The HTTP client instance for making requests.
    """

    def __init__(self, client: Any) -> None:
        """
        Initialize the PetstoreRequests instance.
        Args:
            client: The HTTP client instance (typically from Locust HttpUser).
        """
        self.client = client

    def post_request(self, payload: Dict[str, Any], url: str) -> bool:
        """
        Execute a POST request to the specified URL.
        Args:
            payload: JSON payload to send in the request body.
            url: The target URL for the POST request.
        Returns:
            bool: True if request succeeded (status 200), False otherwise.
        """
        with self.client.post(url=url, json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                return True
            else:
                response.failure("POST request error")
                return False

    def get_request(self, url: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Execute a GET request to the specified URL.
        Args:
            url: The target URL for the GET request.
        Returns:
            Tuple[bool, Optional[Dict]]: A tuple containing:
                - Success status (True if status 200, False otherwise)
                - Response content as JSON dict (None if request failed)
        """
        with self.client.get(url=url, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                content = response.json()
                return True, content
            else:
                response.failure("GET request error")
                return False, None

    def put_request(self, url: str, payload: Dict[str, Any]) -> bool:
        """
        Execute a PUT request to the specified URL.
        Args:
            url: The target URL for the PUT request.
            payload: JSON payload to send in the request body.
        Returns:
            bool: True if request succeeded (status 200), False otherwise.
        """
        with self.client.put(url=url, json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                return True
            else:
                response.failure("PUT request error")
                return False

    def delete_request(self, url: str) -> bool:
        """
        Execute a DELETE request to the specified URL.
        Args:
            url: The target URL for the DELETE request.
        Returns:
            bool: True if request succeeded (status 200), False otherwise.
        """
        with self.client.delete(url=url, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                return True
            else:
                response.failure("DELETE request error")
                return False

    def delete_request_expect_error_404(self, url: str) -> bool:
        """
        Execute a DELETE request expecting a 404 response.
        This method is used for negative testing scenarios where the
        deletion of a non-existent resource is expected to return 404.
        Args:
            url: The target URL for the DELETE request. 
        Returns:
            bool: True if response was 404 as expected, False otherwise.
        """
        with self.client.delete(url=url, catch_response=True) as response:
            if response.status_code == 404:
                response.success()
                return True
            else:
                response.failure(f"Expected 404, got {response.status_code}")
                return False
