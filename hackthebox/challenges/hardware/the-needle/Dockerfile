FROM ubuntu:latest

# Get necessary packages
RUN apt-get update && apt-get install busybox-static fakeroot git dmsetup kpartx netcat-openbsd nmap python3-psycopg2 snmp uml-utilities util-linux vlan python3-setuptools file -y --fix-missing
RUN apt-get install p7zip-full p7zip-rar --fix-missing -y
RUN git clone --recursive https://github.com/firmadyne/firmadyne.git
RUN git clone https://github.com/ReFirmLabs/binwalk.git

# Install binwalk on device
WORKDIR /binwalk
RUN python3 ./setup.py install


# Import the firmware image

# Install sasquatch
RUN apt-get update && apt-get install make wget zlib1g-dev liblzma-dev liblzo2-dev --fix-missing -y
RUN apt-get install build-essential manpages-dev --fix-missing -y

WORKDIR /
RUN git clone https://github.com/devttys0/sasquatch
WORKDIR ./sasquatch
#RUN ./build.sh

# Copy firmware
WORKDIR /
COPY ./firmware.bin /firmware.bin


