#!/bin/bash
#
# Packages Orchestrator as RPM
#

BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source $BASE/get_version_string.sh

#read ver rel < <(get_rpm_version_string)
string=$(get_rpm_version_string)
ver=${string% *}
rel=${string#* }

RPM_DIR=$BASE/build/rpm
mkdir -p $RPM_DIR/BUILD

ORCHESTRATOR_USER=orchestrator

rpmbuild -bb orchestrator.spec \
  --define "_topdir $RPM_DIR" \
  --define "_root $BASE"\
  --define "_project_user $ORCHESTRATOR_USER"\
  --define "_version $ver"\
  --define "_release $rel"
