#
# Conditional build:
%bcond_without	vala		# do not build Vala API

Summary:	GObject contact aggregation library
Summary(pl.UTF-8):	Biblioteka GObject do agregowania kontaktów
Name:		folks
Version:	0.11.3
Release:	3
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/folks/0.11/%{name}-%{version}.tar.xz
# Source0-md5:	1e3a1a78e3f1d5fef6711826ccc5ca8b
URL:		https://live.gnome.org/Folks
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.12
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	evolution-data-server-devel >= 3.13.90
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.40.0
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	intltool >= 0.50.0
BuildRequires:	libgee-devel >= 0.8.4
BuildRequires:	libsocialweb-devel >= 0.25.20
BuildRequires:	libtool >= 2:2
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig >= 1:0.21
BuildRequires:	readline-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	telepathy-glib-devel >= 0.19.9
BuildRequires:	tracker-devel >= 1.0.0
%if %{with vala}
BuildRequires:	vala >= 2:0.22.1
BuildRequires:	vala-evolution-data-server >= 3.13.90
BuildRequires:	vala-libgee >= 0.8.4
BuildRequires:	vala-libsocialweb >= 0.25.20
BuildRequires:	vala-telepathy-glib >= 0.19.9
BuildRequires:	vala-tracker >= 1.0.0
BuildRequires:	vala-zeitgeist >= 0.9.14
#BuildRequires:	valadoc >= 0.3.1
%endif
BuildRequires:	xz
BuildRequires:	zeitgeist-devel >= 0.9.14
Requires:	evolution-data-server-libs >= 3.13.90
Requires:	glib2 >= 1:2.40.0
Requires:	libgee >= 0.8.4
Requires:	telepathy-glib >= 0.19.9
Requires:	tracker-libs >= 1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libfolks is a library that aggregates people from multiple sources
(e.g. Telepathy connection managers and eventually evolution data
server, Facebook, etc.) to create meta-contacts.

%description -l pl.UTF-8
libfolks to biblioteka gromadząca osoby z wielu źródeł (np. zarządców
połączeń Telepathy, serwera danych Evolution, Facebooka itp.), aby
utworzyć metakontakty.

%package devel
Summary:	Development files for folks libraries
Summary(pl.UTF-8):	Pliki programistyczne bibliotek folks
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	evolution-data-server-devel >= 3.13.90
Requires:	glib2-devel >= 1:2.40.0
Requires:	libgee-devel >= 0.8.4
Requires:	libsocialweb-devel >= 0.25.20
Requires:	telepathy-glib-devel >= 0.19.9
Requires:	tracker-devel >= 1.0.0

%description devel
Development files for folks libraries.

%description devel -l pl.UTF-8
Pliki programistyczne bibliotek folks.

%package -n vala-folks
Summary:	folks API for Vala language
Summary(pl.UTF-8):	API folks dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.22.1
Requires:	vala-evolution-data-server >= 3.13.90
Requires:	vala-libgee >= 0.8.4
Requires:	vala-libsocialweb >= 0.25.20
Requires:	vala-telepathy-glib >= 0.19.9
Requires:	vala-tracker >= 1.0.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vala-folks
folks API for Vala language.

