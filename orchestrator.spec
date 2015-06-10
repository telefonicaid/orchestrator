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

%description
IoT Platform Orchestrator

# System folders
%define _srcdir $RPM_BUILD_ROOT
%define _service_name orchestrator
%define _install_dir %{python_lib}/iotp-orchestrator
%define _orchestrator_log_dir /var/log/orchestrator

# RPM Building folder
%define _build_root_project %{buildroot}%{_install_dir}

# %prep
# echo "[INFO] Preparing installation"
# # Create rpm/BUILDROOT folder
# rm -Rf $RPM_BUILD_ROOT && mkdir -p $RPM_BUILD_ROOT
# [ -d %{_build_root_project} ] || mkdir -p %{_build_root_project}
# # Copy src files
# cp -R %{_srcdir}/bin \
#       %{_srcdir}/LICENSE \
#       %{_build_root_project}

# cp -R %{_topdir}/SOURCES/etc %{buildroot}

%install
mkdir -p $RPM_BUILD_ROOT/%{python_lib}
cp -a %{_root}/src/ $RPM_BUILD_ROOT/%{python_lib}/iotp-orchestrator
find $RPM_BUILD_ROOT/%{python_lib}/iotp-orchestrator -name "*.pyc" -delete

mkdir -p $RPM_BUILD_ROOT/etc/init.d
cp -a %{_root}/bin/orchestrator-daemon.sh $RPM_BUILD_ROOT/etc/init.d/orchestrator

%files
"/var/env-orchestrator/lib/python2.6/site-packages/iotp-orchestrator"
%defattr(755,%{_project_user},%{_project_user},755)
%config /etc/init.d/%{_service_name}
%{_install_dir}

# -------------------------------------------------------------------------------------------- #
# pre-install section:
# -------------------------------------------------------------------------------------------- #
%pre
echo "[INFO] Creating %{_project_user} user"
grep ^%{_project_user}: /etc/passwd
RET_VAL=$?
if [ "$RET_VAL" != "0" ]; then
      chown -R %{_project_user}:%{_project_user} %{_install_dir}
      /usr/sbin/useradd -s "/bin/bash" -d %{_install_dir} %{_project_user}
      RET_VAL=$?
      if [ "$RET_VAL" != "0" ]; then
         echo "[ERROR] Unable create %{_project_user} user" \
         exit $RET_VAL
      fi
fi

# -------------------------------------------------------------------------------------------- #
# post-install section:
# -------------------------------------------------------------------------------------------- #
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
echo "Done"


%preun
echo "[INFO] stoping service %{_service_name}"
service %{_service_name} stop &> /dev/null

# if [ $1 -gt 0 ] ; then
#   # upgrading: no remove extension
#   exit 0
# fi

