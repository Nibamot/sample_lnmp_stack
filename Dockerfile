FROM php:7.2-fpm
RUN apt update
RUN apt install -y python3-pip
RUN pip3 install mysql-connector-python