# Market IQ Deployment Guide

This guide provides detailed instructions for deploying the Market IQ application in various environments.

## Quick Start (Recommended)

### Using Docker Compose

1. **Extract and navigate to the package:**
   ```bash
   unzip market_iq_package.zip
   cd market_iq_package
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Open browser: `http://localhost:5000`
   - The application will be ready in 1-2 minutes

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

## Deployment Options

### 1. Docker Container (Production Ready)

**Build the image:**
```bash
docker build -t market-iq:latest .
```

**Run with custom configuration:**
```bash
docker run -d \
  --name market-iq-app \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  --restart unless-stopped \
  market-iq:latest
```

**With volume mounting for development:**
```bash
docker run -d \
  --name market-iq-dev \
  -p 5000:5000 \
  -v $(pwd)/src:/app/src \
  -e FLASK_ENV=development \
  market-iq:latest
```

### 2. Local Python Environment

**Setup virtual environment:**
```bash
python3 -m venv market_iq_env
source market_iq_env/bin/activate  # Linux/Mac
# or
market_iq_env\Scripts\activate     # Windows
```

**Install dependencies:**
```bash
pip install -r requirements_full.txt
```

**Download NLTK data:**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

**Run the application:**
```bash
cd src
python main.py
```

### 3. Production Deployment with Gunicorn

**Install Gunicorn:**
```bash
pip install gunicorn
```

**Create Gunicorn configuration (`gunicorn.conf.py`):**
```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

**Run with Gunicorn:**
```bash
cd src
gunicorn --config ../gunicorn.conf.py main:app
```

### 4. Kubernetes Deployment

**Create deployment YAML (`k8s-deployment.yaml`):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: market-iq
spec:
  replicas: 3
  selector:
    matchLabels:
      app: market-iq
  template:
    metadata:
      labels:
        app: market-iq
    spec:
      containers:
      - name: market-iq
        image: market-iq:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: market-iq-service
spec:
  selector:
    app: market-iq
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

**Deploy to Kubernetes:**
```bash
kubectl apply -f k8s-deployment.yaml
```

## Environment Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_APP` | Flask application module | `src.main` | No |
| `FLASK_ENV` | Environment mode | `development` | No |
| `PYTHONPATH` | Python module path | `/app` | No |
| `PORT` | Application port | `5000` | No |

### Configuration Files

**For production, create `config.py`:**
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///financial_kb.db'
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Add production-specific settings

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

## Performance Optimization

### 1. Database Optimization

**For production, consider PostgreSQL:**
```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Update database URL
export DATABASE_URL="postgresql://user:password@localhost/market_iq"
```

### 2. Caching

**Add Redis caching:**
```bash
pip install redis flask-caching
```

**Configure caching in application:**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

### 3. Load Balancing

**Nginx configuration (`nginx.conf`):**
```nginx
upstream market_iq {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://market_iq;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/market_iq/src/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## Security Considerations

### 1. Production Security

**Update Flask configuration:**
```python
# Disable debug mode
app.config['DEBUG'] = False

# Set secure secret key
app.config['SECRET_KEY'] = 'your-secure-secret-key'

# Enable security headers
from flask_talisman import Talisman
Talisman(app)
```

### 2. Container Security

**Use non-root user in Dockerfile:**
```dockerfile
RUN adduser --disabled-password --gecos '' appuser
USER appuser
```

### 3. Network Security

- Use HTTPS in production
- Implement proper firewall rules
- Regular security updates

## Monitoring and Logging

### 1. Application Logging

**Configure logging:**
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/market_iq.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

### 2. Health Checks

**Add health check endpoint:**
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

### 3. Metrics Collection

**Prometheus metrics:**
```bash
pip install prometheus-flask-exporter
```

## Troubleshooting

### Common Issues

1. **Application won't start:**
   - Check Python version (3.11+ required)
   - Verify all dependencies installed
   - Check port availability

2. **Database errors:**
   - Ensure SQLite file permissions
   - Check database file path
   - Verify database integrity

3. **NLTK data missing:**
   ```bash
   python -c "import nltk; nltk.download('all')"
   ```

4. **Memory issues:**
   - Increase container memory limits
   - Optimize database queries
   - Enable caching

### Debug Mode

**Enable debug logging:**
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
```

**Check application logs:**
```bash
docker logs market-iq-app
```

### Performance Issues

1. **Slow search queries:**
   - Check database indexes
   - Optimize NLP processing
   - Enable query caching

2. **High memory usage:**
   - Monitor pandas/numpy operations
   - Implement data pagination
   - Use streaming for large datasets

## Backup and Recovery

### Database Backup

**SQLite backup:**
```bash
cp src/financial_kb.db backup/financial_kb_$(date +%Y%m%d).db
```

**Automated backup script:**
```bash
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
cp src/financial_kb.db $BACKUP_DIR/financial_kb_$DATE.db
find $BACKUP_DIR -name "financial_kb_*.db" -mtime +7 -delete
```

### Application Recovery

1. Stop the application
2. Restore database from backup
3. Restart the application
4. Verify functionality

## Scaling

### Horizontal Scaling

- Use multiple application instances
- Implement load balancing
- Share database across instances

### Vertical Scaling

- Increase container resources
- Optimize database performance
- Enable caching layers

## Support

For deployment issues:
1. Check logs for error details
2. Verify system requirements
3. Test with minimal configuration
4. Review security settings

