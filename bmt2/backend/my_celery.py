from celery import Celery
celery_app= Celery(
    "BMT2",  
    broker="redis://localhost:6379/0",  # URL to your Redis broker
    backend="redis://localhost:6379/0",
      include=['exportCSV','send_email'],  # URL to your Redis backend
)

# Load task modules from all registered Flask apps
celery_app.conf.update(
    result_backend="redis://localhost:6379/0",
    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
    timezone="Asia/Kolkata",
)
