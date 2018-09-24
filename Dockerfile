FROM dorowu/ubuntu-desktop-lxde-vnc
MAINTAINER nosix

RUN apt-get update
RUN apt-get -y install python3-pip python3-tk git
RUN apt-get -y upgrade
RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN pip3 install git+https://github.com/nosix/raspberry-gpio-emulator/

ENV USER=pi
ENV PASSWORD=raspbrry
ENV HOME=/home/pi

RUN mkdir $HOME
WORKDIR $HOME
RUN mkdir samples
COPY samples/*.py samples/
RUN mkdir work
RUN echo "alias python=python3.6" > .bashrc
