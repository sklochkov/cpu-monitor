%define _builddir	.
%define _sourcedir	.
%define _specdir	.
%define _rpmdir		.

Name:		cpu-monitor
Version:	0.1
Release:	4%{dist}

Summary:	CPU usage monitor
License:	MIT
Group:		System Environment/Libraries
Distribution:	Red Hat Enterprise Linux

BuildArch:	noarch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires: dstat

%description
IQBuzz monitoring scripts


%prep


%build


%install
%{__rm} -rf %{buildroot}
install -d -m755 %{buildroot}/etc/init.d
install -d -m755 %{buildroot}/usr/local/bin
install -m755 cpustat.py %{buildroot}/usr/local/bin/cpustat.py
install -m755 cpustat.init %{buildroot}/etc/init.d/cpustat

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq 1 ] ; then
	chkconfig --add cpustat
	chkconfig cpustat on
	/etc/init.d/cpustat start
elif [ $1 -eq 2 ] ; then
	/etc/init.d/cpustat restart
fi

%preun
if [ $1 -eq 0 ] ; then
	chkconfig cpustat off
	chkconfig --del cpustat
	/etc/init.d/cpustat stop
fi

%files
%defattr(-,root,root)
%attr(0755,root,root) /usr/local/bin/cpustat.py
%attr(0755,root,root) /etc/init.d/cpustat


