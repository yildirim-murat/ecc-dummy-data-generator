FROM python:latest

WORKDIR /app

COPY . /app/

RUN chmod -R 755 /app

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]