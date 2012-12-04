#
# Conditional build:
%bcond_without	vala		# do not build Vala API
#
Summary:	GObject contact aggregation library
Name:		folks
Version:	0.8.0
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/folks/0.8/%{name}-%{version}.tar.xz
# Source0-md5:	5664f85c4acdda2934cbd08a9d3d78e3
URL:		https://live.gnome.org/Folks
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-glib-devel
BuildRequires:	evolution-data-server-devel >= 3.6.0
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	intltool >= 0.50.0
BuildRequires:	libgee0.6-devel
BuildRequires:	libsocialweb-devel >= 0.25.20
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libzeitgeist-devel >= 0.3.14
BuildRequires:	pkgconfig >= 1:0.21
BuildRequires:	readline-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	telepathy-glib-devel >= 0.19.0
BuildRequires:	tracker-devel >= 0.14.0
%if %{with vala}
BuildRequires:	vala >= 2:0.17.6
BuildRequires:	vala-evolution-data-server >= 3.6.0
BuildRequires:	vala-libgee0.6
BuildRequires:	vala-libsocialweb >= 0.25.20
BuildRequires:	vala-telepathy-glib >= 0.19.0
BuildRequires:	vala-zeitgeist >= 0.3.14
BuildRequires:	vala-tracker >= 0.14.0
%endif
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
Requires:	evolution-data-server-devel >= 3.6.0
Requires:	glib2-devel >= 1:2.32.0
Requires:	libgee0.6-devel
Requires:	libsocialweb-devel >= 0.25.20
Requires:	telepathy-glib-devel >= 0.19.0
Requires:	tracker-devel >= 0.14.0

%description devel
Development files for folks libraries.

%description devel -l pl.UTF-8
Pliki programistyczne bibliotek folks.

%package -n vala-folks
Summary:	folks API for Vala language
Summary(pl.UTF-8):	API folks dla języka Vala
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

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
	--disable-silent-rules \
	--disable-static \
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
%attr(755,root,root) %{_libdir}/libfolks-tracker.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-tracker.so.25
%dir %{_libdir}/folks
%dir %{_libdir}/folks/37
%dir %{_libdir}/folks/37/backends
%dir %{_libdir}/folks/37/backends/eds
%attr(755,root,root) %{_libdir}/folks/37/backends/eds/eds.so
%dir %{_libdir}/folks/37/backends/key-file
%attr(755,root,root) %{_libdir}/folks/37/backends/key-file/key-file.so
%dir %{_libdir}/folks/37/backends/libsocialweb
%attr(755,root,root) %{_libdir}/folks/37/backends/libsocialweb/libsocialweb.so
%dir %{_libdir}/folks/37/backends/telepathy
%attr(755,root,root) %{_libdir}/folks/37/backends/telepathy/telepathy.so
%dir %{_libdir}/folks/37/backends/tracker
%attr(755,root,root) %{_libdir}/folks/37/backends/tracker/tracker.so
%{_libdir}/girepository-1.0/*.typelib
%{_datadir}/GConf/gsettings/folks.convert
%{_datadir}/glib-2.0/schemas/org.freedesktop.folks.gschema.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfolks.so
%attr(755,root,root) %{_libdir}/libfolks-eds.so
%attr(755,root,root) %{_libdir}/libfolks-libsocialweb.so
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so
%attr(755,root,root) %{_libdir}/libfolks-tracker.so
%{_datadir}/gir-1.0/*.gir
%{_includedir}/folks
%{_pkgconfigdir}/folks.pc
%{_pkgconfigdir}/folks-eds.pc
%{_pkgconfigdir}/folks-libsocialweb.pc
%{_pkgconfigdir}/folks-telepathy.pc
%{_pkgconfigdir}/folks-tracker.pc

%if %{with vala}
%files -n vala-folks
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/folks.deps
%{_datadir}/vala/vapi/folks.vapi
%{_datadir}/vala/vapi/folks-eds.deps
%{_datadir}/vala/vapi/folks-eds.vapi
%{_datadir}/vala/vapi/folks-libsocialweb.deps
%{_datadir}/vala/vapi/folks-libsocialweb.vapi
%{_datadir}/vala/vapi/folks-telepathy.deps
%{_datadir}/vala/vapi/folks-telepathy.vapi
%{_datadir}/vala/vapi/folks-tracker.deps
%{_datadir}/vala/vapi/folks-tracker.vapi
%endif
