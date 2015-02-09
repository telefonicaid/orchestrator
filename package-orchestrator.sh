#!/bin/bash
#
# Packages Orchestrator as RPM
#

BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

RPM_DIR=$BASE/build/rpm
mkdir -p $RPM_DIR/BUILD

ORCHESTRATOR_USER=orchestrator

rpmbuild -bb orchestrator.spec \
  --define "_topdir $RPM_DIR" \
  --define "_root $BASE"\
  --define "_project_user $ORCHESTRATOR_USER"

