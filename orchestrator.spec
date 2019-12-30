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
%define python_lib /var/env-orchestrator/lib/python2.6/site-packages
%if 0%{?with_python27}
%define python_lib /var/env-orchestrator/lib/python2.7/site-packages
%define __python /usr/bin/python2.7
%endif # if with_python27

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


%files
%{python_lib}/iotp-orchestrator
%defattr(755,%{_project_user},%{_project_user},755)
%config /etc/init.d/%{_service_name}
%config /etc/default/%{_service_name}-daemon
%{_install_dir}


%pre
echo "[INFO] Creating %{_project_user} user"
grep ^%{_project_user}: /etc/passwd
RET_VAL=$?
if [ "$RET_VAL" != "0" ]; then
      mkdir -p %{_install_dir}
      /usr/sbin/useradd -s "/bin/bash" -d %{_install_dir} %{_project_user}
      RET_VAL=$?
      if [ "$RET_VAL" != "0" ]; then
         echo "[ERROR] Unable create %{_project_user} user" \
         exit $RET_VAL
      fi
else
      ls %{_install_dir}/settings/dev.py
      RET_VAL=$?

      if [ "$RET_VAL" == "0" ]; then
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

    if [ "$RET_VAL" == "0" ]; then
        mv /tmp/dev.py %{_install_dir}/settings/dev.py
    fi

    echo "[INFO] Link to /opt"
    ln -sf %{_install_dir} %{_orchestrator_link_dir}
    ln -sf %{_orchestrator_link_dir}/orchestrator/commands %{_orchestrator_link_dir}/bin

    echo "[INFO] Fix version"
    sed -i -e 's/ORC_version/%{_version}/g' %{_install_dir}/settings/common.py
    sed -i -e 's/\${project.version}/%{_version}/g' %{_install_dir}/orchestrator/core/banner.txt

    echo "[INFO] restart service %{_service_name}"
    service %{_service_name} restart &> /dev/null
    
echo "Done"


%preun
echo "[INFO] stoping service %{_service_name}"
service %{_service_name} stop &> /dev/null

if [ $1 == 0 ]; then

  echo "[INFO] Removing application log files"
  # Log
  [ -d %{_orchestrator_log_dir} ] && rm -rfv %{_orchestrator_log_dir}

  echo "[INFO] Removing application files"
  # Installed files
  [ -d %{_install_dir} ] && rm -rfv %{_install_dir}

  echo "[INFO] Removing application user"
  userdel -fr %{_project_user}

  echo "[INFO] Removing application service"
  chkconfig --del %{_service_name}
  rm -Rf /etc/init.d/%{_service_name}

  echo "[INFO] Removing orchestrator link"
  rm %{_orchestrator_link_dir}

  echo "Done"
fi

