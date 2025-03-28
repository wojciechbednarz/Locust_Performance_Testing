# Locust Performance Testing

## Overview
A simple Locust-based performance testing project to simulate user behavior and measure system performance.

## Installation
```sh
pip install -r requirements.txt
```

## Usage
Run tests via Locust UI:
```sh
locust -f locustfile.py
```
Or headless mode:
```sh
locust -f locustfile.py --headless -u 100 -r 10 -t 5m --host=http://example.com
```

## Docker
```sh
docker build -t locust-test .
docker run -p 8089:8089 locust-test
```

## License
MIT License

