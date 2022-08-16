FROM python:latest

WORKDIR /usr/src/app

COPY ./flask/requirements.txt ./

COPY ./flask/SCIM ./SCIM
COPY ./flask/uwsgi.ini ./uwsgi.ini
#COPY ./flask/run.py ./run.py
COPY ./start.sh ./start.sh
COPY ./nginx/ssl/scim-server.crt /etc/ssl/certs/scim-server.crt
COPY ./nginx/ssl/scim-server.key /etc/ssl/private/scim-server.key

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

RUN pip install --no-cache-dir -r ./requirements.txt

#CMD ["gunicorn", "-b", "0.0.0.0:5001", "--workers=2", "--threads=4", "--worker-class=gthread", "--log-file=-", "run:app"]
COPY ./nginx/nginx.conf /etc/nginx
RUN chmod +x ./start.sh
RUN chmod o+rw ./SCIM/.cache
CMD ["./start.sh"]
EXPOSE 443