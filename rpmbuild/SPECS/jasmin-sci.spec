%{!?scl:%global scl jasmin-sci}
%scl_package %scl

Summary: Package that installs %scl
Name: %scl_name
Version: 2.2
Release: 3%{?dist}
BuildArch: noarch
License: GPLv2+
BuildRequires: scl-utils-build
#Obsoletes: ceda-sci
#Obsoletes: jasmin-sci-nccmp

Requires: %{scl_prefix}runtime == %{version}-%{release}

# Requires from Rocky / EPEL base (non SCL packages)

Requires: atlas
Requires: atlas-devel
Requires: ddd
Requires: emacs
Requires: gcc-gfortran
Requires: geany
Requires: geos-devel
Requires: git-lfs
Requires: gitk
Requires: glibc-static
Requires: gnuplot
Requires: gpsbabel
Requires: GraphicsMagick-c++
Requires: grass
Requires: grass-devel
Requires: gv
Requires: htop
Requires: ImageMagick-c++-devel
Requires: ksh
Requires: less
Requires: libRmath
Requires: libRmath-devel
Requires: libXaw-devel
Requires: libcurl-devel
Requires: libuuid-devel
Requires: mercurial
Requires: mesa-dri-drivers
Requires: nano
Requires: ncview
Requires: nedit
Requires: netcdf-cxx
Requires: netcdf-cxx-devel
Requires: netcdf-devel
Requires: netcdf-fortran-devel
Requires: netpbm-devel
Requires: octave
Requires: octave-devel
Requires: octave-netcdf
Requires: openssl-devel
Requires: p7zip
Requires: patch
Requires: perl-Image-ExifTool
Requires: perl-core
Requires: perl-devel
Requires: postgresql-devel
Requires: proj
Requires: proj-devel
Requires: qt5-devel
Requires: screen
Requires: singularity-ce
Requires: sqlite-devel
Requires: subversion
Requires: subversion-devel
Requires: subversion-tools
Requires: tcl-devel
Requires: tcsh
Requires: texlive-dvipng texlive-pdftex texlive-type1cm texlive-latex-bin texlive-cm-super texlive-cm texlive-epstopdf
Requires: tk-devel
Requires: tmpwatch
Requires: tmux
Requires: tree
Requires: udunits2-devel
Requires: uuid
Requires: uuid-devel
Requires: vim-enhanced
Requires: vim-X11
Requires: wgrib
Requires: wxGTK-devel
Requires: xfce4-terminal
Requires: xorg-x11-util-macros
Requires: xpdf
Requires: xterm

# Requires from local JASMIN builds (SCL packages)

# when updating this list, also update the build_all.sh script at the
# top level of the repo with the names of the spec files required to
# build these
#
Requires: %{scl_prefix}mo_unpack >= 2.0.1-3
Requires: %{scl_prefix}xconv >= 1.94-2
Requires: %{scl_prefix}leafpad >= 0.8.19-1
Requires: %{scl_prefix}tkdiff >= 5.6-1
Requires: %{scl_prefix}ferret >= 7.6.0-1
Requires: %{scl_prefix}ferret-datasets >= 7.6-1
Requires: %{scl_prefix}hdfeos2 >= 3.0-2
Requires: %{scl_prefix}mtk >= 1.5.1-1
Requires: %{scl_prefix}mtk-devel >= 1.5.1-1
Requires: %{scl_prefix}libemos >= 4.5.9-2
Requires: %{scl_prefix}libdrs >= 3.1.2-2
Requires: %{scl_prefix}libcrayutil >= 20121128-3
Requires: %{scl_prefix}umutil >= 20130102-5
Requires: %{scl_prefix}umutil-lib >= 20130102-5
Requires: %{scl_prefix}filesystem >= 1.1-5
Requires: %{scl_prefix}minio >= 20211007.041958-2
Requires: %{scl_prefix}saga >= 9.3.2-1
Requires: %{scl_prefix}xdiskusage >= 1.60-1
Requires: %{scl_prefix}eccodes2_27 >= 2.27.1-2

%if %{?_with_closed_source:1}%{?!_with_closed_source:0}
Requires: %{scl_prefix}withgroups >= 1.1-2
%endif


%description
The %scl Software Collection is a collection of software packages which provide a scientific
software environment.  It is intended to be used in combination with the Jaspy conda environment,
and these RPMs will provide additional packages to supplement Jaspy.  Installing this 
meta-package will cause the installation of:

 1) a number of software packages built for JASMIN, which will install under /opt/rh/jasmin-sci
    and which will require the following setup command before running them:

        source /opt/rh/jasmin-sci/enable

 2) a number of software packages from standard repositories, which will install under 
    ordinary system paths

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils
#Requires: %{scl_name} == %{version}-%{release}
#Obsoletes: ceda-sci-runtime

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: %{scl_name}-runtime == %{version}-%{release}

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%prep
%setup -c -T

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_scl_scripts}/root
cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}:\$PATH

if [ -z \$LD_LIBRARY_PATH ]
then
   export LD_LIBRARY_PATH=%{_libdir}
else
   export LD_LIBRARY_PATH=%{_libdir}:\$LD_LIBRARY_PATH
fi

if [ -z \$MANPATH ]
then
   export MANPATH=%{_mandir}
else
   export MANPATH=%{_mandir}:\$MANPATH
fi

. %{_scl_root}/etc/profile
EOF

mkdir -p %{buildroot}%{_scl_root}/etc
cat >> %{buildroot}%{_scl_root}/etc/profile <<EOF
for i in %{_scl_root}/etc/profile.d/*.sh ; do
    if [ -r "\$i" ]; then
       . "\$i" >/dev/null
    fi
done
EOF

cat >> %{buildroot}%{_scl_root}/etc/csh.login <<EOF
if ( -d %{_scl_root}/etc/profile.d ) then
    set nonomatch
    foreach i ( %{_scl_root}/etc/profile.d/*.csh )
        if ( -r "\$i" ) then
            source "\$i" >& /dev/null
        endif
    end
    unset i nonomatch
endif
EOF


%scl_install

%files

%files runtime
%scl_files
%{_scl_root}/etc/profile
%{_scl_root}/etc/csh.login

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config


%changelog
# changelog may be incomplete - see history in git

* Mon Dec 16 2019 Builder <builder@builder.ceda.ac.uk> - 1.3-1
- -firefox again

* Fri Dec 13 2019 Builder <builder@builder.ceda.ac.uk> - 1.2-1
- +firefox

* Fri Nov  1 2019 Builder <builder@builder.ceda.ac.uk> - 1-5
- direct dependency on exact version of runtime

* Thu Sep 26 2019 Alan Iwi <alan.iwi@stfc.ac.uk> 1-1
- Initial package