%description -n vala-folks -l pl.UTF-8
API folks dla języka Vala.

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
	--disable-fatal-warnings \
	--disable-silent-rules \
	--enable-tracker-backend \
	%{__enable_disable vala vala}

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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/folks-import
%attr(755,root,root) %{_bindir}/folks-inspect
%attr(755,root,root) %{_libdir}/libfolks.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks.so.25
%attr(755,root,root) %{_libdir}/libfolks-dummy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-dummy.so.25
%attr(755,root,root) %{_libdir}/libfolks-eds.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-eds.so.25
%attr(755,root,root) %{_libdir}/libfolks-libsocialweb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-libsocialweb.so.25
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-telepathy.so.25
%attr(755,root,root) %{_libdir}/libfolks-tracker.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-tracker.so.25
%{_libdir}/girepository-1.0/Folks-0.6.typelib
%{_libdir}/girepository-1.0/FolksDummy-0.6.typelib
%{_libdir}/girepository-1.0/FolksEds-0.6.typelib
%{_libdir}/girepository-1.0/FolksLibsocialweb-0.6.typelib
%{_libdir}/girepository-1.0/FolksTelepathy-0.6.typelib
%{_libdir}/girepository-1.0/FolksTracker-0.6.typelib
%dir %{_libdir}/folks
%dir %{_libdir}/folks/43
%dir %{_libdir}/folks/43/backends
%dir %{_libdir}/folks/43/backends/bluez
%attr(755,root,root) %{_libdir}/folks/43/backends/bluez/bluez.so
%dir %{_libdir}/folks/43/backends/dummy
%attr(755,root,root) %{_libdir}/folks/43/backends/dummy/dummy.so
%dir %{_libdir}/folks/43/backends/eds
%attr(755,root,root) %{_libdir}/folks/43/backends/eds/eds.so
%dir %{_libdir}/folks/43/backends/key-file
%attr(755,root,root) %{_libdir}/folks/43/backends/key-file/key-file.so
%dir %{_libdir}/folks/43/backends/libsocialweb
%attr(755,root,root) %{_libdir}/folks/43/backends/libsocialweb/libsocialweb.so
%dir %{_libdir}/folks/43/backends/ofono
%attr(755,root,root) %{_libdir}/folks/43/backends/ofono/ofono.so
%dir %{_libdir}/folks/43/backends/telepathy
%attr(755,root,root) %{_libdir}/folks/43/backends/telepathy/telepathy.so
%dir %{_libdir}/folks/43/backends/tracker
%attr(755,root,root) %{_libdir}/folks/43/backends/tracker/tracker.so
%{_datadir}/GConf/gsettings/folks.convert
%{_datadir}/glib-2.0/schemas/org.freedesktop.folks.gschema.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfolks.so
%attr(755,root,root) %{_libdir}/libfolks-dummy.so
%attr(755,root,root) %{_libdir}/libfolks-eds.so
%attr(755,root,root) %{_libdir}/libfolks-libsocialweb.so
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so
%attr(755,root,root) %{_libdir}/libfolks-tracker.so
%{_datadir}/gir-1.0/Folks-0.6.gir
%{_datadir}/gir-1.0/FolksDummy-0.6.gir
%{_datadir}/gir-1.0/FolksEds-0.6.gir
%{_datadir}/gir-1.0/FolksLibsocialweb-0.6.gir
%{_datadir}/gir-1.0/FolksTelepathy-0.6.gir
%{_datadir}/gir-1.0/FolksTracker-0.6.gir
%{_includedir}/folks
%{_pkgconfigdir}/folks.pc
%{_pkgconfigdir}/folks-dummy.pc
%{_pkgconfigdir}/folks-eds.pc
%{_pkgconfigdir}/folks-libsocialweb.pc
%{_pkgconfigdir}/folks-telepathy.pc
%{_pkgconfigdir}/folks-tracker.pc

%if %{with vala}
%files -n vala-folks
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/folks.deps
%{_datadir}/vala/vapi/folks.vapi
%{_datadir}/vala/vapi/folks-dummy.deps
%{_datadir}/vala/vapi/folks-dummy.vapi
%{_datadir}/vala/vapi/folks-eds.deps
%{_datadir}/vala/vapi/folks-eds.vapi
%{_datadir}/vala/vapi/folks-libsocialweb.deps
%{_datadir}/vala/vapi/folks-libsocialweb.vapi
%{_datadir}/vala/vapi/folks-telepathy.deps
%{_datadir}/vala/vapi/folks-telepathy.vapi
%{_datadir}/vala/vapi/folks-tracker.deps
%{_datadir}/vala/vapi/folks-tracker.vapi
%endif
