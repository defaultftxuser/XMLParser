from celery import Celery
from celery.schedules import crontab

from src.common.settings.config import ProjectSettings


settings = ProjectSettings()

app = Celery(
    main=settings.celery_name,
    broker=settings.get_redis_url,
    backend=settings.get_redis_backend_url,
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

app.autodiscover_tasks(["src.infra.celery.tasks"])

app.conf.beat_schedule = {
    "task-every-hour": {
        "task": "src.infra.celery.tasks.gpt_task",
        "schedule": crontab(minute="0", hour="*"),
    },
}


app.conf.timezone = "UTC"
