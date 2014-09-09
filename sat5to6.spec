%global _hardened_build 1

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name: sat5to6
Version: 1.0.0
Release: 1%{?dist}
Summary: Migration tool for moving from Satellite 5 to Satellite 6
Group:   System Environment/Base
License: GPLv2
URL:     https://www.candlepinproject.org

Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: subscription-manager >= 0:1.8.22
Requires: python-rhsm >= 0:1.13.2
Requires: rhnlib

# Since the migration data package is not in Fedora, we can only require it
# on RHEL.
%if 0%{?rhel}
Requires: subscription-manager-migration-data
%endif

BuildRequires: python-devel
BuildRequires: python-setuptools
BuildRequires: gettext

%description
%{summary}.

%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --root %{buildroot}

# fix timestamps on our byte compiled files so they match across arches
find %{buildroot} -name \*.py -exec touch -r %{SOURCE0} '{}' \;
%find_lang %{name}

%{__install} -d %{buildroot}%{_var}/log/rhsm

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc LICENSE
%attr(755,root,root) %dir %{_var}/log/rhsm
%attr(755,root,root) %{_sbindir}/sat5to6
%{python2_sitelib}/%{name}/*
%{python2_sitelib}/%{name}-*.egg-info

%changelog
* Sun Sep 07 2014 Alex Wood <awood@redhat.com> 1.13.1-1
- Initial packaging
