# Sample LNMP stack
 Linux, Nginx, MySQL and PHP in this case

# GOAL
To setup a simple nginx and mysql application and display data fom mysql using nginx while exposing nginx and keeping mysql under wraps. 

# PLAN
We can divide the documentation below into 2 parts.
The first part being the testing of these components in the local docker setup. The second part describes the process of securely deploying the solution on the cloud-premises.  

Before we dig into the specifics of each process , there are a few components that are common to both and a short description is provided below.

1. **NGINX**
NGINX along wih Apache is one of the most widely used web-servers. to act as a reverse proxy. By default it serves on port 80.

2. **PHP-FPM**
PHP-FPM stands for PHP-FastCGI Process Manager. This is primarily used for interfacing interactive programs with the web-server(Not just plain HTML) Simply put, the the PHP-FPM is reponsible in this scenario for loading the data. By default it works on the port 9000. The PHP output is then served through nginx. 

3. **MySQL**
MySQl is an example of a well-used database among monolithic and microservices architecture. It serves on port 3306 by default.




## Part one: Docker-Compose
To test the working of this simple LNMP setup I wrote a docker-compose. The docker-compose has the following components. The docker-compose is a simple single line command to be run provided docker is installed. This makes testing way easier to configure, test and troubleshoot.



1. **NGINX**
A custom image of nginx including the nginx.conf was built so that it can be used to act as a reverse proxy for PHP based execution of python script. The nginx server serves on port 8080 (default is 80), which is then forwarded on port 8085 to avoid confusions with any other port allocations.

2. **PHP**
Another custom image of php-fpm was was built. The PHP output is then served through nginx. The environment variables for the mysql is set in the PHP container as well because it needs to access the DB. On the cloud-premises this would be retrieved from secrets or something of that ilk.

3. **MySQL**
MySQl acts as the database from which nginx-php duo retrieve data. The `testdb.py` script simply creates a table and keeps adding and entry to the table in the database every time the script is run. 


With the `docker-demo` folder in place, one has to simply run the `docker-compose up -d` command. Then application springs up and you can check http://localhost:8085 shows a sample output from the database. It can be torn down as easily as it was brought up with the command `docker-compose down`.


## Part two: Kubernetes deployment
I have used minikube as an example of a cloud-premise. 
This application has been packaged into a helmchart for sake of automation in deployment. Helming also makes our job easier to upgrade and track applications. 

We will go though the components that need to be used in our K8s deployment.

1. **Nginx and PHP**
A deployment (`nginx-php-deployment`) in which each pod contains one `nginx` container and a Custom `phpapp` container is setup. The Php image is custom in order to allow the container to access and retrieve data from the Mysql DB. An appropriate NodePort based service (nginx-php-svc) on port 30600 from default port 80 is setup for this deployment such that it can accessed. We have setup the `nginx.conf` file  using a config map named `nginx-config-volume`.  Also, the phpapp has been configured to receive the MySQL access credentials though secrets and config-maps. The nginx-php-deployment is also served by a Persistent Volume named `data-store-pv` that shares the index.php and testdb.py on the hostpath `data_scripts`. I have also setup a Horizontal Pod Autoscaler for this deployment with the autoscaler triggered if the cpu utilization goes beyond 90% (just an example) .

2. **MySQL**
A deployment named `mysql-deployment` is in place to serve as the DB. The deployment has been exposed as a ClusterIP (mysql-svc) on the default port 3306. The MySQL deployment also has a Persistent Volume to keep it's data stateful and if one pod goes down another one will come up and be able to access the previous state. Horizontal Pod Autoscaler has been applied to this one as well

Within the helm charts I have also included a simple test-case to test the functioning of the endpoint.

We can run this chart by adding the helm repo:
1. `helm repo add <repo-name> https://raw.githubusercontent.com/Nibamot/sample_lnmp_stack/master`
2. `helm install <custom-chart-name> <repo/chart-name>` to install the helm chart.
3. This chart can be removed simply by doing a `helm uninstall <custom-chart-name>`