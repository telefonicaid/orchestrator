# Installation guide

## Service impact
The iotp-orchestrator is a stateless application. This means that its code can be replaced and no migration of data is needed.

## Backup procedure
Due to its stateless behavior, iotp-orchestrator does not require any backup procedure.

## Installation using pdihub

### Prerequisites
 * Internet access
 * Connectivity to http://pdihub.hi.inet
 * [Git](http://git-scm.com/)
 * Python 2.6 (or upper) and pip
 * UNIX platforms but not mandatory
 * WSGI Web server (Apache2/Nginx) but not mandatory

### Installation procedure
Make sure you have installed Python and Git

Download the iotp-orchestrator code and change of directory:
```
git clone git@pdihub.hi.inet:fiware/iotp-orchestrator.git
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
pip install -f requirements.txt
```


Start server in 8084 port using django web server:
```
python manage.py runserver 8084 --settings=settings.custom_dev
```

or using another web server like uWSGI
```
uwsgi --http :8084 --chdir /home/avega/tid/fiware/iotp-orchestrator/src --wsgi-file wsgi.py  --env DJANGO_SETTINGS_MODULE=settings.custom_dev --virtualenv /home/avega/tid/fiware/iotp-orchestrator/env --master --processes 1 --threads 4 --stats 127.0.0.1:8085
```

### Build procedure
Build RPM by running script [package-orchestrator](https://pdihub.hi.inet/fiware/iotp-orchestrator/blob/develop/package-orchestrator.sh)
```
package-orchestrator.sh
```


## Installation by RPM packages
Just install as usual:

```
rpm -iVh iotp-orchestrator.rpm
```

Once installed, configure your environment [settings](https://pdihub.hi.inet/fiware/iotp-orchestrator/blob/develop/src/settings) following [Configuration](CONFIG.md)



## Start the server
RPM install orchestrator as a service controlled by a [daemon](https://pdihub.hi.inet/fiware/iotp-orchestrator/blob/develop/bin/orchestrator-daemon.sh)

```
$ sudo service orchestrator start
```
