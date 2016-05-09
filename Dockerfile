FROM alpine:3.3

ENV WWW_PATH /opt/www
RUN mkdir -p ${WWW_PATH}
WORKDIR ${WWW_PATH}
COPY . ${WWW_PATH}

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

RUN virtualenv /env && /env/bin/pip install -r requirements.txt

EXPOSE 8080
CMD ["/env/bin/python", "main.py"]