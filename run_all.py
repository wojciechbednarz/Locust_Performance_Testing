"""Module to run both Flask app and Locust load tests concurrently."""
import os
import signal
import time
import sys
import threading
import logging
import subprocess
from web_app import app

FLASK_PROCESS = None
logger = logging.getLogger(__name__)


def signal_handler(sig, frame):
    """
    Handle termination signals to gracefully shut down the Flask server.
    """
    logger.info("\nSignal received, shutting down Flask server.")
    sys.exit(0)

def run_flask() -> None:
    """
    Start the Flask web application server.
    Runs the Flask app on host 0.0.0.0 and port 5000, making it
    accessible from any network interface.
    """
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

def run_locust(users_number: int = 50, spawn_rate: int = 5) -> None:
    """
    Execute Locust load test in headless mode.
    Runs Locust with specified user count and spawn rate, targeting
    the local Flask server on port 5000.
    Args:
        users_number: Number of concurrent users to simulate. Defaults to 50.
        spawn_rate: Rate at which users are spawned per second. Defaults to 5.
    """
    target_host = os.getenv('TARGET_HOST', 'http://localhost:5000')
    users = os.getenv('USERS', str(users_number))
    runtime = os.getenv('RUN_TIME', '30s')
    try:
        subprocess.run([
            "locust",
            "-f", "locustfile.py",
            "--headless",
            "--users", str(users),
            "-r", "2",
            "-t", runtime,
            "--spawn-rate", str(spawn_rate),
            f"--host={target_host}",
            "--web-port", "8089"
        ], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Locust test failed with error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    logger.info("Waiting for Flask server to start...")
    time.sleep(2)
    
    logger.info("Starting Locust tests...")
    run_locust()
    
    logger.info("Tests completed successfully")
