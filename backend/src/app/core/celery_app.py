from celery import Celery
from app.core.config import settings

BROKER = f'amqp://{settings.RABBITMQ_DEFAULT_USER}:{settings.RABBITMQ_DEFAULT_PASS}@{settings.HOSTNAME}:{settings.RABBITMQ_NODE_PORT}/{settings.RABBITMQ_DEFAULT_VHOST}'
celery_app = Celery("worker", broker=BROKER)

celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
