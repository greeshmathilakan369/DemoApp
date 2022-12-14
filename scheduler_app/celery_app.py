from os import environ
from flask import Flask
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import timedelta
from twiiter_data_fetch import fetch_data
app = Flask(__name__)
logger = get_task_logger(__name__)

def make_celery(app):
    #Celery configuration
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config['CELERYBEAT_SCHEDULE'] = {
        'periodic_task-every-minute': {
            'task': 'periodic_task',
            'schedule': timedelta(seconds=600),
        }
    }

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

@celery.task(name="periodic_task")
def periodic_task():
    res = fetch_data()
    logger.info("Hello! from periodic task")

@app.route('/')
def view():
    return "Hello, Flask is up and running!"


if __name__ == "__main__":
    app.run(debug = True)