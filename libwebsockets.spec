Summary:	Lightweight C library for Websockets
Name:		libwebsockets
Version:	4.2.0
Release:	2
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
	-DLWS_SUPPRESS_DEPRECATED_API_WARNINGS=ON \
	-DLWS_WITH_HTTP2=ON \
	-DLWS_IPV6=ON \
	-DLWS_WITH_ZIP_FOPS=ON \
	-DLWS_WITH_SOCKS5=ON \
	-DLWS_WITH_RANGES=ON \
	-DLWS_WITH_ACME=ON \
	-DLWS_WITH_LIBUV=ON \
	-DLWS_WITH_LIBEV=ON \
	-DLWS_WITH_LIBEVENT=OFF \
	-DLWS_WITH_FTS=ON \
	-DLWS_WITH_THREADPOOL=ON \
	-DLWS_UNIX_SOCK=ON \
	-DLWS_WITH_HTTP_PROXY=ON \
	-DLWS_WITH_DISKCACHE=ON \
	-DLWS_WITH_LWSAC=ON \
	-DLWS_LINK_TESTAPPS_DYNAMIC=ON \
	-DLWS_WITHOUT_BUILTIN_GETIFADDRS=ON \
	-DLWS_USE_BUNDLED_ZLIB=OFF \
	-DLWS_WITHOUT_BUILTIN_SHA1=ON \
	-DLWS_WITH_STATIC=OFF \
	-DLWS_WITHOUT_CLIENT=OFF \
	-DLWS_WITHOUT_SERVER=OFF \
	-DLWS_WITHOUT_TESTAPPS=ON \
	-DLWS_WITHOUT_TEST_SERVER=ON \
	-DLWS_WITHOUT_TEST_SERVER_EXTPOLL=ON \
	-DLWS_WITHOUT_TEST_PING=ON \
	-DLWS_WITHOUT_TEST_CLIENT=ON \
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
