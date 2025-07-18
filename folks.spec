#
# Conditional build:
%bcond_with	apidocs		# API documentation (broken install: HTML for devhelp part, sources+HTML for gtk-doc?)
%bcond_without	vala		# Vala API
%bcond_without	bluez		# Bluez backend
%bcond_without	evolution	# EDS (Evolution Data Server) backend
%bcond_without	ofono		# oFono backend
%bcond_with	sysprof		# sysprof based profiling
%bcond_without	telepathy	# Telepathy backend
%bcond_without	zeitgeist	# ` Zeitgeist support in Telepathy backend

%if %{without telepathy}
%undefine	with_zeitgeist
%endif
Summary:	GObject contact aggregation library
Summary(pl.UTF-8):	Biblioteka GObject do agregowania kontaktów
Name:		folks
Version:	0.15.9
Release:	2
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/folks/0.15/%{name}-%{version}.tar.xz
# Source0-md5:	e297a1fa21839522777be991782f9543
Patch0:		%{name}-meson.patch
URL:		https://wiki.gnome.org/Projects/Folks
BuildRequires:	dbus-devel
%{?with_telepathy:BuildRequires:	dbus-glib-devel}
%if %{with bluez} || %{with evolution} || %{with ofono}
# libebook for all; libebook-contacts, libedataserver, evolution-data-server for evolution
BuildRequires:	evolution-data-server-devel >= 3.38
%endif
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.58
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	libgee-devel >= 0.8.4
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	meson >= 0.57
BuildRequires:	ncurses-devel
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.21
BuildRequires:	python3 >= 1:3.2
%{?with_bluez:BuildRequires:	python3-dbusmock}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	readline-devel
%{?with_sysprof:BuildRequires:	sysprof-devel >= 3.38.0}
BuildRequires:	tar >= 1:1.22
%{?with_telepathy:BuildRequires:	telepathy-glib-devel >= 0.19.9}
%if %{with vala}
BuildRequires:	vala >= 2:0.22.1
%if %{with bluez} || %{with evolution} || %{with ofono}
BuildRequires:	vala-evolution-data-server >= 3.38
%endif
BuildRequires:	vala-libgee >= 0.8.4
%{?with_telepathy:BuildRequires:	vala-telepathy-glib >= 0.19.9}
%{?with_zeitgeist:BuildRequires:	vala-zeitgeist >= 0.9.14}
%endif
%{?with_apidocs:BuildRequires:	valadoc >= 0.3.1}
BuildRequires:	xz
%{?with_zeitgeist:BuildRequires:	zeitgeist-devel >= 0.9.14}
%if %{with bluez} || %{with evolution} || %{with ofono}
Requires:	evolution-data-server-libs >= 3.38
%endif
Requires:	glib2 >= 1:2.58
Requires:	libgee >= 0.8.4
%{?with_telepathy:Requires:	telepathy-glib >= 0.19.9}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abiver	26

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
Requires:	evolution-data-server-devel >= 3.38
%endif
Requires:	glib2-devel >= 1:2.58
Requires:	libgee-devel >= 0.8.4
%{?with_telepathy:Requires:	telepathy-glib-devel >= 0.19.9}

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
Requires:	vala-evolution-data-server >= 3.38
%endif
Requires:	vala-libgee >= 0.8.4
%{?with_telepathy:Requires:	vala-telepathy-glib >= 0.19.9}
BuildArch:	noarch

%description -n vala-folks
folks API for Vala language.

%description -n vala-folks -l pl.UTF-8
API folks dla języka Vala.

%prep
%setup -q
%patch -P0 -p1

%build
%meson \
	%{!?with_bluez:-Dbluez_backend=false} \
	%{?with_apidocs:-Ddocs=true} \
	%{!?with_evolution:-Deds_backend=false} \
	%{!?with_ofono:-Dofono_backend=false} \
	%{?with_sysprof:-Dprofiling=true} \
	%{!?with_telepathy:-Dtelepathy_backend=false} \
	%{?with_zeitgeist:-Dzeitgeist=true}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_bindir}/folks-import
%attr(755,root,root) %{_bindir}/folks-inspect
%attr(755,root,root) %{_libdir}/libfolks.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks.so.26
%attr(755,root,root) %{_libdir}/libfolks-dummy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-dummy.so.26
%{_libdir}/girepository-1.0/Folks-0.7.typelib
%{_libdir}/girepository-1.0/FolksDummy-0.7.typelib
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
%attr(755,root,root) %ghost %{_libdir}/libfolks-eds.so.26
%{_libdir}/girepository-1.0/FolksEds-0.7.typelib
%dir %{_libdir}/folks/%{abiver}/backends/eds
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/eds/eds.so
%endif
%if %{with telepathy}
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-telepathy.so.26
%{_libdir}/girepository-1.0/FolksTelepathy-0.7.typelib
%dir %{_libdir}/folks/%{abiver}/backends/telepathy
%attr(755,root,root) %{_libdir}/folks/%{abiver}/backends/telepathy/telepathy.so
%endif
%{_datadir}/GConf/gsettings/folks.convert
%{_datadir}/glib-2.0/schemas/org.freedesktop.folks.gschema.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfolks.so
%attr(755,root,root) %{_libdir}/libfolks-dummy.so
%{_datadir}/gir-1.0/Folks-0.7.gir
%{_datadir}/gir-1.0/FolksDummy-0.7.gir
%{_includedir}/folks
%{_pkgconfigdir}/folks.pc
%{_pkgconfigdir}/folks-dummy.pc
%if %{with evolution}
%attr(755,root,root) %{_libdir}/libfolks-eds.so
%{_datadir}/gir-1.0/FolksEds-0.7.gir
%{_pkgconfigdir}/folks-eds.pc
%endif
%if %{with telepathy}
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so
%{_datadir}/gir-1.0/FolksTelepathy-0.7.gir
%{_pkgconfigdir}/folks-telepathy.pc
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
%endif
