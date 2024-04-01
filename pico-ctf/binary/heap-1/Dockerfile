FROM ubuntu:22.04
RUN apt-get update && apt-get upgrade -y
RUN apt-get install libssl-dev
RUN apt-get install -y -q build-essential curl git
RUN git clone https://github.com/pwndbg/pwndbg && cd pwndbg && ./setup.sh
ENV LC_CTYPE C.UTF-8

COPY ./chall /chall
