from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevSecOps Pipeline</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }

        .container {
            text-align: center;
            padding: 40px;
            max-width: 900px;
        }

        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            padding: 8px 20px;
            border-radius: 50px;
            font-size: 14px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }

        .badge span {
            color: #00ff88;
            font-weight: bold;
        }

        h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 15px;
            background: linear-gradient(90deg, #00ff88, #00b4d8, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            font-size: 1.2rem;
            color: rgba(255,255,255,0.7);
            margin-bottom: 50px;
            line-height: 1.6;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 50px;
        }

        .card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 25px 20px;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            border-color: #00ff88;
        }

        .card .icon {
            font-size: 2.5rem;
            margin-bottom: 12px;
        }

        .card h3 {
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 8px;
            color: #00ff88;
        }

        .card p {
            font-size: 0.85rem;
            color: rgba(255,255,255,0.6);
        }

        .pipeline {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 50px;
        }

        .pipeline-step {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.15);
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
        }

        .pipeline-arrow {
            color: #00ff88;
            font-size: 1.2rem;
        }

        .status-bar {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9rem;
        }

        .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #00ff88;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.4; }
            100% { opacity: 1; }
        }

        .author {
            font-size: 0.9rem;
            color: rgba(255,255,255,0.5);
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 30px;
        }

        .author span {
            color: #00b4d8;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">

        <div class="badge">
            🔐 <span>SECURITY VERIFIED</span> — Trivy + OWASP + SonarQube
        </div>

        <h1>DevSecOps Pipeline</h1>

        <p class="subtitle">
            Enterprise-grade secure CI/CD pipeline with automated<br>
            vulnerability scanning and zero-downtime deployments on AWS EKS
        </p>

        <div class="status-bar">
            <div class="status-item">
                <div class="dot"></div>
                App Status: Live
            </div>
            <div class="status-item">
                <div class="dot"></div>
                Security: Verified
            </div>
            <div class="status-item">
                <div class="dot"></div>
                Pods: Running on EKS
            </div>
        </div>

        <div class="cards">
            <div class="card">
                <div class="icon">🔍</div>
                <h3>Trivy Scanner</h3>
                <p>Docker image vulnerability scanning — blocks critical CVEs</p>
            </div>
            <div class="card">
                <div class="icon">🛡️</div>
                <h3>OWASP Check</h3>
                <p>Dependency vulnerability analysis on every build</p>
            </div>
            <div class="card">
                <div class="icon">📊</div>
                <h3>SonarQube</h3>
                <p>Code quality and security hotspot detection</p>
            </div>
            <div class="card">
                <div class="icon">🐳</div>
                <h3>Docker + ECR</h3>
                <p>Containerized and stored in AWS private registry</p>
            </div>
            <div class="card">
                <div class="icon">☸️</div>
                <h3>AWS EKS</h3>
                <p>Kubernetes with auto-scaling and self-healing pods</p>
            </div>
            <div class="card">
                <div class="icon">📈</div>
                <h3>Prometheus + Grafana</h3>
                <p>Real-time monitoring and alerting dashboards</p>
            </div>
        </div>

        <div class="pipeline">
            <div class="pipeline-step">📥 GitHub</div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-step">⚙️ Jenkins</div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-step">🔍 OWASP</div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-step">📊 SonarQube</div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-step">🐳 Docker</div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-step">🛡️ Trivy</div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-step">☁️ ECR</div>
            <div class="pipeline-arrow">→</div>
            <div class="pipeline-step">☸️ EKS</div>
        </div>

        <div class="author">
            Built by <span>Ravi Dhande</span> | Cloud & DevSecOps Engineer |
            AWS Certified Cloud Practitioner
        </div>

    </div>
</body>
</html>
    '''

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'version': '1.0',
        'security': 'verified'
    })

@app.route('/info')
def info():
    return jsonify({
        'app': 'DevSecOps Pipeline',
        'stack': ['Jenkins', 'Trivy', 'OWASP', 'SonarQube', 'Docker', 'EKS'],
        'author': 'Ravi Dhande'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
