FROM python:3.12 AS builder

# Don't buffer `stdout`:
ENV PYTHONUNBUFFERED=1
# Don't create `.pyc` files:
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY manage.py manage.py
COPY ./splootwyze ./splootwyze
COPY ./expenses ./expenses
COPY ./mystaticfiles/ ./mystaticfiles/

# Set dummy value for collectstatic, no need for secret key here
RUN SECRET_KEY_FILE=manage.py python manage.py collectstatic --no-input

EXPOSE 8000/tcp
COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh
CMD ["/app/docker-entrypoint.sh"]
