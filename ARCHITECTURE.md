# DevOps Book Library API - Architecture Report

## Executive Summary

Book Library API built with FastAPI, demonstrating containerization, Kubernetes orchestration, CI/CD automation, observability, and security scanning.

## System Architecture

**Three-Tier Design:**
1. **Application** - FastAPI REST API (96 lines)
2. **Container** - Docker + Docker Compose
3. **Orchestration** - Kubernetes (Minikube)

### API Service (FastAPI)

**Why FastAPI:**
- High performance (NodeJS/Go comparable)
- Auto API documentation
- Pydantic validation
- Async support

**Endpoints:**
- `GET /` - Welcome + book count
- `GET /health` - Health check
- `GET /books` - List books (filter available)
- `POST /books` - Add book
- `GET /books/{id}` - Get book
- `DELETE /books/{id}` - Delete book
- `GET /stats` - Statistics
- `GET /metrics` - Prometheus metrics

**Data:** In-memory storage (5 pre-loaded books), CRUD operations, ready for DB integration.

## Infrastructure

### Docker
- Base: `python:3.9-slim`
- Port: 8000
- Docker Compose included
- Benefits: Consistency, isolation, portability

### Container Registry
- Docker Hub: `eyahafsa/devops-api:latest`

### Kubernetes
- 2 replicas (high availability)
- Auto-healing, rolling updates
- Horizontal scaling ready

## CI/CD Pipeline

**GitHub Actions:**
1. Checkout → 2. Build → 3. Test → 4. Cleanup

**Triggers:** Push to any branch, PRs to main

## Observability

**Metrics (Prometheus):**
- `http_requests_total` counter
- `/metrics` endpoint, Grafana-ready

**Logging:**
- Structured: `{method} {path}`
- Access: Console, `docker logs`, `kubectl logs`

## Security

**SAST (Bandit):**
- 96 lines scanned, 0 vulnerabilities
- No hardcoded secrets, proper input validation

**DAST (OWASP ZAP):**
- Tested on running Docker container
- All endpoints validated

**Container Security:**
- Minimal image (python:3.9-slim)
- Regular updates

## Lessons Learned

**Challenges & Solutions:**
- VT-X unavailable → Used Docker driver for Minikube
- GitHub Actions not triggering → Fixed branch config
- Image pull errors → Used `imagePullPolicy: Never`

**Key Insights:**
- Automation saves time
- Start simple, iterate
- Observability from day one
- Security can't be retrofitted

**Future Improvements:**
- Grafana dashboard
- Cloud deployment (AWS/Azure)

## Conclusion

Complete DevOps lifecycle demonstration: FastAPI app → Docker → Kubernetes → CI/CD → Monitoring → Security.

**Achieved:**
- Scalable (Kubernetes)
- Maintainable (automation)
- Reliable (health checks, replicas)
- Observable (metrics, logs)
- Secure (SAST, DAST)

**Technologies:** FastAPI, Docker, Kubernetes, GitHub Actions, Prometheus, Bandit, OWASP ZAP

