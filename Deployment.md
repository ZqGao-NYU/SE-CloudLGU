## Deployment 

### Local Deployment

---

Local deployment is much easier, and it can be used to test the functionality of our applications. All of the settings and deployments can be done in minutes. All we need to do is to set up the front-end client, back-end server, and the database. And adjust the address of the routers, then we are all done.

### **Firstly, we can set up the front-end:**

#### Build Setup


```bash
# clone the project
git clone git@github.com:118010077/SE-CloudLGU.git

# enter the project directory
cd SE-CloudLGU

# install dependency
npm install

# develop
npm run dev
```

This will automatically open http://localhost:9528

#### Build

```bash
# build for test environment
npm run build:stage

# build for production environment
npm run build:prod
```

#### Advanced

```bash
# preview the release environment effect
npm run preview

# preview the release environment effect + static resource analysis
npm run preview -- --report

# code format check
npm run lint

# code format check and auto fix
npm run lint -- --fix
```

#### Browsers support

Modern browsers and Internet Explorer 10+.

| [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/edge/edge_48x48.png" alt="IE / Edge" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>IE / Edge | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/firefox/firefox_48x48.png" alt="Firefox" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Firefox | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/chrome/chrome_48x48.png" alt="Chrome" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Chrome | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/safari/safari_48x48.png" alt="Safari" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Safari |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| IE10, IE11, Edge                                             | last 2 versions                                              | last 2 versions                                              | last 2 versions                                              |

### Then, set up the database with MySQL:

This step is simple, just make sure that we have correct Hostname, Port, Username, and Password, and be sure that the user being used have the authority to read and write to the database. 



Also, remember those parameters, and they will be used in the next step.

<img src="C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220512160208552.png" alt="image-20220512160208552" style="zoom:67%;" />

![image-20220512160418115](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220512160418115.png)

### Finally, about the Django back-end:

#### Settings.py

Firstly, we need to adjust some settings so that we can communicate with the client. We need firstly enable CORS headers in the project and add the address of the client into our whitelist:

Add the following content into the `settings.py`. Remember to update your URLs in `CORS_ORIGIN_WHITELIST` to the URL of front-end. 

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'webpack_loader',
    'accounts',
    'OfficeHour',
    'forum'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'DEFAULT_RENDERER_CLASSES': (
    'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.BasicAuthentication',
]
}

CORS_ORIGIN_WHITELIST = (
    'http://localhost:9528',
    'http://10.30.201.27:9528',  # Set it to your Vue.js client's address
)
```

**Caution: It is dangerous to use the hard-coded password and address directly, remember to read those critical information from another files before publish this application:**

Then, update the information in the `DATABASE` field like this with the following content:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # DBMS you used
        'NAME': 'csc4001',  # Name of the schemas
        'USER': 'root',  # Username
        'PASSWORD': 'GgGg657199',  # Password
        'HOST': '127.0.0.1',  # Address of DB
        'PORT': '3306',  # Port of DB
    }
}
```

Also, we can add some settings about our SMTP email service just like this:

```python
# Email Service
CONFIRM_TIME = 30
DEFAULT_FROM_EMAIL = '13141391404@163.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = '13141391404@163.com'
EMAIL_HOST_PASSWORD = 'KTRHGXYRRFQFFDJW'
EMAIL_PORT = 25
```

`EMAIL_HOST`, `EMAIL_BACKEND`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and `EMAIL_PORT` can be set up and get when you start up your SMTP service.

---

## Deploy with Nginx and uWSGI

### Basic Introduction

When users visit a web site, they need to send requests to the Web Server (we use Nginx here). As web pages become more complex and user input becomes more diverse, we need to build a script into the child process that converts the user's input and requests into HTML for the user's browser to use. The scripting Interface defined by Python is Web Server Gateway Interface (WSGI). The uWSGI installed in this article implements the same functionality as WSGI, while being more productive and itself can be accessed as a server.

At the same time, since we need to implement the separated front-end and back-end architecture, we need to solve the cross-domain problem of the front-end and back-end, how to set up Nginx is the most important problem.



