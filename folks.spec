#
# Conditional build:
%bcond_with	apidocs		# API documentation (currently built as devhelp part, not gtk-doc?)
%bcond_without	vala		# do not build Vala API

Summary:	GObject contact aggregation library
Summary(pl.UTF-8):	Biblioteka GObject do agregowania kontaktów
Name:		folks
Version:	0.13.1
Release:	2
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/folks/0.13/%{name}-%{version}.tar.xz
# Source0-md5:	0038ec90db52ed7a82c93d98e227b078
Patch0:		%{name}-meson.patch
Patch1:		%{name}-module.patch
URL:		https://wiki.gnome.org/Projects/Folks
BuildRequires:	dbus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	evolution-data-server-devel >= 3.13.2
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	libgee-devel >= 0.8.4
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	meson >= 0.49
BuildRequires:	ncurses-devel
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.21
BuildRequires:	python3 >= 1:3.2
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	readline-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	telepathy-glib-devel >= 0.19.9
BuildRequires:	tracker-devel >= 2.0
%if %{with vala}
BuildRequires:	vala >= 2:0.22.1
BuildRequires:	vala-evolution-data-server >= 3.33.2
BuildRequires:	vala-libgee >= 0.8.4
BuildRequires:	vala-telepathy-glib >= 0.19.9
BuildRequires:	vala-tracker >= 2.0
BuildRequires:	vala-zeitgeist >= 0.9.14
%endif
%{?with_apidocs:BuildRequires:	valadoc >= 0.3.1}
BuildRequires:	xz
BuildRequires:	zeitgeist-devel >= 0.9.14
Requires:	evolution-data-server-libs >= 3.33.2
Requires:	glib2 >= 1:2.44
Requires:	libgee >= 0.8.4
Requires:	telepathy-glib >= 0.19.9
Requires:	tracker-libs >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abiver	45

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
Requires:	evolution-data-server-devel >= 3.33.2
Requires:	glib2-devel >= 1:2.44
Requires:	libgee-devel >= 0.8.4
Requires:	telepathy-glib-devel >= 0.19.9
Requires:	tracker-devel >= 2.0

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
Requires:	vala-evolution-data-server >= 3.33.2
Requires:	vala-libgee >= 0.8.4
Requires:	vala-telepathy-glib >= 0.19.9
Requires:	vala-tracker >= 2.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vala-folks
folks API for Vala language.

%description -n vala-folks -l pl.UTF-8
API folks dla języka Vala.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%meson build \
	%{?with_apidocs:-Ddocs=true} \
	-Dtracker_backend=true \
	-Dzeitgeist=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS MAINTAINERS NEWS README.md
%attr(755,root,root) %{_bindir}/folks-import
%attr(755,root,root) %{_bindir}/folks-inspect
%attr(755,root,root) %{_libdir}/libfolks.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks.so.25
%attr(755,root,root) %{_libdir}/libfolks-dummy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-dummy.so.25
%attr(755,root,root) %{_libdir}/libfolks-eds.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-eds.so.25
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-telepathy.so.25
%attr(755,root,root) %{_libdir}/libfolks-tracker.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-tracker.so.25
%{_libdir}/girepository-1.0/Folks-0.6.typelib
%{_libdir}/girepository-1.0/FolksDummy-0.6.typelib
%{_libdir}/girepository-1.0/FolksEds-0.6.typelib
%{_libdir}/girepository-1.0/FolksTelepathy-0.6.typelib
%{_libdir}/girepository-1.0/FolksTracker-0.6.typelib
%dir %{_libdir}/folks
%dir %{_libdir}/folks/%{abiver}
%dir %{_libdir}/folks/%{abiver}/backends
%dir %{_libdir}/folks/%{abiver}/backends/bluez
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/bluez/bluez.so
%dir %{_libdir}/folks/%{abiver}/backends/dummy
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/dummy/dummy.so
%dir %{_libdir}/folks/%{abiver}/backends/eds
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/eds/eds.so
%dir %{_libdir}/folks/%{abiver}/backends/key-file
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/key-file/key-file.so
%dir %{_libdir}/folks/%{abiver}/backends/ofono
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/ofono/ofono.so
%dir %{_libdir}/folks/%{abiver}/backends/telepathy
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/telepathy/telepathy.so
%dir %{_libdir}/folks/%{abiver}/backends/tracker
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/tracker/tracker.so
%{_datadir}/glib-2.0/schemas/org.freedesktop.folks.gschema.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfolks.so
%attr(755,root,root) %{_libdir}/libfolks-dummy.so
%attr(755,root,root) %{_libdir}/libfolks-eds.so
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so
%attr(755,root,root) %{_libdir}/libfolks-tracker.so
%{_datadir}/gir-1.0/Folks-0.6.gir
%{_datadir}/gir-1.0/FolksDummy-0.6.gir
%{_datadir}/gir-1.0/FolksEds-0.6.gir
%{_datadir}/gir-1.0/FolksTelepathy-0.6.gir
%{_datadir}/gir-1.0/FolksTracker-0.6.gir
%{_includedir}/folks
%{_pkgconfigdir}/folks.pc
%{_pkgconfigdir}/folks-dummy.pc
%{_pkgconfigdir}/folks-eds.pc
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
%{_datadir}/vala/vapi/folks-telepathy.deps
%{_datadir}/vala/vapi/folks-telepathy.vapi
%{_datadir}/vala/vapi/folks-tracker.deps
%{_datadir}/vala/vapi/folks-tracker.vapi
%endif
