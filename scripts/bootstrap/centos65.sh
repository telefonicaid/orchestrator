#
# Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U
#
# This file is part of Orchestrator.
#
# Orchestrator is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Orchestrator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Orion Context Broker. If not, see http://www.gnu.org/licenses/.
#
# For those usages not covered by this license please contact with
# iot_support at tid dot es
#
# Author: IoT Platform Team
#

# Setting up EPEL Repo
wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
sudo rpm -ivh epel-release-6-8.noarch.rpm

sudo yum -y install rpm-build
sudo yum -y install python git python-pip python-devel python-virtualenv gcc ssh

mkdir updates
cd updates

GIT_SSL_NO_VERIFY=true git clone https://github.com/telefonicaid/orchestrator.git iotp-orchestrator
cd iotp-orchestrator
#git checkcout master
git checkout bug/rpm_install_dir_permissions
sudo pip install -r requirements.txt
sudo pip install repoze.lru

bash ./package-orchestrator.sh
find . -name "*.rpm" -exec sudo rpm -Uvh {} \;

service orchestrator restart
