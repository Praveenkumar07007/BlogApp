pip uninstall celery
pip install celery==5.3.4

make sure you are in /BlogApp directory
    celery -A app.tasks.celery_app worker --pool=solo --loglevel=info


docker pull redis
docker run -d   --name redis-server   -p 6379:6379   -v redis-data:/data   redis redis-server --appendonly yes
docker exec -it redis-server redis-cli
ping

.venv\Scripts\activate
fastapi run main.py
