Summary:	GObject contact aggregation library
Name:		folks
Version:	0.5.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/folks/0.5/%{name}-%{version}.tar.bz2
# Source0-md5:	b1fb6e35cd91e05dae30206d46cefdc8
URL:		http://telepathy.freedesktop.org/wiki/Folks
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.24.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libgee-devel < 0.7
BuildRequires:	libsocialweb-devel >= 0.25.15-2
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig >= 1:0.21
BuildRequires:	telepathy-glib-devel >= 0.13.1
BuildRequires:	vala >= 1:0.12.0
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
Requires:	glib2-devel >= 1:2.24.0
Requires:	libgee-devel < 0.7
Requires:	telepathy-glib-devel >= 0.13.1

%description devel
Development files for folks libraries.

%description devel -l pl.UTF-8
Pliki programistyczne bibliotek folks.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--disable-static \
	--enable-vala

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/folks/*/backends/*/libfolks-backend-*.la \
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
%attr(755,root,root) %ghost %{_libdir}/libfolks.so.22
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-telepathy.so.22
%attr(755,root,root) %{_libdir}/libfolks-libsocialweb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-libsocialweb.so.22
%dir %{_libdir}/folks
%dir %{_libdir}/folks/23
%dir %{_libdir}/folks/23/backends
%dir %{_libdir}/folks/23/backends/key-file
%attr(755,root,root) %{_libdir}/folks/23/backends/key-file/libfolks-backend-key-file.so
%dir %{_libdir}/folks/23/backends/libsocialweb
%attr(755,root,root) %{_libdir}/folks/23/backends/libsocialweb/libfolks-backend-libsocialweb.so
%dir %{_libdir}/folks/23/backends/telepathy
%attr(755,root,root) %{_libdir}/folks/23/backends/telepathy/libfolks-backend-telepathy.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfolks.so
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so
%attr(755,root,root) %{_libdir}/libfolks-libsocialweb.so
%{_datadir}/vala/vapi/folks.deps
%{_datadir}/vala/vapi/folks.vapi
%{_datadir}/vala/vapi/folks-libsocialweb.deps
%{_datadir}/vala/vapi/folks-libsocialweb.vapi
%{_datadir}/vala/vapi/folks-telepathy.deps
%{_datadir}/vala/vapi/folks-telepathy.vapi
%{_includedir}/folks
%{_pkgconfigdir}/folks.pc
%{_pkgconfigdir}/folks-telepathy.pc
%{_pkgconfigdir}/folks-libsocialweb.pc
