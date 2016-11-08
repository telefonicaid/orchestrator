#!/bin/bash
#
# Packages Orchestrator as RPM
#

BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source $BASE/get_version_string.sh

#read ver rel < <(get_rpm_version_string)
string=$(get_rpm_version_string)
VERSION_VALUE=${string% *}
RELEASE_VALUE=${string#* }

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
done


RPM_DIR=$BASE/build/rpm
mkdir -p $RPM_DIR/BUILD

ORCHESTRATOR_USER=orchestrator

rpmbuild -bb orchestrator.spec \
  --define "_topdir $RPM_DIR" \
  --define "_root $BASE"\
  --define "_project_user $ORCHESTRATOR_USER"\
  --define "_version $VERSION_VALUE"\
  --define "_release $RELEASE_VALUE"
