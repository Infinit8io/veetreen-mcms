FROM ubuntu:trusty

RUN apt-get update && apt-get install -y \
		sqlite3 \
		python3-pip \
        libmysqlclient-dev \
        python-mysqldb \
        python-dev \
        curl \
        apt-transport-https \
        git

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install -y yarn
RUN curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
RUN apt-get install -y nodejs

ADD ./requirements.txt .
ADD . ./data/web/whatineed

ENV DJANGO_VERSION 1.11
ENV GUNICORN_VERSION 19.3.0

RUN pip3 install django==${DJANGO_VERSION}
RUN pip3 install gunicorn==${GUNICORN_VERSION}
RUN pip3 install -r requirements.txt
RUN apt-get autoremove -y

RUN cd /data/web/whatineed && yarn && npm run production && python3 manage.py makemigrations

VOLUME /data/web/whatineed
