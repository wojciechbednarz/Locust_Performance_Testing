import threading
import subprocess
from web_app import app


def run_flask():
    app.run(host="0.0.0.0", port=5000)

def run_locust(users_number=50, spawn_rate=5):
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