**We deploy our Nginx client server at https://10.30.201.27:9528, and our uWSGI server at  http://10.30.201.28:8080**

Also, we use CentOS7.8 to be our operating system. It is much easier and convenient to deploy our servers on Linux.

#### Install Nginx and Allow HTTP Connection

Credit to https://qizhanming.com/blog/2018/08/06/how-to-install-nginx-on-centos-7

1. Firstly, we add a new Yum source so that we can download Nginx from that image:

   > ```
   > sudo rpm -ivh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
   > ```

2. Install EPEL Extension 

   > sudo yum install epel-release  

3. Install Nginx

   > sudo yum install nginx

4. Firewall Setting

   > sudo firewall-cmd --zone=public --permanent --add-service=http       
   > sudo firewall-cmd --zone=public --permanent --add-service=https   
   > sudo firewall-cmd --reload  

5. Startup Nginx
   Setting Nginx to run on startup:

   > sudo systemctl enable nginx

   Start Nginx Service:

   > sudo systemctl start nginx

   Then we can get the following result showing we have successfully startup our Nginx server:

![image-20220512171901969](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220512171901969.png)

### Deploy Django Back-end Application (Set up uWSGI)

1. Install Python3
   Update Yum

   > yum update -y

   Install Python3 

   > yum install -y python 3

2. Choose your working directory and clone the source code from Git Repository

   > sudo yum install git
   >
   > git clone https://github.com/118010077/SE-CloudLGU.git

3. Before we deploy the application, we need to product our source code's information:

   > DEBUG = False

   Set `DEBUG` in `settings.py` to *False*.

4. Create Virtual Environment and Install relevant required libraries

   > sudo pip3 install virtualenv -i https://pypi.tuna.tsinghua.edu.cn/simple

   Start the virtual environment 

   > virtualenv venDjango
   >
   > cd .venDjango/
   >
   > source ./bin/activate

   Install relevant libraries:

   > pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r ../SE-CloudLGU/src/Back-End/Requirements/common.txt

   Some of our libraries require you to have C language complier, and we need to install them right now:

   > yum install -y pcre pcre-devel pcre-static
   >
   > sudo yum group install "Development Tools"

5. Install uWSGI

   > yum -y install python36-devel
   >
   > pip install uwsgi -l --no-cache-dir

6. Set up uWSGI:

   Go to the directory of your Django source code, and create `uwsgi.ini`, and input the following content:

   ```bash
   [uwsgi]
   socket= 10.30.201.28:8001
   http = 10.30.201.28:8080
   chdir = /home/CloudLGU/src/Back-End/Back-End/ # Location of Working Directory
   py-autoreload=1
   wsgi-file = /home/CloudLGU/src/Back-End/Back-End/wsgi.py
   master = true
   pidfile = uwsgi.pid
   enable-threads = true
   thunder-lock = true
   home = /home/CloudLGU/venvDjango
   daemonize = uwsgi.log  # Where to save your uWSGI log
   ```

   

7. Start your server
   Before you start the server, please follow the instruction from the **Local Deployment - Part  2 and 3's DB setting and Django Setting**

   > python manage.py runserver

   If the server starts successfully,  we can use the following instruction to start uWSGI

   > Start： uwsgi --ini uwsgi.ini
   >
   > Stop: uwsgi --stop uwsgi.pid
   >
   > Restart: uwsgi --stop uwsgi.pid

   

### Deploy the Vue.js with Nginx

1. Install Node.js:
   Firstly, use `curl` to add image to the yum repository, and install Node.js and npm.

   > curl -sL https://rpm.nodesource.com/setup_10.x | sudo bash -  
   > sudo yum install nodejs  

2. Build the front end and prepare it for the production environment

   > cd /home/CloudLGU/src/Front-End/
   >
   > npm install express --registry=https://registry.npm.taobao.org  # Download from images at home
   >
   > npm run build

   Then we will have a directory called `dist` with the built code.

