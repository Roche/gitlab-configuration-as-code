FROM python:3.8-alpine

WORKDIR /workspace
COPY requirements.txt ./
RUN pip --no-cache-dir install -r requirements.txt

COPY bin ./bin
COPY gcasc ./gcasc
COPY utils ./utils
ENV PYTHONPATH /workspace
ENV GITLAB_CONFIG_FILE gitlab.yml
CMD [ "bin/gcasc" ]