Summary:	GObject contact aggregation library
Name:		folks
Version:	0.6.8
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/folks/0.6/%{name}-%{version}.tar.xz
# Source0-md5:	d7552026c4763a3d6e915a2de0fbec3f
URL:		http://telepathy.freedesktop.org/wiki/Folks
BuildRequires:	GConf2-devel >= 2.31.0
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-glib-devel
BuildRequires:	evolution-data-server-devel >= 3.2.0
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.24.0
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libgee-devel < 0.7
BuildRequires:	libsocialweb-devel >= 0.25.20
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig >= 1:0.21
BuildRequires:	readline-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	telepathy-glib-devel >= 0.16.4
BuildRequires:	tracker-devel >= 0.14.0
BuildRequires:	vala >= 2:0.16.0
BuildRequires:	vala-libgee < 0.7
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libfolks is a library that aggregates people from multiple sources
(e.g. Telepathy connection managers and eventually evolution data
server, Facebook, etc.) to create meta-contacts.

%package devel
Summary:	Development files for folks libraries
Summary(pl.UTF-8):	Pliki programistyczne bibliotek folks
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	evolution-data-server-devel >= 3.2.0
Requires:	glib2-devel >= 1:2.24.0
Requires:	libgee-devel < 0.7
Requires:	libsocialweb-devel >= 0.25.20
Requires:	telepathy-glib-devel >= 0.16.4
Requires:	tracker-devel >= 0.14.0

%description devel
Development files for folks libraries.

%description devel -l pl.UTF-8
Pliki programistyczne bibliotek folks.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	--enable-vala

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/folks/*/backends/*/*.la \
	$RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/folks-import
%attr(755,root,root) %{_bindir}/folks-inspect
%attr(755,root,root) %{_libdir}/libfolks.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks.so.25
%attr(755,root,root) %{_libdir}/libfolks-eds.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-eds.so.25
%attr(755,root,root) %{_libdir}/libfolks-libsocialweb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-libsocialweb.so.25
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-telepathy.so.25
%dir %{_libdir}/folks
%dir %{_libdir}/folks/32
%dir %{_libdir}/folks/32/backends
%dir %{_libdir}/folks/32/backends/eds
%attr(755,root,root) %{_libdir}/folks/32/backends/eds/eds.so
%dir %{_libdir}/folks/32/backends/key-file
%attr(755,root,root) %{_libdir}/folks/32/backends/key-file/key-file.so
%dir %{_libdir}/folks/32/backends/libsocialweb
%attr(755,root,root) %{_libdir}/folks/32/backends/libsocialweb/libsocialweb.so
%dir %{_libdir}/folks/32/backends/telepathy
%attr(755,root,root) %{_libdir}/folks/32/backends/telepathy/telepathy.so
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfolks.so
%attr(755,root,root) %{_libdir}/libfolks-eds.so
%attr(755,root,root) %{_libdir}/libfolks-libsocialweb.so
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/folks.deps
%{_datadir}/vala/vapi/folks.vapi
%{_datadir}/vala/vapi/folks-eds.deps
%{_datadir}/vala/vapi/folks-eds.vapi
%{_datadir}/vala/vapi/folks-libsocialweb.deps
%{_datadir}/vala/vapi/folks-libsocialweb.vapi
%{_datadir}/vala/vapi/folks-telepathy.deps
%{_datadir}/vala/vapi/folks-telepathy.vapi
%{_includedir}/folks
%{_pkgconfigdir}/folks.pc
%{_pkgconfigdir}/folks-eds.pc
%{_pkgconfigdir}/folks-libsocialweb.pc
%{_pkgconfigdir}/folks-telepathy.pc
