#
# Conditional build:
%bcond_with	apidocs		# API documentation (broken install: HTML for devhelp part, sources+HTML for gtk-doc?)
%bcond_without	vala		# Vala API
%bcond_without	bluez		# Bluez backend
%bcond_without	evolution	# EDS (Evolution Data Server) backend
%bcond_without	ofono		# oFono backend
%bcond_without	telepathy	# Telepathy backend
%bcond_without	zeitgeist	# ` Zeitgeist support in Telepathy backend
%bcond_without	tracker		# Tracker backend

%if %{without telepathy}
%undefine	with_zeitgeist
%endif
Summary:	GObject contact aggregation library
Summary(pl.UTF-8):	Biblioteka GObject do agregowania kontaktów
Name:		folks
Version:	0.14.0
Release:	2
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/folks/0.14/%{name}-%{version}.tar.xz
# Source0-md5:	dc852fceab9e84362b675d5ffcd4803e
Patch0:		%{name}-meson.patch
Patch1:		%{name}-module.patch
Patch2:		%{name}-vala.patch
URL:		https://wiki.gnome.org/Projects/Folks
BuildRequires:	dbus-devel
%{?with_telepathy:BuildRequires:	dbus-glib-devel}
%if %{with bluez} || %{with evolution} || %{with ofono}
# libebook for all; libebook-contacts, libedataserver, evolution-data-server for evolution
BuildRequires:	evolution-data-server-devel >= 3.33.2
%endif
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	libgee-devel >= 0.8.4
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	meson >= 0.51
BuildRequires:	ncurses-devel
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.21
BuildRequires:	python3 >= 1:3.2
%{?with_bluez:BuildRequires:	python3-dbusmock}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	readline-devel
BuildRequires:	tar >= 1:1.22
%{?with_telepathy:BuildRequires:	telepathy-glib-devel >= 0.19.9}
%{?with_tracker:BuildRequires:	tracker-devel >= 2.0}
%if %{with vala}
BuildRequires:	vala >= 2:0.22.1
%if %{with bluez} || %{with evolution} || %{with ofono}
BuildRequires:	vala-evolution-data-server >= 3.33.2
%endif
BuildRequires:	vala-libgee >= 0.8.4
%{?with_telepathy:BuildRequires:	vala-telepathy-glib >= 0.19.9}
%{?with_tracker:BuildRequires:	vala-tracker >= 2.0}
%{?with_zeitgeist:BuildRequires:	vala-zeitgeist >= 0.9.14}
%endif
%{?with_apidocs:BuildRequires:	valadoc >= 0.3.1}
BuildRequires:	xz
%{?with_zeitgeist:BuildRequires:	zeitgeist-devel >= 0.9.14}
%if %{with bluez} || %{with evolution} || %{with ofono}
Requires:	evolution-data-server-libs >= 3.33.2
%endif
Requires:	glib2 >= 1:2.44
Requires:	libgee >= 0.8.4
%{?with_telepathy:Requires:	telepathy-glib >= 0.19.9}
%{?with_tracker:Requires:	tracker-libs >= 2.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abiver	46

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
%if %{with bluez} || %{with evolution} || %{with ofono}
Requires:	evolution-data-server-devel >= 3.33.2
%endif
Requires:	glib2-devel >= 1:2.44
Requires:	libgee-devel >= 0.8.4
%{?with_telepathy:Requires:	telepathy-glib-devel >= 0.19.9}
%{?with_tracker:Requires:	tracker-devel >= 2.0}

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
%if %{with bluez} || %{with evolution} || %{with ofono}
Requires:	vala-evolution-data-server >= 3.33.2
%endif
Requires:	vala-libgee >= 0.8.4
%{?with_telepathy:Requires:	vala-telepathy-glib >= 0.19.9}
%{?with_tracker:Requires:	vala-tracker >= 2.0}
BuildArch:	noarch

%description -n vala-folks
folks API for Vala language.

%description -n vala-folks -l pl.UTF-8
API folks dla języka Vala.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%meson build \
	%{!?with_bluez:-Dbluez_backend=false} \
	%{?with_apidocs:-Ddocs=true} \
	%{!?with_evolution:-Deds_backend=false} \
	%{!?with_ofono:-Dofono_backend=false} \
	%{?with_tracker:-Dtracker_backend=true} \
	%{!?with_telepathy:-Dtelepathy_backend=false} \
	%{?with_zeitgeist:-Dzeitgeist=true}

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
%{_libdir}/girepository-1.0/Folks-0.6.typelib
%{_libdir}/girepository-1.0/FolksDummy-0.6.typelib
%dir %{_libdir}/folks
%dir %{_libdir}/folks/%{abiver}
%dir %{_libdir}/folks/%{abiver}/backends
%dir %{_libdir}/folks/%{abiver}/backends/dummy
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/dummy/dummy.so
%dir %{_libdir}/folks/%{abiver}/backends/key-file
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/key-file/key-file.so
%if %{with bluez}
%dir %{_libdir}/folks/%{abiver}/backends/bluez
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/bluez/bluez.so
%endif
%if %{with ofono}
%dir %{_libdir}/folks/%{abiver}/backends/ofono
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/ofono/ofono.so
%endif
%if %{with evolution}
%attr(755,root,root) %{_libdir}/libfolks-eds.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-eds.so.25
%{_libdir}/girepository-1.0/FolksEds-0.6.typelib
%dir %{_libdir}/folks/%{abiver}/backends/eds
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/eds/eds.so
%endif
%if %{with telepathy}
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-telepathy.so.25
%{_libdir}/girepository-1.0/FolksTelepathy-0.6.typelib
%dir %{_libdir}/folks/%{abiver}/backends/telepathy
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/telepathy/telepathy.so
%endif
%if %{with tracker}
%attr(755,root,root) %{_libdir}/libfolks-tracker.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-tracker.so.25
%{_libdir}/girepository-1.0/FolksTracker-0.6.typelib
%dir %{_libdir}/folks/%{abiver}/backends/tracker
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/tracker/tracker.so
%endif
%{_datadir}/GConf/gsettings/folks.convert
%{_datadir}/glib-2.0/schemas/org.freedesktop.folks.gschema.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfolks.so
%attr(755,root,root) %{_libdir}/libfolks-dummy.so
%{_datadir}/gir-1.0/Folks-0.6.gir
%{_datadir}/gir-1.0/FolksDummy-0.6.gir
%{_includedir}/folks
%{_pkgconfigdir}/folks.pc
%{_pkgconfigdir}/folks-dummy.pc
%if %{with evolution}
%attr(755,root,root) %{_libdir}/libfolks-eds.so
%{_datadir}/gir-1.0/FolksEds-0.6.gir
%{_pkgconfigdir}/folks-eds.pc
%endif
%if %{with telepathy}
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so
%{_datadir}/gir-1.0/FolksTelepathy-0.6.gir
%{_pkgconfigdir}/folks-telepathy.pc
%endif
%if %{with tracker}
%attr(755,root,root) %{_libdir}/libfolks-tracker.so
%{_datadir}/gir-1.0/FolksTracker-0.6.gir
%{_pkgconfigdir}/folks-tracker.pc
%endif

%if %{with vala}
%files -n vala-folks
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/folks.deps
%{_datadir}/vala/vapi/folks.vapi
%{_datadir}/vala/vapi/folks-dummy.deps
%{_datadir}/vala/vapi/folks-dummy.vapi
%if %{with evolution}
%{_datadir}/vala/vapi/folks-eds.deps
%{_datadir}/vala/vapi/folks-eds.vapi
%endif
%if %{with telepathy}
%{_datadir}/vala/vapi/folks-telepathy.deps
%{_datadir}/vala/vapi/folks-telepathy.vapi
%endif
%if %{with tracker}
%{_datadir}/vala/vapi/folks-tracker.deps
%{_datadir}/vala/vapi/folks-tracker.vapi
%endif
%endif
