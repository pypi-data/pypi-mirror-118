FROM python:3-slim

RUN buildDeps='gcc libc6-dev make' && \
    set -x && \
    apt-get update && apt-get install -y $buildDeps --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir tormicro==0.0.1.4 && \
    mkdir /app && \
    apt-get purge -y --auto-remove $buildDeps

WORKDIR /app

ENTRYPOINT [ "tormicro" ]
CMD [ "-h" ]