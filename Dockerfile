FROM python:3.4
MAINTAINER ckreuzberger@localhost

#COPY ./engage_project/ /app/engage_project
#
#COPY ./engage/ /app/engage
#
#COPY ./requirements.txt /app
COPY ./app /app

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
