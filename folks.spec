Summary:	GObject contact aggregation library
Name:		folks
Version:	0.3.6
Release:	1
License:	LGPL v2+
Group:		Libraries
URL:		http://telepathy.freedesktop.org/wiki/Folks
Source0:	http://download.gnome.org/sources/folks/0.3/%{name}-%{version}.tar.bz2
# Source0-md5:	a708f45d67620294effd33fd88f2a81d
BuildRequires:	libgee-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
BuildRequires:	telepathy-glib-devel
BuildRequires:	vala >= 0.9.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libfolks is a library that aggregates people from multiple sources
(e.g. Telepathy connection managers and eventually evolution data
server, Facebook, etc.) to create meta-contacts.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure \
	--disable-static

%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

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
%attr(755,root,root) %ghost %{_libdir}/libfolks.so.21
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-telepathy.so.21
%dir %{_libdir}/folks
%dir %{_libdir}/folks/21
%dir %{_libdir}/folks/21/backends
%dir %{_libdir}/folks/21/backends/*
%attr(755,root,root) %{_libdir}/folks/21/backends/*/libfolks-backend-*.so
%{_datadir}/vala/vapi/folks.*
%{_datadir}/vala/vapi/folks-telepathy.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/folks
%{_libdir}/libfolks.so
%{_libdir}/libfolks-telepathy.so
%{_pkgconfigdir}/folks.pc
%{_pkgconfigdir}/folks-telepathy.pc
