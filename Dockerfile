FROM openjdk:8-jdk-alpine
VOLUME /tmp
# see https://devcenter.heroku.com/articles/exec#enabling-docker-support
RUN apk add --no-cache curl bash openssh python
ADD src/main/docker/heroku-exec.sh /app/.profile.d/heroku-exec.sh
RUN chmod a+x /app/.profile.d/heroku-exec.sh
ADD src/main/docker/sh-wrapper.sh /bin/sh-wrapper.sh
RUN chmod a+x /bin/sh-wrapper.sh
RUN rm /bin/sh && ln -s /bin/sh-wrapper.sh /bin/sh


FROM python:3.6-alpine AS python-build-env
LABEL maintainer="Harry"
RUN apk update && apk add ca-certificates && apk add libpq postgresql-dev && apk add libffi-dev \
    && apk add build-base && rm -rf /var/cache/apk/*
WORKDIR /app
ADD requirements.txt /app
RUN cd /app && pip install -r requirements.txt

FROM python:3.6-alpine
LABEL maintainer="Harry"
RUN apk update && apk add ca-certificates && apk add libpq postgresql-client
WORKDIR /app
ADD . /app
COPY --from=python-build-env /root/.cache /root/.cache
RUN cd /app && pip install -r requirements.txt && rm -rf /root/.cache
#RUN chmod +x launch.sh
CMD ["python", "-u" ,"server.py"]
# CMD ["gunicorn", "server:app"]
