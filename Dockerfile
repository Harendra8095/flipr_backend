FROM python:3.6-alpine AS python-build-env
LABEL maintainer="Vishnu"
RUN apk update && apk add ca-certificates && apk add libpq postgresql-dev && apk add libffi-dev \
    && apk add build-base && rm -rf /var/cache/apk/*
WORKDIR /app
ADD requirements.txt /app
RUN cd /app && pip install -r requirements.txt

FROM python:3.6-alpine
LABEL maintainer="Vishnu"
RUN apk update && apk add ca-certificates && apk add libpq postgresql-client
WORKDIR /app
ADD . /app
COPY --from=python-build-env /root/.cache /root/.cache
RUN cd /app && pip install -r requirements.txt && rm -rf /root/.cache
#RUN chmod +x launch.sh
ENV DATABASE_URL=postgres://ycaffmkrsgyjsm:95e7001c889477e404a8b767df66b68907039b6cb451881501105e3880b64603@ec2-54-90-211-192.compute-1.amazonaws.com:5432/df0lpdam7ipsq1
CMD ["python", "-u" ,"server.py"]
# CMD ["gunicorn", "server:app"]
