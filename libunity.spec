#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Unity instrumenting and integration library
Summary(pl.UTF-8):	Biblioteka oprzyrządowania i integracji Unity
Name:		libunity
Version:	6.12.0
Release:	5
License:	LGPL v3
Group:		Libraries
Source0:	https://launchpad.net/libunity/6.0/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	d7a4d5b1ab317b8ee23e2bae716d67da
Patch0:		vala-ambiguity.patch
URL:		https://launchpad.net/libunity
BuildRequires:	dee-devel >= 1.0.14
BuildRequires:	glib2-devel >= 1:2.32.1
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk+3-devel >= 3.4.1
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libdbusmenu-devel >= 0.4
BuildRequires:	libgee0.6-devel >= 0.6.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	vala >= 2:0.16.0
BuildRequires:	vala-dee >= 1.0.14
BuildRequires:	vala-libdbusmenu >= 0.4
BuildRequires:	vala-libgee0.6 >= 0.6.0
#BuildRequires:	valadoc >= 0.3.3
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	glib2 >= 1:2.32.1
Requires:	dee >= 1.0.14
Requires:	glib2 >= 1:2.32.1
Requires:	libdbusmenu >= 0.4
Requires:	libgee0.6 >= 0.6.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibUnity is a shared library to be able to interact with the launcher
and add places in Unity environment.

%description -l pl.UTF-8
LibUnity to biblioteka współdzielona pozwalająca na interakcję z
programem uruchamiającym (launcherem) i dodawanie miejsc w środowisku
Unity.

%package devel
Summary:	Unity instrumenting and integration library - development files
Summary(pl.UTF-8):	Biblioteka oprzyrządowania i integracji Unity - pliki programistyczne
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dee-devel >= 1.0.14
Requires:	glib2-devel >= 1:2.32.1
Requires:	libdbusmenu-devel >= 0.4
Requires:	libgee0.6-devel >= 0.6.0

%description devel
This package provides the development files required to build
applications which use LibUnity.

%description devel -l pl.UTF-8
Ten pakiet dostarcza pliki programistyczne, wymagane przy tworzeniu
aplikacji wykorzystujących LibUnity.

%package static
Summary:	Static LibUnity library
Summary(pl.UTF-8):	Statyczna biblioteka LibUnity
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LibUnity library.

%description static -l pl.UTF-8
Statyczna biblioteka LibUnity.

%package -n python-unity
Summary:	Python bindings for LibUnity
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki LibUnity
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-pygobject3 >= 3

%description -n python-unity
Python bindings for LibUnity.

%description -n python-unity -l pl.UTF-8
Wiązania Pythona do biblioteki LibUnity.

%package -n vala-libunity
Summary:	Vala API for LibUnity
Summary(pl.UTF-8):	API języka Vala do biblioteki LibUnity
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.16.0
Requires:	vala-dee >= 1.0.14
Requires:	vala-libdbusmenu >= 0.4
Requires:	vala-libgee0.6 >= 0.6.0
BuildArch:	noarch

%description -n vala-libunity
Vala API for LibUnity.

%description -n vala-libunity -l pl.UTF-8
API języka Vala do biblioteki LibUnity.

%prep
%setup -q
%patch -P0 -p1

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libunity.la \
	$RPM_BUILD_ROOT%{_libdir}/libunity/*.la

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%glib_compile_schemas

%postun
/sbin/ldconfig
%glib_compile_schemas

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libunity.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libunity.so.9
%{_libdir}/girepository-1.0/Unity-6.0.typelib
%dir %{_libdir}/libunity
%attr(755,root,root) %{_libdir}/libunity/libunity-protocol-private.so.*
%{_datadir}/glib-2.0/schemas/com.canonical.Unity.Lenses.gschema.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/libunity-tool
%attr(755,root,root) %{_libdir}/libunity.so
%attr(755,root,root) %{_libdir}/libunity/libunity-protocol-private.so
%{_datadir}/gir-1.0/Unity-6.0.gir
%{_includedir}/unity
%{_pkgconfigdir}/unity.pc
%{_pkgconfigdir}/unity-protocol-private.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libunity.a
%{_libdir}/libunity/libunity-protocol-private.a
%endif

%files -n python-unity
%defattr(644,root,root,755)
%{py_sitedir}/gi/overrides/Unity.py[co]

%files -n vala-libunity
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/unity.deps
%{_datadir}/vala/vapi/unity.vapi
%{_datadir}/vala/vapi/unity-protocol.vapi
%{_datadir}/vala/vapi/unity-trace.deps
%{_datadir}/vala/vapi/unity-trace.vapi
