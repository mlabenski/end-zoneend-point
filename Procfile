web: gunicorn wsgi:app
worker: rq worker -u $REDIS_URL