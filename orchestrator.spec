%define timestamp %(date +"%Y%m%d%H%M%S")
Name: iotp-orchestrator
Version: %{_version}
Release: %{_release}
Summary: IoT Platform Orchestrator
License: AGPLv3
Distribution: noarch
Vendor: Telefonica I+D
Group: Applications/System
Packager: Telefonica I+D
Requires: python
Requires(post): /sbin/chkconfig, /usr/sbin/useradd
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
autoprov: no
autoreq: no
Prefix: /opt
BuildArch: noarch

%define _target_os Linux
%define python_lib /var/env-orchestrator/lib/python3.6/site-packages
%define __python /usr/bin/python3.6

%description
IoT Platform Orchestrator

# System folders
%define _srcdir $RPM_BUILD_ROOT
%define _service_name orchestrator
%define _install_dir %{python_lib}/iotp-orchestrator
%define _orchestrator_log_dir /var/log/orchestrator
%define _orchestrator_link_dir /opt/orchestrator

# RPM Building folder
%define _build_root_project %{buildroot}%{_install_dir}


%install
mkdir -p $RPM_BUILD_ROOT/%{python_lib}
cp -a %{_root}/src/ $RPM_BUILD_ROOT/%{python_lib}/iotp-orchestrator
find $RPM_BUILD_ROOT/%{python_lib}/iotp-orchestrator -name "*.pyc" -delete

mkdir -p $RPM_BUILD_ROOT/etc/init.d
cp -a %{_root}/bin/orchestrator-daemon.sh $RPM_BUILD_ROOT/etc/init.d/orchestrator
mkdir -p $RPM_BUILD_ROOT/etc/default
cp -a %{_root}/bin/orchestrator-daemon $RPM_BUILD_ROOT/etc/default/orchestrator-daemon


%pre
echo "[INFO] Creating %{_project_user} user"
grep ^%{_project_user}: /etc/passwd
RET_VAL=$?
if [ "$RET_VAL" != "0" ]
then
  mkdir -p %{_install_dir}
  /usr/sbin/groupadd -f orchestrator
  /usr/sbin/useradd -s "/bin/bash" -g orchestrator %{_project_user}
  RET_VAL=$?
  if [ "$RET_VAL" != "0" ]
  then
    echo "[ERROR] Unable create %{_project_user} user"
    exit $RET_VAL
  fi
else
  ls %{_install_dir}/settings/dev.py
  RET_VAL=$?

  if [ "$RET_VAL" == "0" ]
  then
    cp %{_install_dir}/settings/dev.py /tmp
  fi
fi


%post
echo "[INFO] Configuring application"

echo "[INFO] Creating log directory"
mkdir -p %{_orchestrator_log_dir}
chown -R %{_project_user}:%{_project_user} %{_orchestrator_log_dir}
chmod g+s %{_orchestrator_log_dir}
setfacl -d -m g::rwx %{_orchestrator_log_dir}
setfacl -d -m o::rx %{_orchestrator_log_dir}

echo "[INFO] Configuring application service"
cd /etc/init.d
chkconfig --add %{_service_name}

ls /tmp/dev.py
RET_VAL=$?

if [ "$RET_VAL" == "0" ]
then
  mv /tmp/dev.py %{_install_dir}/settings/dev.py
fi

echo "[INFO] Link to /opt"
# Remove bad created links
rm -f %{_install_dir}/iotp-orchestrator
rm -f %{_orchestrator_link_dir}/orchestrator/commands/commands
# Create good links
ln -sfn %{_install_dir} %{_orchestrator_link_dir}
ln -sfn %{_orchestrator_link_dir}/orchestrator/commands %{_orchestrator_link_dir}/bin

echo "[INFO] Fix version"
sed -i -e 's/ORC_version/%{_version}/g' %{_install_dir}/settings/common.py
sed -i -e 's/\${project.version}/%{_version}/g' %{_install_dir}/orchestrator/core/banner.txt

echo "[INFO] restart service %{_service_name}"
service %{_service_name} restart &> /dev/null
    
echo "Done"


%preun
echo "[INFO] stoping service %{_service_name}"
service %{_service_name} stop &> /dev/null

if [ $1 == 0 ]
then
  echo "[INFO] Removing application log files"
  # Log
  [ -d %{_orchestrator_log_dir} ] && rm -rf %{_orchestrator_log_dir}

  echo "[INFO] Removing application files"
  # Installed files
  [ -d %{_install_dir} ] && rm -rf %{_install_dir}

  echo "[INFO] Removing application user"
  userdel -fr %{_project_user}

  echo "[INFO] Removing application service"
  chkconfig --del %{_service_name}
  rm -Rf /etc/init.d/%{_service_name}

  echo "[INFO] Removing orchestrator link"
  rm -f %{_orchestrator_link_dir}

  echo "Done"
fi

%files
%defattr(755,%{_project_user},%{_project_user},755)
%attr(755,root,root) /etc/init.d/%{_service_name}
%attr(644,root,root) /etc/default/%{_service_name}-daemon
%config /etc/init.d/%{_service_name}
%config /etc/default/%{_service_name}-daemon
%{python_lib}/iotp-orchestrator

