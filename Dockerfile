FROM python:2-alpine

ENV WWW_PATH /opt/www
RUN mkdir -p ${WWW_PATH}
WORKDIR ${WWW_PATH}
COPY . ${WWW_PATH}

RUN pip install virtualenv

RUN virtualenv /env && /env/bin/pip install -r requirements.txt

EXPOSE 8080
CMD ["/env/bin/python", "main.py"]