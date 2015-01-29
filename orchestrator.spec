%define timestamp %(date +"%Y%m%d%H%M%S")
Name: iotp-orchestrator
Version: 0.1.0
Release: %{timestamp}
Summary: IoT Platform Orchestrator 
License: Copyright 2015 Telefonica Investigación y Desarrollo, S.A.U
Distribution: noarch
Vendor: Telefonica I+D
Group: Applications/System
Packager: Telefonica I+D
Requires: Python
autoprov: no
autoreq: no
Prefix: /opt
BuildArch: noarch

%define _target_os Linux
%define python_lib /usr/lib/python2.6/site-packages

%description
IoT Platform Orchestrator


%install
mkdir -p $RPM_BUILD_ROOT/%{python_lib}
cp -a %{_root}/src/ $RPM_BUILD_ROOT/%{python_lib}/iotp-orchestrator
find $RPM_BUILD_ROOT/%{python_lib}/iotp-orchestrator -name "*.pyc" -delete

%files
"/usr/lib/python2.6/site-packages/iotp-orchestrator"

%post
echo "Orchestrator installed successfully."

%preun
if [ $1 -gt 0 ] ; then
  # upgrading: no remove extension
  exit 0
fi

