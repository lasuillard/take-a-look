FROM python:3.7

# install dependencies
RUN apt update && \
    apt-get install libpq-dev

# python buffer off
ENV PYTHONUNBUFFERED 0

# install pip dependencies
WORKDIR /django
COPY . .
RUN pip install -r requirements.txt --default-timeout=100

# download helper shell script
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
RUN ["chmod", "u+x", "/wait-for-it.sh"]

# make migration files
ONBUILD RUN python manage.py makemigrations

# TODO: migrations should be performed only one time for all pods
CMD /wait-for-it.sh svc-db:5432 -t 10 && \
    gunicorn --bind 0.0.0.0:8000 core.wsgi
