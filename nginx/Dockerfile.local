FROM nginx:1.17-alpine

# copy template
COPY service.template /etc/nginx/conf.d/service.template

# fill template and run nginx
CMD envsubst '$$DJANGO_HOST $$DJANGO_PORT  \
              $$TOMCAT_HOST $$TOMCAT_PORT' \
        < /etc/nginx/conf.d/service.template > /etc/nginx/conf.d/default.conf && \
    nginx -g 'daemon off;'
