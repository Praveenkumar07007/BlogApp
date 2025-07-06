# BlogApp - FastAPI Blog Application

A modern blog application built with FastAPI, featuring authentication, real-time tasks with Celery, and Redis caching.

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Database**: SQLAlchemy ORM
- **Authentication**: JWT + OAuth2
- **Task Queue**: Celery
- **Cache/Broker**: Redis
- **Server**: Uvicorn
- **Email**: Pydantic email validation

## 📋 Prerequisites

- Python 3.8+ installed
- Docker (for Redis)
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Praveenkumar07007/BlogApp.git
cd BlogApp
```

### 2. Set Up Virtual Environment

**Option A: Using PowerShell**
```powershell
# Create virtual environment (if not exists)
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate
```


### 3. Install Dependencies
```bash
# Make sure you're in the BlogApp root directory
pip install -r app/requirements.txt
```

### 4. Set Up Redis (Docker)

**Start Redis Server:**
```bash
# Pull Redis image
docker pull redis

# Run Redis container
docker run -d \
  --name redis-server \
  -p 6379:6379 \
  -v redis-data:/data \
  redis redis-server --appendonly yes
```

**Test Redis Connection:**
```bash
# Connect to Redis CLI
docker exec -it redis-server redis-cli

# Test connection (should return PONG)
ping

# Exit Redis CLI
exit
```

### 5. Environment Configuration

Create a `.env` file in the app directory:
```bash
# Copy from example (create this file with your settings)
cp app/.env.example app/.env
```

Example `.env` content:
```env
DATABASE_URL=sqlite:///./blog.db
SECRET_KEY=your-secret-key-here
REDIS_URL=redis://localhost:6379
```

## 🏃‍♂️ Running the Application

### Method 1: Development Server
```bash
# Make sure you're in BlogApp root directory and virtual environment is active
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Method 2: FastAPI CLI (if available)
```bash
cd app
fastapi run main.py
```

The application will be available at: http://localhost:8000

## 🔄 Running Background Tasks (Celery)

In a separate terminal, start the Celery worker:

```bash
# Make sure you're in BlogApp root directory
celery -A app.tasks.celery_app worker --pool=solo --loglevel=info
```

**Note**: The `--pool=solo` flag is required for Windows compatibility.

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Development Workflow

### Daily Development Setup
1. Navigate to project directory
2. Activate virtual environment: `.\activate`
3. Start Redis: `docker start redis-server` (if stopped)
4. Start FastAPI: `cd app && uvicorn main:app --reload`
5. Start Celery worker (separate terminal): `celery -A app.tasks.celery_app worker --pool=solo --loglevel=info`

### Package Management
```bash
# Install new package
pip install package-name

# Update requirements.txt
pip freeze > app/requirements.txt

# Install from requirements
pip install -r app/requirements.txt
```

## 🐳 Docker Commands Reference

### Redis Management
```bash
# Start existing container
docker start redis-server

# Stop container
docker stop redis-server

# View logs
docker logs redis-server

# Remove container (careful!)
docker rm redis-server

# List running containers
docker ps
```

## 🔧 Troubleshooting

### Virtual Environment Issues
```bash
# If activation fails, recreate virtual environment
rmdir /s .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
```

### Redis Connection Issues
```bash
# Check if Redis is running
docker ps | findstr redis

# Restart Redis container
docker restart redis-server

# Check Redis logs
docker logs redis-server
```

### Celery Issues
```bash
# Clear Celery cache
celery -A app.tasks.celery_app purge

# Check Celery status
celery -A app.tasks.celery_app status
```

## 📁 Project Structure
```
BlogApp/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── requirements.txt     # Python dependencies
│   ├── tasks/
│   │   └── celery_app.py   # Celery configuration
│   └── ...
├── .venv/                   # Virtual environment (auto-created)
├── .gitignore              # Git ignore rules
├── activate.bat            # Convenience activation script
└── README.md               # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Commit: `git commit -am 'Add feature'`
5. Push: `git push origin feature-name`
6. Create a Pull Request

## 📝 License

This project is licensed under the MIT License.

---

## 🔗 Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Redis Documentation](https://redis.io/documentation)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
