from flask import Flask, request
from prometheus_client import start_http_server, Counter, Gauge, Histogram
import time

app = Flask(__name__)

# Application request counter
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total App Requests"
)

# Application error counter
ERROR_COUNT = Counter(
    "app_errors_total",
    "Total application errors"
)

# Application response latency
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Application request latency in seconds"
)

# Estimated cloud cost per service
CLOUD_COST = Gauge(
    "cloud_estimated_cost",
    "Estimated Cloud Cost in USD",
    ["service"]
)

# Simulated cloud resource usage
CLOUD_USAGE = Gauge(
    "cloud_resource_usage",
    "Simulated Cloud Resource Usage",
    ["service"]
)

# Simulated cloud services
services = {
    "Compute": {"usage": 120, "rate": 0.05},
    "Storage": {"usage": 500, "rate": 0.02},
    "Network": {"usage": 80, "rate": 0.01}
}

# Calculate and export cloud costs
for service, values in services.items():
    usage = values["usage"]
    cost = usage * values["rate"]

    CLOUD_COST.labels(service=service).set(cost)
    CLOUD_USAGE.labels(service=service).set(usage)


# Track application requests and response latency
@app.before_request
def before_request():
    request.start_time = time.perf_counter()


@app.after_request
def after_request(response):
    REQUEST_COUNT.inc()

    duration = time.perf_counter() - request.start_time
    REQUEST_LATENCY.observe(duration)

    if response.status_code >= 500:
        ERROR_COUNT.inc()

    return response


# Application homepage
@app.route("/")
def home():
    return "Cloud Service Running"


# Test endpoint for application errors
@app.route("/error")
def error():
    return "Simulated server error", 500


if __name__ == "__main__":
    start_http_server(8000)
    app.run(host="0.0.0.0", port=5000)
