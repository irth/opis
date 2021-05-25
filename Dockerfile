FROM python:3-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP main.py
ENV FLASK_DEBUG 0
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt && pip install gunicorn
COPY ./ /app
WORKDIR /app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]

