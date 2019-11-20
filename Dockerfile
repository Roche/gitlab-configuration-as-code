FROM python:3.8-alpine
ARG GCASC_PATH=/opt/gcasc
ARG WORKSPACE=/workspace

WORKDIR ${GCASC_PATH}
COPY requirements.txt ./
RUN pip --no-cache-dir install -r requirements.txt

COPY bin ./bin
COPY gcasc ./gcasc

RUN ln -s ${GCASC_PATH}/bin/gcasc /usr/local/bin/gcasc

ENV PYTHONPATH ${GCASC_PATH}
ENV GITLAB_CLIENT_CONFIG_FILE ${WORKSPACE}/gitlab.cfg
ENV GITLAB_CONFIG_FILE ${WORKSPACE}/gitlab.yml

WORKDIR ${WORKSPACE}
CMD [ "gcasc" ]