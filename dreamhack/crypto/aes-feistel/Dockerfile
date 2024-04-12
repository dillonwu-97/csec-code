FROM ubuntu:22.04@sha256:965fbcae990b0467ed5657caceaec165018ef44a4d2d46c7cdea80a9dff0d1ea

RUN apt update
RUN apt-get install -y socat python3 python3-pip
RUN pip install pycryptodome


COPY ./deploy/flag /flag
COPY ./deploy/prob.py /prob.py
COPY ./deploy/cipher.py /cipher.py

RUN chmod 755 /flag /prob.py

EXPOSE 1119

CMD socat TCP-LISTEN:1119,reuseaddr,fork EXEC:/prob.py