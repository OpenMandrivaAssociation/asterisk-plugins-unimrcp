%define origname asterisk-unimrcp
%define name asterisk-plugins-unimrcp
%define devel %mklibname %{name} -d
%define staticdevel %mklibname -d -s %{name}
%define svnrelease 1815
%define subrel 1

Name: %{name}
Version: 0.%svnrelease
Release: %mkrel 0

Summary: Media Resource Control Protocol Stack
License: Apache
Group: System/Libraries
Url: http://unimrcp.org
BuildRoot: %{_tmppath}/%{name}-%{version}

Source: %{origname}.tar.gz

BuildRequires: asterisk-devel
BuildRequires: libunimrcp-devel libunimrcp-deps-devel
BuildRequires: expat-devel

Requires: asterisk
Requires: libunimrcp
Requires: libunimrcp-deps

%description
Media Resource Control Protocol (MRCP) allows to control media processing
resources over the network using distributed client/server architecture.
Media processing resources include:
- Speech Synthesizer (TTS)
- Speech Recognizer (ASR)
- Speaker Verifier (SV)
- Speech Recorder (SR)

%package -n %{devel}
Summary: Media Resource Control Protocol Stack development
Group: Development/C
Requires: %{name} = %version-%release

%package -n %{staticdevel}
Summary: Media Resource Control Protocol Stack development static
Group: Development/C
Requires: %{name} = %version-%release

%description -n %{devel}
Development files for asterisk-plugins-unimrcp

%description -n %{staticdevel}
Static development files for asterisk-plugins-unimrcp

%prep
%setup -q -n %{origname}

%build
[ ! -x ./bootstrap ] || ./bootstrap
perl -pi -w -e 's/lib\/pkgconfig/pkgconfig/g' configure
perl -pi -w -e 's/UNIMRCP_DIR_LOCATION \"\$unimrcp_dir\"/UNIMRCP_DIR_LOCATION \"\/etc\/unimrcp\"/g' configure
perl -pi -w -e 's/\$\(asterisk_conf_dir\)/\$\(DESTDIR\)\$\(asterisk_conf_dir\)/g' Makefile.in

%configure2_5x \
    --sysconfdir=%{_sysconfdir}/asterisk \
    --with-unimrcp=%{_libdir} \
    --with-asterisk-conf=%{_sysconfdir}/asterisk \
    --prefix=%{_libdir}/asterisk/modules

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d -m1775 %{buildroot}%{_sysconfdir}/asterisk
%makeinstall_std

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/asterisk/modules/*.so
%config(noreplace) %{_sysconfdir}/asterisk/*.conf

%files -n %{devel}
%defattr(-,root,root)
%{_libdir}/asterisk/modules/*.la

%files -n %{staticdevel}
%defattr(-,root,root)
%{_libdir}/asterisk/modules/*.a
