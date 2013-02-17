Summary:	Unity instrumenting and integration library
Name:		libunity
Version:	5.12.0
Release:	2
License:	LGPL v3
Group:		Libraries
URL:		http://launchpad.net/libunity
Source0:	https://launchpad.net/libunity/5.0/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	41245701df2b7dc24af2b92bffb675be
BuildRequires:	dee-devel >= 1.0.14
BuildRequires:	glib2-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	libdbusmenu-devel
BuildRequires:	libgee0.6-devel
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	vala
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libunity is a shared library to be able to interact with the launcher
and add places in Unity environment.

%package devel
Summary:	Unity instrumenting and integration library - development files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package provides the development files required to build
applications.

%package -n python-unity
Summary:	Python bindings for libunity
Group:		Development/Languages/Python

%description -n python-unity
Python bindings Libunity is a shared library to be able to interact
with the launcher and add places in Unity environment.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--disable-static \
	--enable-gtk-doc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libunity.la

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libunity.so.*.*.*
%ghost %{_libdir}/libunity.so.9
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/unity-tool
%dir %{_includedir}/unity
%{_includedir}/unity/unity
%{_libdir}/libunity.so
%{_pkgconfigdir}/unity.pc
%{_datadir}/vala/vapi/unity-trace.deps
%{_datadir}/vala/vapi/unity-trace.vapi
%{_datadir}/vala/vapi/unity.deps
%{_datadir}/vala/vapi/unity.vapi
%{_datadir}/gir-1.0/Unity-5.0.gir

%files -n python-unity
%defattr(644,root,root,755)
%{py_sitedir}/gi/overrides/Unity.py[co]