3. Set up Nginx

   > sudo vi  /etc/nginx/nginx.conf

   Add the following information to the location/block of the Server module and modify the basic information of the Server block. Note that Conf part is not the final version. It is only used as an example.

   ```bash
       server {
           listen       9528 10.30.201.27; # Deploy your server at port 80
           listen       [::]:9528 10.30.201.27;
           server_name  cloudLGU; # Server's name, anything is ok
   
       location / {
                   root /home/CloudLGU/src/Front-End/dist;
                   index index.html;
           }
   ```

   The above setting will listen the request from *10.30.201.27:9528* and render the front-end webpages.

   Note that we are still using HTTP here; HTTPS and related certificate configurations are described below.

   Restarting nginx after the configuration is complete encounters error 403. The reason is that SELinux blocks external access.

   Perform the following operations to add Nginx to the whitelist.

   > sudo setenforce 1  
   >
   > semanage permissive -a httpd_t

4.  Generate SSL certificate and set up HTTPS:

   We generate SSL certificate by ourself:
   Create the directory:

   > mkdir /etc/nginx/ssl/manage

   Generate Certificate:

   - Create CA Key

     > openssl genrsa -des3 -out ca.key 2048

   - Create CA root certificate:

     > openssl req -sha256 -new -x509 -days 3650 -key ca.key -out ca.crt

     Then we use the user interface to generate our certificate:

     ```bash
     (base) [root@webtest]# openssl req -sha256 -new -x509 -days 3650 -key ca.key -out ca.crt
     Enter pass phrase for ca.key:
     You are about to be asked to enter information that will be incorporated
     into your certificate request.
     What you are about to enter is what is called a Distinguished Name or a DN.
     There are quite a few fields but you can leave some blank
     For some fields there will be a default value,
     If you enter '.', the field will be left blank.
     -----
     Country Name (2 letter code) [AU]:CN
     State or Province Name (full name) [Some-State]:Guangdong
     Locality Name (eg, city) []:Shenzhen
     Organization Name (eg, company) [Internet Widgits Pty Ltd]:CSC4001
     Organizational Unit Name (eg, section) []:SE
     Common Name (e.g. server FQDN or YOUR name) []:Cloud_LGU
     Email Address []:118010077@link.cuhk.edu.cn
     ```

     Generate secret key:

     > openssl genrsa -des3 -out server.key 2048 

     Generate Certificate Signing Request (CSR):

     ```bash
     openssl req -new \
         -sha256 \
         -key server.key \
         -reqexts SAN \
         -config <(cat /etc/pki/tls/openssl.cnf \
             <(printf "[SAN]\nsubjectAltName=DNS:10.21.44.36\nextendedKeyUsage=serverAuth")) \
         -out server.csr
     ```

     Still, use the user interface to finish the setting:

     ```bash
     Enter pass phrase for server.key:
     You are about to be asked to enter information that will be incorporated
     into your certificate request.
     What you are about to enter is what is called a Distinguished Name or a DN.
     There are quite a few fields but you can leave some blank
     For some fields there will be a default value,
     If you enter '.', the field will be left blank.
     -----
     Country Name (2 letter code) [AU]:CN
     State or Province Name (full name) [Some-State]:Guangdong
     Locality Name (eg, city) []:Shenzhen
     Organization Name (eg, company) [Internet Widgits Pty Ltd]:CSC4001
     Organizational Unit Name (eg, section) []:SE
     Common Name (e.g. server FQDN or YOUR name) []:10.30.201.27
     Email Address []:118010077@link.cuhk.edu.cn
     
     Please enter the following 'extra' attributes
     to be sent with your certificate request
     A challenge password []: 
     An optional company name []:CloudLGU
     ```

     Set up the ssl secret key so that we do not need to reinput those information when we set the Nginx:

     > cp -v server.{key,original}  
     > openssl rsa -in server.original -out server.key  
     > rm -v server.original

     Finally, generate the certificate:

     ```bash
     openssl ca -in server.csr \
             -md sha256 \
             -keyfile ca.key \
             -days 3650 \
         -cert ca.crt \
         -extensions SAN \
         -config <(cat /etc/pki/tls/openssl.cnf \
             <(printf "[SAN]\nsubjectAltName=DNS:10.30.201.27\nextendedKeyUsage=serverAuth")) \
         -out server.crt
     ```

