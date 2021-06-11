#!/usr/bin/env bash
#
# Packages Orchestrator as RPM
#
#
# Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U
#
# This file is part of IoT orchestrator
#
# IoT orchestrator is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# IoT orchestrator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with IoT orchestrator. If not, see http://www.gnu.org/licenses/.
#
# For those usages not covered by this license please contact with
# iot_support at tid dot es
#
# Author: IoT team
#


BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source $BASE/get_version_string.sh

#read ver rel < <(get_rpm_version_string)
string=$(get_rpm_version_string)
VERSION_VALUE=${string% *}
RELEASE_VALUE=${string#* }
PYTHON27_VALUE=0
PYTHON3_VALUE=0

args=("$@")
ELEMENTS=${#args[@]}

for (( i=0;i<$ELEMENTS;i++)); do
    arg=${args[${i}]}
    if [ "$arg" == "--with-version" ]; then
        VERSION_VALUE=${args[${i}+1]}
    fi
    if [ "$arg" == "--with-release" ]; then
        RELEASE_VALUE=${args[${i}+1]}
    fi
    if [ "$arg" == "--with-python27" ]; then
        PYTHON27_VALUE=1
    fi
    if [ "$arg" == "--with-python3" ]; then
        PYTHON3_VALUE=1
    fi
done


RPM_DIR=$BASE/build/rpm
mkdir -p $RPM_DIR/BUILD

ORCHESTRATOR_USER=orchestrator

rpmbuild -bb orchestrator.spec \
  --define "_topdir $RPM_DIR" \
  --define "_root $BASE"\
  --define "_project_user $ORCHESTRATOR_USER"\
  --define "with_python27 $PYTHON27_VALUE"\
  --define "with_python3 $PYTHON3_VALUE"\
  --define "_version $VERSION_VALUE"\
  --define "_release $RELEASE_VALUE"
