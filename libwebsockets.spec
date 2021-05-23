Summary:	Lightweight C library for Websockets
Name:		libwebsockets
Version:	4.2.0
Release:	1
License:	MIT
Source0:	https://github.com/warmcat/libwebsockets/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e6613bf565664adb6954f17c8e908149
Patch0:		no-git.patch
URL:		http://libwebsockets.org
BuildRequires:	cmake
BuildRequires:	libev-devel
BuildRequires:	libuv-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel

%description
This is the libwebsockets C library for lightweight websocket clients
and servers.

%package devel
Summary:	Headers for developing programs that will use %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libev-devel
Requires:	libuv-devel

%description devel
This package contains the header files needed for developing %{name}
applications.

%prep
%setup -q
%patch0 -p1

%build
mkdir -p build
cd build

export CFLAGS="%{rpmcflags} -pthread"
%cmake \
	-D LWS_WITH_HTTP2=ON \
	-D LWS_IPV6=ON \
	-D LWS_WITH_ZIP_FOPS=ON \
	-D LWS_WITH_SOCKS5=ON \
	-D LWS_WITH_RANGES=ON \
	-D LWS_WITH_ACME=ON \
	-D LWS_WITH_LIBUV=ON \
	-D LWS_WITH_LIBEV=ON \
	-D LWS_WITH_LIBEVENT=OFF \
	-D LWS_WITH_FTS=ON \
	-D LWS_WITH_THREADPOOL=ON \
	-D LWS_UNIX_SOCK=ON \
	-D LWS_WITH_HTTP_PROXY=ON \
	-D LWS_WITH_DISKCACHE=ON \
	-D LWS_WITH_LWSAC=ON \
	-D LWS_LINK_TESTAPPS_DYNAMIC=ON \
	-D LWS_WITHOUT_BUILTIN_GETIFADDRS=ON \
	-D LWS_USE_BUNDLED_ZLIB=OFF \
	-D LWS_WITHOUT_BUILTIN_SHA1=ON \
	-D LWS_WITH_STATIC=OFF \
	-D LWS_WITHOUT_CLIENT=OFF \
	-D LWS_WITHOUT_SERVER=OFF \
	-D LWS_WITHOUT_TESTAPPS=ON \
	-D LWS_WITHOUT_TEST_SERVER=ON \
	-D LWS_WITHOUT_TEST_SERVER_EXTPOLL=ON \
	-D LWS_WITHOUT_TEST_PING=ON \
	-D LWS_WITHOUT_TEST_CLIENT=ON \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -delete
find $RPM_BUILD_ROOT -name '*_static.pc' -delete

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md changelog
%attr(755,root,root) %{_libdir}/%{name}.so.18

%files devel
%defattr(644,root,root,755)
%doc READMEs/README.coding.md READMEs
%{_includedir}/*.h
%{_includedir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}*.so
%{_pkgconfigdir}/%{name}.pc
%{_libdir}/cmake/libwebsockets
