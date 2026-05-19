from flask import Flask, jsonify, render_template_string
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# Prometheus Metrics
REQUEST_COUNT = Counter(
    'app_request_count_total',
    'Total request count',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

ACTIVE_USERS = Gauge(
    'app_active_users',
    'Number of active users'
)

# Dashboard HTML
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Monitoring Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #1a1a2e; color: white; margin: 0; padding: 20px; }
        h1 { color: #00d4ff; text-align: center; }
        .cards { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin: 30px 0; }
        .card { background: #16213e; padding: 30px; border-radius: 10px; min-width: 200px; text-align: center; border: 1px solid #00d4ff; }
        .card h2 { color: #00d4ff; font-size: 2.5em; margin: 0; }
        .card p { color: #aaa; margin: 5px 0 0 0; }
        .status { text-align: center; padding: 10px; background: #0f3460; border-radius: 8px; margin: 10px auto; max-width: 300px; }
        .green { color: #00ff88; }
        a { color: #00d4ff; }
    </style>
</head>
<body>
    <h1>🚀 DevOps Monitoring Dashboard</h1>
    <div class="status"><span class="green">● LIVE</span> — App is Running!</div>
    <div class="cards">
        <div class="card">
            <h2>{{ total_requests }}</h2>
            <p>Total Requests</p>
        </div>
        <div class="card">
            <h2>{{ active_users }}</h2>
            <p>Active Users</p>
        </div>
        <div class="card">
            <h2>{{ avg_latency }}ms</h2>
            <p>Avg Latency</p>
        </div>
    </div>
    <p style="text-align:center">
        <a href="/metrics">📊 View Prometheus Metrics</a> |
        <a href="/health">❤️ Health Check</a> |
        <a href="/api/stats">📈 API Stats</a>
    </p>
</body>
</html>
'''

@app.route('/')
def dashboard():
    start = time.time()
    ACTIVE_USERS.set(random.randint(10, 100))
    REQUEST_COUNT.labels(method='GET', endpoint='/', status='200').inc()
    latency = (time.time() - start) * 1000
    REQUEST_LATENCY.labels(endpoint='/').observe(latency / 1000)
    return render_template_string(DASHBOARD_HTML,
        total_requests=int(REQUEST_COUNT.labels(method='GET', endpoint='/', status='200')._value.get()),
        active_users=int(ACTIVE_USERS._value.get()),
        avg_latency=round(latency, 2)
    )

@app.route('/health')
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health', status='200').inc()
    return jsonify({
        "status": "healthy",
        "service": "devops-monitoring-dashboard",
        "version": "1.0.0"
    })

@app.route('/api/stats')
def stats():
    REQUEST_COUNT.labels(method='GET', endpoint='/api/stats', status='200').inc()
    return jsonify({
        "total_requests": int(REQUEST_COUNT.labels(method='GET', endpoint='/api/stats', status='200')._value.get()),
        "active_users": int(ACTIVE_USERS._value.get()),
        "uptime": "running"
    })

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)