# Sample LNMP stack
 Linux, Nginx, MySQL and PHP in this case

# GOAL
To setup a simple nginx and mysql application and display data fom mysql using nginx while exposing nginx and keeping mysql under wraps. 

# PLAN
We can divide the documentation below into 2 parts.
The first part being the testing of these components in the local docker setup. The second bit was

## Part one: Docker-Compose
To test the working of this simple LNMP setup I wrote a docker-compose. The docker-compose has the following components.

1. **NGINX**
A custom image of nginx including the nginx.conf was built so that it can be used to act as a reverse proxy for PHP based execution of python script. The nginx server serves on port 8080 

2. **PHP**
Another custom image of php-fpm was was built. PHP-FastCGI Process Manager. Simply put, the the PHP-FPM is reponsible in this scenario for loading the data

3. **MySQL**
MySQl acts as the database from which nginx-php duo retrieve data. The `testdb.py` script simply creates a table and keeps adding and entry to the table in the database every time the script is run. 




## Part two: Kubernetes deployment

We will first go though the components that need to be used in our K8s deployment.
1. **Nginx as a webserver**
The primary component is a simple nginx webserver which I configure to be a reverse proxy for PHP
