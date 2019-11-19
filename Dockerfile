FROM python:3.8-alpine

WORKDIR /workspace
COPY requirements.txt ./
RUN pip --no-cache-dir install -r requirements.txt

COPY bin ./bin
COPY gcasc ./gcasc
ENV PYTHONPATH /workspace
ENV GITLAB_CLIENT_CONFIG_FILE gitlab.cfg
ENV GITLAB_CONFIG_FILE gitlab.yml
CMD [ "bin/gcasc" ]