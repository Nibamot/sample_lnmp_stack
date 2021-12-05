FROM php:7.2-fpm  
RUN apt update
RUN apt install -y python3-pip
RUN pip3 install mysql-connector-python
RUN docker-php-ext-install pdo_mysql 
COPY testdb.py /var/www/html/testdb.py
COPY index.php /var/www/html/index.php