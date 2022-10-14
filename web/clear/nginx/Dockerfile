FROM nginx:latest 

COPY ./nginx.conf /etc/nginx/conf.d/vhost.conf 
COPY ./key.pem /tmp/key.pem 
COPY ./cert.pem /tmp/cert.pem


EXPOSE 443
