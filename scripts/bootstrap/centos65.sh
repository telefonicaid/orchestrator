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

sudo mkdir ~/.ssh

# Allow connecting pdihub.hi.inet
sudo echo "Host      pdihub.hi.inet
  Hostname        pdihub.hi.inet
  StrictHostKeyChecking no
  IdentityFile    ~/.ssh/id_rsa_pdihub" > ~/.ssh/config

sudo   echo "-----BEGIN DSA PRIVATE KEY-----
MIIBvAIBAAKBgQDod9JbsS3PaK60T6cDVnk4eT04CMRjyoA/CGT05Uh+InpQpB/a
1j+E9kUztZfyNg3B4xozWXu1zUNsE/Hh6KXHff4ZJfbj4owcoW2dzcsSHGkPn61z
GhBZa5PD3PlIcknBsAIKXjUUVL3f+GaWVTQBIm3moAal3qxuemxFz+hr+QIVAKCV
mfVNCs2laMcXHvtXcplqokHrAoGBAIHcci/y0qIog5jMN5RWYpwajak1On55efeX
ZMWuJeQLGN3P4lYdaqmJH3a6a4wJTRq4IUEQMk141iYneXFmdrzpShUWLDTbtMeE
pgsE1wVnjNs5F+AQfhLn+3UJWsPaUYuUN8/5YiS4CmraFSL3qPYOw1J7+OwRLUQG
0b3RMn0JAoGBANmqUtWDqbM0wzzjgXmeN7RyIVt/nvtjVB3hGrbKfXAQYcMp34B/
lbcvcthtKHcPR5+mOljcqJQhYTVhF4IEcJJeDFPb/A+p+yvqJnvm+mQas76ne+aH
f0l0BxiwY8toMnlOjED3aiXx99kJjt3g5dPH9PMbla1Nblh5gp0mIWl9AhRyXGXC
6MTy0yRRjba3BDiwf4G8JQ==
-----END DSA PRIVATE KEY-----" > ~/.ssh/id_rsa_pdihub

sudo  chmod 700 ~/.ssh/id_rsa_pdihub

mkdir updates
cd updates

#GIT_SSL_NO_VERIFY=true git clone https://github.com/telefonicaid/orchestrator.git iotp-orchestrator
GIT_SSL_NO_VERIFY=true git clone https://visitor:visitor@pdihub.hi.inet/fiware/iotp-orchestrator.git iotp-orchestrator 
cd iotp-orchestrator
#git checkcout master
git checkout bug/rpm_install_dir_permissions
sudo pip install -r requirements.txt
sudo pip install repoze.lru

bash ./package-orchestrator.sh
find . -name "*.rpm" -exec sudo rpm -Uvh {} \;

service orchestrator restart
