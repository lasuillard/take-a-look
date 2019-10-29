FROM python:3.7

# install dependencies
RUN apt update && \
    apt-get install libpq-dev

# python buffer off
ENV PYTHONUNBUFFERED 0

# install pip dependencies
WORKDIR /django
ADD requirements.txt /django/
RUN pip install -r requirements.txt --default-timeout=100

# download helper shell script
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
RUN ["chmod", "u+x", "/wait-for-it.sh"]

# collect statics and update database
ONBUILD RUN python manage.py collectstatic --no-input && \
            python manage.py makemigrations && \
            python manage.py migrate
