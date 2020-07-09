FROM python:3.8 as aam_aadmi_aspataal-base

ENV DOCKERIZE_VERSION v0.6.1

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
                       build-essential \
                       git \
                       libpq-dev \
                       libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# PostgreSQL client
RUN curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
ENV PG_MAJOR 12
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main' $PG_MAJOR > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
                       postgresql-client-$PG_MAJOR \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code

RUN mkdir /code/aam_aadmi_aspataal
WORKDIR /code/aam_aadmi_aspataal

COPY requirements.txt /code/aam_aadmi_aspataal/
RUN pip3 install --no-cache-dir -r requirements.txt
RUN useradd --create-home --shell /bin/bash aam_aadmi_aspataal

# Now install our code, which may change frequently
COPY . /code/aam_aadmi_aspataal/

WORKDIR /code/aam_aadmi_aspataal