import threading
import subprocess
from web_app import app


def run_flask() -> None:
    """
    Start the Flask web application server.
    Runs the Flask app on host 0.0.0.0 and port 5000, making it
    accessible from any network interface.
    """
    app.run(host="0.0.0.0", port=5000)

def run_locust(users_number: int = 50, spawn_rate: int = 5) -> None:
    """
    Execute Locust load test in headless mode.
    Runs Locust with specified user count and spawn rate, targeting
    the local Flask server on port 5000.
    Args:
        users_number: Number of concurrent users to simulate. Defaults to 50.
        spawn_rate: Rate at which users are spawned per second. Defaults to 5.
    """
    subprocess.run([
        "locust", "-f", "locustfile.py", "--headless", "--users", str(users_number),
        f"--spawn-rate", str(spawn_rate), "--host=http://localhost:5000", "--web-port", "8089"
    ])

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    import time
    time.sleep(2)
    run_locust()
