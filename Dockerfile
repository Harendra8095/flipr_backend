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
ADD heroku-exec.sh /app/.profile.d
COPY --from=python-build-env /root/.cache /root/.cache
RUN cd /app && pip install -r requirements.txt && rm -rf /root/.cache && python manage.py restart
#RUN chmod +x launch.sh
CMD ["python", "-u" ,"server.py"]
# CMD ["gunicorn", "server:app"]
