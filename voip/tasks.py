from celery import Celery
import time
# from .models import ActiveChannels  
import asterisk.manager
import django

django.setup()
app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def update_asterisk_data():
    print("tes")
   
@app.task
def schedule_print_task():
    while True:
        update_asterisk_data.delay()
