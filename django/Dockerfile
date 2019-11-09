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

# add codes

# download helper shell script
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
RUN ["chmod", "u+x", "/wait-for-it.sh"]

# collect statics and update database
ONBUILD RUN python manage.py collectstatic --no-input && \
            python manage.py makemigrations

CMD /wait-for-it.sh postgres:5432 -t 10 && \
    python manage.py migrate && \
    gunicorn --bind 0.0.0.0:8000 core.wsgi
