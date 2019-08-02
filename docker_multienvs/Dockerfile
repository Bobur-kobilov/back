FROM ubuntu:16.04

LABEL maintainer="bcg <dev@blockchainglobal.co.kr>"

#ENV HOME /root
#CMD ["/sbin/my_init"]

RUN apt-get update && \
    apt-get upgrade -y && \     
    apt-get install -y \
        git \
        libmysqlclient-dev \
        nginx \
        libpcre3 \
        libpcre3-dev \
        supervisor \
        python3 \
        python3-dev \
        python3-setuptools \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app-dev.conf /etc/supervisor/conf.d/
COPY supervisor-app-stage.conf /etc/supervisor/conf.d/
COPY supervisor-app-production.conf /etc/supervisor/conf.d/

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN mkdir /home/bcoffice
WORKDIR /home/bcoffice

RUN git clone -b dev https://bcg-dev:'bcGCha!ng1oba!'@github.com/syncodax/syncodax-bcoffice-back.git backend

WORKDIR /home/bcoffice/backend
COPY initial.sh /home/bcoffice/backend/
RUN chmod -R 777 /home/bcoffice/backend/initial.sh

ADD settings/base.py /home/bcoffice/backend/bcoffice/bcoffice/settings/base.py
ADD settings/dev.py /home/bcoffice/backend/bcoffice/bcoffice/settings/dev.py
ADD settings/stage.py /home/bcoffice/backend/bcoffice/bcoffice/settings/stage.py
ADD settings/production.py /home/bcoffice/backend/bcoffice/bcoffice/settings/production.py

ADD settings/daemon_dev.py /home/bcoffice/backend/daemon_multienvs/config_dev.py
ADD settings/daemon_stage.py /home/bcoffice/backend/daemon_multienvs/config_stage.py
ADD settings/daemon_production.py /home/bcoffice/backend/daemon_multienvs/config_production.py

COPY bcoffice_uwsgi_dev.ini bin/
COPY bcoffice_uwsgi_stage.ini bin/
COPY bcoffice_uwsgi_production.ini bin/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements/production.txt

WORKDIR /home/bcoffice

RUN mkdir socket \
    logs \
    params

COPY uwsgi_params /etc/nginx/params/uwsgi_params

EXPOSE 8000

ENTRYPOINT ["/home/bcoffice/backend/initial.sh"]
