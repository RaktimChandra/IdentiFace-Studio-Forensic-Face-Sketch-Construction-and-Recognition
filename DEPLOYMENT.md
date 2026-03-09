# Deployment Guide - IdentiFace Studio

Complete deployment instructions for production environments.

---

## Quick Deploy with Docker

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM
- 10GB+ storage

### Steps

1. **Clone Repository**
```bash
git clone https://github.com/RaktimChandra/IdentiFace-Studio.git
cd IdentiFace-Studio
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your settings
nano .env
```

3. **Build and Start**
```bash
docker-compose up -d
```

4. **Access Application**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

---

## Manual Deployment

### Backend Deployment (Ubuntu 20.04+)

#### 1. Install Dependencies
```bash
# System packages
sudo apt update
sudo apt install -y python3.11 python3-pip postgresql-14 nginx

# Python packages
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Setup Database
```bash
# Create database
sudo -u postgres psql
CREATE DATABASE identiface_db;
CREATE USER identiface WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE identiface_db TO identiface;
\q

# Run migrations
python scripts/init_db.py
```

#### 3. Configure Systemd Service
Create `/etc/systemd/system/identiface-backend.service`:

```ini
[Unit]
Description=IdentiFace Studio Backend
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/identiface/backend
Environment="PATH=/var/www/identiface/backend/venv/bin"
ExecStart=/var/www/identiface/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable identiface-backend
sudo systemctl start identiface-backend
```

#### 4. Configure Nginx
Create `/etc/nginx/sites-available/identiface`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 20M;

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /uploads {
        alias /var/www/identiface/backend/uploads;
    }

    location / {
        root /var/www/identiface/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/identiface /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. SSL Certificate
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Frontend Deployment

#### 1. Build Application
```bash
cd frontend
npm install
npm run build
```

#### 2. Copy to Server
```bash
rsync -avz dist/ user@server:/var/www/identiface/frontend/dist/
```

---

## Cloud Platforms

### AWS Deployment

#### Using EC2

**Instance Type:** t3.medium or larger (2GB+ RAM)

1. Launch EC2 instance (Ubuntu 20.04)
2. Configure security groups (ports 80, 443, 8000)
3. Follow manual deployment steps
4. Use RDS for PostgreSQL (recommended)
5. Use S3 for file storage

#### Using ECS (Docker)

```bash
# Build images
docker build -t identiface-backend ./backend
docker build -t identiface-frontend ./frontend

# Push to ECR
aws ecr create-repository --repository-name identiface-backend
docker tag identiface-backend:latest <ecr-url>/identiface-backend:latest
docker push <ecr-url>/identiface-backend:latest

# Create ECS task definition and service
aws ecs create-cluster --cluster-name identiface
# Configure task definition, service, load balancer
```

### Google Cloud Platform

#### Using Compute Engine

1. Create VM instance (n1-standard-2)
2. Install Docker
3. Run docker-compose deployment
4. Configure Cloud SQL for PostgreSQL
5. Use Cloud Storage for uploads

#### Using Cloud Run

```bash
# Build and push images
gcloud builds submit --tag gcr.io/PROJECT_ID/identiface-backend ./backend
gcloud builds submit --tag gcr.io/PROJECT_ID/identiface-frontend ./frontend

# Deploy backend
gcloud run deploy identiface-backend \
  --image gcr.io/PROJECT_ID/identiface-backend \
  --platform managed \
  --memory 2Gi

# Deploy frontend
gcloud run deploy identiface-frontend \
  --image gcr.io/PROJECT_ID/identiface-frontend \
  --platform managed
```

### Heroku

#### Backend
```bash
cd backend
heroku create identiface-api
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

#### Frontend
```bash
cd frontend
heroku create identiface-app
heroku buildpacks:set heroku/nodejs
git push heroku main
```

---

## Production Checklist

### Security
- [ ] Change SECRET_KEY to strong random value
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Use strong database passwords
- [ ] Enable database encryption
- [ ] Set up VPN for admin access
- [ ] Configure rate limiting
- [ ] Enable audit logging

### Performance
- [ ] Configure database connection pooling
- [ ] Enable Redis caching
- [ ] Set up CDN for static files
- [ ] Configure gzip compression
- [ ] Optimize database indexes
- [ ] Enable query caching
- [ ] Configure load balancer
- [ ] Set up auto-scaling

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure log aggregation
- [ ] Set up uptime monitoring
- [ ] Enable performance monitoring
- [ ] Configure alerts
- [ ] Set up backup monitoring

### Backup
- [ ] Database daily backups
- [ ] Upload files backup
- [ ] Configuration backup
- [ ] Test restore procedures
- [ ] Offsite backup storage

---

## Environment Variables

### Required
```env
SECRET_KEY=<strong-random-key>
DATABASE_URL=<postgresql-url>
ENVIRONMENT=production
```

### Optional
```env
REDIS_URL=<redis-url>
AWS_ACCESS_KEY_ID=<aws-key>
AWS_SECRET_ACCESS_KEY=<aws-secret>
AWS_S3_BUCKET=<bucket-name>
```

---

## Troubleshooting

### Database Connection Failed
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U identiface -d identiface_db
```

### High Memory Usage
- Increase instance size
- Enable Redis caching
- Optimize database queries
- Reduce worker processes

### Slow Face Recognition
- Use GPU instance (AWS p2/p3)
- Optimize image sizes
- Batch processing
- Caching results

---

## Scaling Strategy

### Horizontal Scaling
- Multiple backend instances
- Load balancer (Nginx/HAProxy)
- Shared PostgreSQL
- Redis for session storage
- S3/Cloud Storage for uploads

### Vertical Scaling
- Increase CPU/RAM
- GPU for face recognition
- SSD storage
- Database tuning

---

## Cost Optimization

### AWS Estimated Monthly Cost
- EC2 t3.medium: $30
- RDS db.t3.micro: $15
- S3 storage (100GB): $3
- **Total: ~$50/month**

### GCP Estimated Monthly Cost
- n1-standard-2: $50
- Cloud SQL: $25
- Cloud Storage: $3
- **Total: ~$80/month**

---

## Support

For deployment issues:
- Check logs: `docker-compose logs -f`
- Review documentation
- Open GitHub issue

---

**Deployment complete! Your forensic tool is live! 🚀**
