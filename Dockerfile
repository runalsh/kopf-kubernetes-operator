FROM python:alpine

ENV APPDIR /app
ENV PYTHONUNBUFFERED 1
RUN mkdir $APPDIR
WORKDIR $APPDIR

COPY requirements.txt /tmp/
RUN apk update && \
    apk add --no-cache --virtual .build-deps gcc python3-dev py-configobj linux-headers libc-dev \
    && pip install  --use-deprecated=legacy-resolver --no-cache-dir -r /tmp/requirements.txt \
    && addgroup -S app && adduser -S app -G app\
    && chown -R app:app $APPDIR \
    && apk del .build-deps  \
    && rm -rf /var/cache/apk/*  \
    && rm -rf  /tmp/*

COPY --chown=app:app . .
USER app
CMD ["kopf", "run", "-A", "--standalone", "/app/main.py"]