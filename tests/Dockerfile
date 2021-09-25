ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}-slim

ARG USER_ID=1000
ARG GROUP_ID=1000
RUN set -x ; \
    if [ "${GROUP_ID}" != 0 ]; then \
        groupadd -g "${GROUP_ID}" pytest ; \
    fi && \
    if [ "${USER_ID}" != 0 ]; then \
        useradd -g "${GROUP_ID}" -u "${USER_ID}" pytest ; \
    fi

WORKDIR /tmp

COPY ./requirements.txt /tmp/
RUN pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

COPY ./tests/requirements.txt /tmp/
RUN pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -yq \
   ffmpeg \
   && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN mkdir /project && \
    chown "${USER_ID}":"${GROUP_ID}" /project

USER "${USER_ID}"

WORKDIR /project

CMD ["pytest", "-v", "--html=out/report.html", "--self-contained-html"]
