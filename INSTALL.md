# Installation guide

## Service impact
The iotp-orchestrator is a stateless application. This means that its code can be replaced and no migration of data is needed.

## Backup procedure
Due to its stateless behavior, iotp-orchestrator does not require any backup procedure.

## Installation using github

### Prerequisites
 * Internet access
 * Connectivity to http://github.com
 * [Git](http://git-scm.com/)
 * Python 2.6 (or upper) and pip
 * C and C++ compilation platform: gcc, g++, make and python headers
 * UNIX platforms but not mandatory
 * WSGI Web server (Apache2/Nginx) but not mandatory

### Installation procedure
Make sure you have installed Python and Git

Download the iotp-orchestrator code and change of directory:
```
git clone git@github.com:telefonicaid/orchestrator.git
git checkout BRANCH
cd iotp-orchestrator
```

Define some variables:
```
export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=$(pwd):$(pwd)/src:/usr/local/lib/python2.7/site-packages
```

Create a virtual env
```
virtualenv env
source env/bin/activate
cd src
```

Then install all dependencies by running:
```
pip install -r requirements.txt
```


Start server in 8084 port using django web server:
```
python manage.py runserver 8084 --settings=settings.dev
```

or using another web server like uWSGI
```
uwsgi --http :8084 --chdir /home/user/iotp-orchestrator/src --wsgi-file wsgi.py  --env DJANGO_SETTINGS_MODULE=settings.dev --virtualenv /home/user/iotp-orchestrator/env --master --processes 1 --threads 4 --stats 127.0.0.1:8085
```

### Build procedure
Build RPM by running script [package-orchestrator](https://github.com/telefonicaid/orchestrator/blob/master/package-orchestrator.sh)
```
package-orchestrator.sh
```


## Installation by RPM packages
Just install as usual:

```
rpm -iVh iotp-orchestrator.rpm
```

Once installed, configure your environment [settings](https://github.com/telefonicaid/orchestrator/blob/master/src/settings) following [Configuration](CONFIG.md)



## Start the server
RPM install orchestrator as a service controlled by a [daemon](https://github.com/telefonicaid/orchestrator/blob/master/bin/orchestrator-daemon.sh)

```
$ sudo service orchestrator start
```

## Make a simple test:
```
curl -X GET http://127.0.0.1:8084/v1.0/service -H "Content-Type: application/json" -d '{ "DOMAIN_NAME": "admin_domain", "SERVICE_ADMIN_USER": "cloud_admin", "SERVICE_ADMIN_PASSWORD":"password"}'
```
