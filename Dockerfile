# syntax=docker/dockerfile:1

FROM python:3.12-alpine3.20

WORKDIR /app
COPY requirements.txt requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn","main:app", "--reload","--host", "0.0.0.0"]

