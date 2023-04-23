# TODO: look into reducing the size of this image
# TODO: add goat counter and remark4
FROM debian:stable-slim

ENV DEBIAN_FRONTEND noninteractive
# used to handle nginx envsubst
ENV DOLLAR $
ENV NGINX_PORT 8080

# update package manager
RUN apt-get update

# install all dependencies available in debian repo
RUN apt-get install -y \
    git \
    curl \
    gnupg2 \
    gettext-base \
    supervisor \
    python3 \
    python3-pip \
    nginx

# install nodejs
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash \
    && apt-get install -y nodejs

# copy all files and set the dest as working dir
COPY . /usr/home/diaryofapolymath
WORKDIR /usr/home/diaryofapolymath

# setup nginx
RUN set -a && . ./.env && set +a \
    && envsubst < ./nginx.conf > ./diaryofapolymath.conf \
    && rm -rf ./nginx.conf \
    && mv ./diaryofapolymath.conf /etc/nginx/conf.d

# setup supervisord config
RUN set -a && . ./.env && set +a \
    && mv ./supervisord.conf ./diaryofapolymath.conf \
    && mv ./diaryofapolymath.conf /etc/supervisor/conf.d

# setup node environment
RUN set -a && . ./.env && set +a \
    && npm ci \
    && npm run build

# setup python environment
RUN set -a && . ./.env && set +a \
    && pip install pipenv \
    && pipenv requirements > requirements.txt \
    && pip3 install -r requirements.txt --no-cache-dir \
    && pip3 uninstall pipenv -y \
    && rm -rf Pipfile*

# setup django environment
RUN set -a && . ./.env && set +a \
    && django-admin makemigrations --no-input \
    && django-admin migrate --no-input \
    && django-admin collectstatic --no-input

# clean up
RUN apt-get -y remove --purge \
    git \
    curl \
    gnupg2 \
    gettext-base \
    nodejs \
    && apt-get -y autoremove \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE ${NGINX_PORT}

ENTRYPOINT ["./run", "start:prod"]