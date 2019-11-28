FROM nginx:1.17-alpine

# copy template
COPY service.template /etc/nginx/conf.d/service.template

# fill template and run nginx
CMD envsubst '$$API_SERVER_URL $$JSP_SERVER_URL' \
        < /etc/nginx/conf.d/service.template > /etc/nginx/conf.d/default.conf && \
    nginx -g 'daemon off;'
