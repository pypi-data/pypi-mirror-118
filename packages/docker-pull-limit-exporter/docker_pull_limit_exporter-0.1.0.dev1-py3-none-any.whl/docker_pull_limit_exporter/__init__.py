#!/usr/bin/env python3
from prometheus_client import Gauge
from prometheus_client import start_http_server
import time
import requests


def run():
    start_http_server(9309)
    gauge_limit = Gauge("docker_pull_limit", "Your daily maximum")
    gauge_remaining = Gauge("docker_pull_remaining","Your Daily remaining pulls")

    while True:
        next_run = time.time() + 6
        jwt_response = requests.get(
            "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull"
        )
        token = jwt_response.json()["token"]
        test_pull_response = requests.head(
            "https://registry-1.docker.io/v2/ratelimitpreview/test/manifests/latest",
            headers={"Authorization": "Bearer {}".format(token)},
        )
        limit = test_pull_response.headers["ratelimit-limit"].split(";")[0]
        remaining = test_pull_response.headers["ratelimit-remaining"].split(";")[0]
        gauge_limit.set(limit)
        gauge_remaining.set(remaining)
        while next_run > time.time():
            time.sleep(1)
run()
