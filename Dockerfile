FROM python:2-slim

# make sure the system packages are installed
RUN set -x \
    && apt-get update \
    && apt-get install -y gcc \
                          libsqlite3-dev \
                          sqlite3=3.8.* \
                          xclip 

# target directory
ENV     MY_TGT_DIR=/usr/src/pwdhash-vault
RUN     set -x \
        && mkdir -p ${MY_TGT_DIR}
COPY    . ${MY_TGT_DIR}
WORKDIR ${MY_TGT_DIR}

# install all dependencies and the application itself
RUN  set -x \
     && pip install .

# remove unused system packages to lower the image size
RUN set -x \
    && apt-get autoremove --purge -y gcc \
    && apt-get autoremove --purge -y libsqlite3-dev

EXPOSE 8080

CMD ["python", "main.py"]
