# Setup Guide - IdentiFace Studio

Complete installation guide for development and production.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (Docker)](#quick-start-docker)
3. [Manual Installation](#manual-installation)
4. [Database Setup](#database-setup)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

**Development:**
- Python 3.9+ ([Download](https://www.python.org/downloads/))
- Node.js 18+ ([Download](https://nodejs.org/))
- PostgreSQL 14+ ([Download](https://www.postgresql.org/download/))
- Git ([Download](https://git-scm.com/downloads))

**Production:**
- Docker 20.10+ ([Download](https://docs.docker.com/get-docker/))
- Docker Compose 2.0+ (included with Docker Desktop)

### System Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Storage: 10GB free space
- OS: Windows 10/11, macOS 11+, Ubuntu 20.04+

**Recommended:**
- CPU: 8+ cores (or NVIDIA GPU)
- RAM: 16GB
- Storage: 20GB SSD
- OS: Ubuntu 22.04 LTS

---

## Quick Start (Docker)

### 1. Clone Repository

```bash
git clone https://github.com/RaktimChandra/IdentiFace-Studio.git
cd IdentiFace-Studio
```

### 2. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` file:
```env
DATABASE_URL=postgresql://identiface:password@postgres/identiface_db
SECRET_KEY=your-random-secret-key-here
```

### 3. Start All Services

```bash
docker-compose up -d
```

### 4. Access Application

- **Frontend:** http://localhost
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs

### 5. Create Admin User

```bash
docker-compose exec backend python scripts/create_admin.py
```

---

## Manual Installation

### Backend Setup

#### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** dlib installation may take 5-10 minutes.

**Windows Users:** If dlib fails, install:
- Visual Studio Build Tools
- CMake

```bash
pip install cmake
pip install dlib
```

#### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost/identiface_db
SECRET_KEY=<generate-random-key>
```

Generate secret key:
```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 4. Create Database

```bash
# PostgreSQL command line
createdb identiface_db

# Or using Python
python scripts/init_db.py
```

#### 5. Run Backend

```bash
uvicorn app.main:app --reload
```

Backend runs on: http://localhost:8000

### Frontend Setup

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
VITE_API_URL=http://localhost:8000
```

#### 3. Run Development Server

```bash
npm run dev
```

Frontend runs on: http://localhost:5173

---

## Database Setup

### PostgreSQL Installation

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### macOS (Homebrew)
```bash
brew install postgresql@15
brew services start postgresql@15
```

#### Windows
Download installer from [postgresql.org](https://www.postgresql.org/download/windows/)

### Create Database

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE identiface_db;
CREATE USER identiface WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE identiface_db TO identiface;
\q
```

### Verify Connection

```bash
psql -h localhost -U identiface -d identiface_db
```

---

## Running the Application

### Development Mode

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### Production Mode

**Backend:**
```bash
gunicorn app.main:app --workers 4 --bind 0.0.0.0:8000
```

**Frontend:**
```bash
npm run build
npm run preview
```

---

## Initial Setup

### 1. Create Admin Account

```python
# backend/scripts/create_admin.py
from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.api.v1.endpoints.auth import get_password_hash

db = SessionLocal()

admin = User(
    email="admin@identiface.com",
    username="admin",
    hashed_password=get_password_hash("admin123"),
    full_name="Administrator",
    role=UserRole.ADMIN,
    is_active=True
)

db.add(admin)
db.commit()
print("Admin user created!")
```

Run:
```bash
python scripts/create_admin.py
```

### 2. Test Face Recognition

```bash
python scripts/test_face_recognition.py
```

### 3. Load Sample Data (Optional)

```bash
python scripts/load_sample_data.py
```

---

## Troubleshooting

### Common Issues

#### 1. dlib Installation Failed

**Solution (Windows):**
```bash
# Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/downloads/

# Install CMake
pip install cmake

# Try again
pip install dlib
```

**Solution (Linux):**
```bash
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
pip install dlib
```

#### 2. PostgreSQL Connection Error

**Check if PostgreSQL is running:**
```bash
# Linux
sudo systemctl status postgresql

# Mac
brew services list

# Windows
# Check Services app
```

**Test connection:**
```bash
psql -h localhost -U identiface -d identiface_db
```

#### 3. Port Already in Use

**Find process:**
```bash
# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### 4. Face Recognition Not Working

**Verify installation:**
```python
import face_recognition
import dlib
print("✓ Libraries installed successfully")
```

**Test with image:**
```python
import face_recognition
image = face_recognition.load_image_file("test.jpg")
encodings = face_recognition.face_encodings(image)
print(f"Found {len(encodings)} face(s)")
```

#### 5. Frontend Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## Verification

### Backend Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "face_recognition": "ready"
}
```

### API Documentation

Visit: http://localhost:8000/api/docs

### Test API Endpoint

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

---

## Next Steps

1. ✅ Complete installation
2. ✅ Create admin account
3. ✅ Test face recognition
4. ✅ Access web interface
5. ✅ Create first case
6. ✅ Build first sketch
7. ✅ Upload suspect photos
8. ✅ Run face matching

---

## Support

### Documentation
- [API Documentation](http://localhost:8000/api/docs)
- [Deployment Guide](DEPLOYMENT.md)
- [Contributing Guide](CONTRIBUTING.md)

### Issues
- Check existing issues on GitHub
- Create new issue with details
- Include error logs

---

**Setup complete! Start building forensic sketches! 🎨🔍**
