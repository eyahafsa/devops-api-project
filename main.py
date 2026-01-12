from fastapi import FastAPI, Request
import time

app = FastAPI()

import logging
from prometheus_client import Counter, generate_latest
from fastapi import Response

# 1. Setup Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')

# 2. Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    REQUEST_COUNT.inc() # Increment counter on every visit
    logger.info(f"Request: {request.method} {request.url.path}")
    return await call_next(request)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


# Simple database (in-memory)
items = []

@app.get("/")
def home():
    return {"message": "Welcome to my DevOps API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/items")
async def create_item(name: str):
    items.append(name)
    return {"added": name, "total": len(items)}
