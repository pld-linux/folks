Summary:	GObject contact aggregation library
Name:		folks
Version:	0.4.3
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/folks/0.4/%{name}-%{version}.tar.bz2
# Source0-md5:	82e3b69de10e5dd59bae170b595f8ad7
URL:		http://telepathy.freedesktop.org/wiki/Folks
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.24.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libgee-devel < 0.7
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig >= 1:0.21
BuildRequires:	telepathy-glib-devel >= 0.13.1
BuildRequires:	vala >= 2:0.11.6
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

%{__rm} $RPM_BUILD_ROOT%{_libdir}/folks/22/backends/*/libfolks-backend-*.la \
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
%attr(755,root,root) %{_libdir}/libfolks.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks.so.22
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-telepathy.so.22
%dir %{_libdir}/folks
%dir %{_libdir}/folks/22
%dir %{_libdir}/folks/22/backends
%dir %{_libdir}/folks/22/backends/*
%attr(755,root,root) %{_libdir}/folks/22/backends/*/libfolks-backend-*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfolks.so
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so
%{_datadir}/vala/vapi/folks.*
%{_datadir}/vala/vapi/folks-telepathy.*
%{_includedir}/folks
%{_pkgconfigdir}/folks.pc
%{_pkgconfigdir}/folks-telepathy.pc
