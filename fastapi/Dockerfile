FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install torch==1.7.1+cpu  -f https://download.pytorch.org/whl/torch_stable.html

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app /app

COPY ./model /models

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "/gunicorn_conf.py", "main:app"]