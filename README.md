# 🚀 DevOps Monitoring Dashboard

A real-time monitoring dashboard built with Flask, Prometheus, Grafana, Docker, and GitHub Actions.

## 🛠️ Tech Stack
- **Flask** - Python web application
- **Prometheus** - Metrics collection
- **Grafana** - Visualization & dashboards
- **Docker & Docker Compose** - Containerization
- **GitHub Actions** - CI/CD Pipeline

## 🚀 How to Run

### Prerequisites
- Docker Desktop installed
- Git installed

### Steps
```bash
git clone https://github.com/pranjalpatil2004/devops-monitoring-dashboard.git
cd devops-monitoring-dashboard
docker-compose up --build
```

## 📊 Access Services
| Service | URL |
|---------|-----|
| Flask App | http://localhost:5000 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

## 📈 Metrics Tracked
- Total request count
- Active users
- Request latency
- Health check endpoint

## 🔄 CI/CD Pipeline
Automated pipeline using GitHub Actions:
- Python setup & dependency installation
- Flask app testing
- Docker image build 