5. Use Nginx to integrate with uWSGI by reverse proxy
   In step 2 and Step 3 we have deployed the front-end and back-end code respectively, except that the front-end is on Nginx and the back-end is on uWSGI. In this step, the backend will also be deployed on port 443 using Nginx's reverse proxy functionality:
   Before modifying nginx.conf, extract Django's static files to a directory so that they can be located later. First, modify Django settings.py to set a directory for collecting static files. Set the method can be imported after reference https://code.ziqiangxuetang.com/django/django-static-files.html Go back to the root directory:

   > python manage.py collectstatic 

   Finally, adjust the configuration in `nginx.conf`:

   ```bash
   user nginx;
   worker_processes auto;
   pid /run/nginx.pid;
   
   
   # Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
   include /usr/share/nginx/modules/*.conf;
   
   events {
       worker_connections 1024;
   }
   
   http {
       log_format main '$remote_addr - $remote_user [$time_local] "$request"'
                       '$status$body_bytes_sent" $http_referer"'
                       '"$http_user_agent" "$http_x_forwarded_for"';
       access_log  /etc/nginx/access.log  main;
       error_log /etc/nginx/error.log debug;
   
       sendfile            on;
       tcp_nopush          on;
       tcp_nodelay         on;
       keepalive_timeout   65;
       types_hash_max_size 2048;
   
       include             /etc/nginx/mime.types;
       default_type        application/octet-stream;
   
       # Load modular configuration files from the /etc/nginx/conf.d directory.
       # See http://nginx.org/en/docs/ngx_core_module.html#include
       # for more information.
       include /etc/nginx/conf.d/*.conf;
       include /etc/nginx/sites-enabled/*;
       ssl_session_timeout 10m;
       ssl_session_cache shared:SSL:10m;
       server {
           listen          80 10.30.201.27;
           server_name     Cloud_LGU;
           rewrite ^/(.*)  https://10.30.201.27/$1 permanent;
           location / {  
           			try_files  $uri/index.html # $ Use uri to check the existance
   					index index.html index.htm  
   		}
       }
   
   
       server {
           listen       443 ssl;
           server_name  10.30.201.27;
           ssl_certificate /etc/nginx/ssl/manage/test/server.crt;
           ssl_certificate_key /etc/nginx/ssl/manage/test/server.key;
           ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
           ssl_ciphers HIGH:!aNULL:!MD5;
           ssl_prefer_server_ciphers on;
   
           location / {
                   add_header Access_Control-Allow-Origin *;
                   add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS, PUT';
                   add_header Access-Control-Allow-Headers 'DNT, X-Mx-ReqToken, Keep-Alive, User-Agent, X-Requested-With, If-Modified-Since, Cache-Control, Content-Type, Authorization';
                #  root /home/talent/background-management-front-end-test/dist;
                   root /home/talent/front_final/background-management-front-end-test/dist;
                   index index.html index.htm;
                   try_files $uri $uri/ /index.html;
           }
   
           error_page 404 /404.html;
           location = /404.html {
   
           }
   
           error_page 500 502 503 504 /50x.html;
   
           location = /50x.html {
           }
   
           location /api {
                   proxy_pass http://10.30.201.28:8080/api;
                   proxy_set_header   Host   $host;
                   proxy_set_header X-Real-IP  $remote_addr;
                   proxy_set_header X-Forwarded-For  $proxy_add_x_forwarded_for;
                   proxy_set_header X-Forwarded-Proto https;
           }
         }
   }
   
   ```

   ### Deal with CORS Problem

   Note that we can use reverse proxy to deal with this problem. Please have a look at the reverse proxy's setting:

   ```bash
           location /django_api {
                   proxy_pass http://10.30.201.28:8080/api;
                   proxy_set_header   Host   $host;
                   proxy_set_header X-Real-IP  $remote_addr;
                   proxy_set_header X-Forwarded-For  $proxy_add_x_forwarded_for;
                   proxy_set_header X-Forwarded-Proto https;
           }
   ```

   

