from celery import Celery

app = Celery ( broker='pyamqp://guest@localhost//')

@app.task
def ola_mundo():
    for a in range(10):
        c=a

    return f"ola mundo! {a} vezes"

