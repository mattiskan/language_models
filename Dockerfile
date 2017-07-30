FROM  ubuntu:latest

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:jonathonf/python-3.6 \
    && apt-get update \
    && apt-get install -y python3.6 virtualenv wget make

RUN wget https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64.deb \
    && dpkg -i dumb-init_*.deb

WORKDIR /code
ADD requirements.txt Makefile /code/
RUN touch /code/.nltk_data && make build
ADD . /code

EXPOSE  8084
ENV PYTHONPATH=/code
CMD ["make", "start_webserver"]