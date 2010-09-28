Summary:	GObject contact aggregation library
Name:		folks
Version:	0.2.0
Release:	1
License:	LGPL v2+
Group:		Libraries
URL:		http://telepathy.freedesktop.org/wiki/Folks
Source0:	http://download.gnome.org/sources/folks/0.2/%{name}-%{version}.tar.bz2
# Source0-md5:	8c66c03d942313db735f6eb375c2f71a
Patch0:		telepathy-glib-vala.patch
BuildRequires:	libgee-devel
BuildRequires:	telepathy-glib-devel
BuildRequires:	vala >= 0.9.7

%description
libfolks is a library that aggregates people from multiple sources
(e.g. Telepathy connection managers and eventually evolution data
server, Facebook, etc.) to create meta-contacts.


%package        devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-static \

%{__make} %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/folks-import
%attr(755,root,root) %{_libdir}/libfolks.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks.so.0
%attr(755,root,root) %{_libdir}/libfolks-telepathy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfolks-telepathy.so.0
%{_libdir}/folks
%{_datadir}/vala/vapi/folks.*
%{_datadir}/vala/vapi/folks-telepathy.*

%files devel
%defattr(644,root,root,755)
%doc
%{_includedir}/folks
%{_libdir}/libfolks.so
%{_libdir}/libfolks-telepathy.so
%{_pkgconfigdir}/folks.pc
%{_pkgconfigdir}/folks-telepathy.pc
