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
COPY supervisor-app.conf /etc/supervisor/conf.d/

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN mkdir /home/bcoffice
WORKDIR /home/bcoffice

RUN git clone -b local https://synco-infra:'Synco!cpdlsql1031'@github.com/syncodax/syncodax-bcoffice-back.git backend

WORKDIR /home/bcoffice/backend
COPY initial.sh /home/bcoffice/backend/
RUN chmod -R 777 /home/bcoffice/backend/initial.sh

ADD base.py /home/bcoffice/backend/bcoffice/bcoffice/settings/base.py
ADD production.py /home/bcoffice/backend/bcoffice/bcoffice/settings/production.py
ADD daemon_config.py /home/bcoffice/backend/daemon/config.py

COPY bcoffice_uwsgi.ini bin/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements/production.txt

WORKDIR /home/bcoffice

RUN mkdir socket \
    logs \
    params

COPY uwsgi_params /etc/nginx/params/uwsgi_params

EXPOSE 8000

CMD ["/home/bcoffice/backend/initial.sh"]
