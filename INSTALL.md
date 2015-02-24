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
 * Python and pip
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

Create a virtual env
```
virtualenv env
source env/bin/activate
cd src
```

Then install all dependencies by running:
```
pip install -f requirements
```

Start server in 8084 port
```
python manage.py runserver 8084 --settings=settings.custom_dev
```

### Build procedure
Build RPM by running script
```
package-orchestrator.sh
```


## Installation by RPM packages
Just install as usual:

```
rpm -iVh iotp-orchestrator.rpm
```

Once installed, configure your environment settings , like
keystone and keypass endpoints.

Start the server

```
$ sudo service orchestrator start
```
