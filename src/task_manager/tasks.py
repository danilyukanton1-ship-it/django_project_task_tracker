from celery import shared_task
import time

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y

@shared_task
def hard_task():
    time.sleep(5)
    return 'Hard task has been completed'

@shared_task
def task_every_220_secs():
    return f'Task 1: {time.time()}'

@shared_task
def task_for_evenings():
    return f'Task 2: {time.time()}'

@shared_task
def sunrise_notification_task():
    print(f'[{time.time()}] WAKE UP!')

