%define _name xdiskusage

%{?scl:%scl_package %{_name}}
Name:           %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Version:        1.60
Release:        1%{?dist}
Summary:        disk usage visualisation tool
Group:          Scientific support
License:        GPLv2+
URL:            https://xdiskusage.sourceforge.net/
Source0:        https://xdiskusage.sourceforge.net/xdiskusage-%{version}.tgz
BuildRoot:      %{_tmppath}/%{_name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  fltk-devel

%description
xdiskusage is a user-friendly program to show you what is using
up all your disk space. It is based on the design of xdu written by Phillip
C. Dykstra <dykstra at ieee dot org>. Changes have been made so it runs "du"
for you, and can display the free space left on the disk, and produce a
PostScript version of the display.

%prep
%setup -q -n %{_name}-%{version}

%build
%define install_dir %{?scl:%{_scl_root}}/usr
./configure --prefix=%{install_dir}
make xdiskusage

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{install_dir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/xdiskusage
%{_mandir}/man1/xdiskusage.1.gz

%changelog
* Mon Apr  8 2024 alan.iwi@stfc.ac.uk - 1.60
- inital build for Rocky 9 under SCL
