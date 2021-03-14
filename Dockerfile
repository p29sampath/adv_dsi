FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app /app

COPY ./model /models

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "/gunicorn_conf.py", "main:app"]