# TODO:
# - subpackages for event libraries
# - more event libraries support? (libevent, glib, systemd/sd-event, libubox/uloop)
# - more features? (SQLITE3, FSMOUNT, HUBBUB)
Summary:	Lightweight C library for Websockets
Summary(pl.UTF-8):	Lekka biblioteka C implementująca Websockets
Name:		libwebsockets
Version:	4.3.3
Release:	1
License:	MIT
Group:		Libraries
#SourceDownload: https://github.com/warmcat/libwebsockets/tags
Source0:	https://github.com/warmcat/libwebsockets/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c078b08b712316f6302f54a9d05273ae
Patch0:		no-git.patch
URL:		https://libwebsockets.org/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	libcap-devel
BuildRequires:	libev-devel
BuildRequires:	libuv-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the libwebsockets C library for lightweight websocket clients
and servers.

%description -l pl.UTF-8
libwebsockets to biblioteka C do tworzenia lekkich klientów i serwerów
websockets.

%package devel
Summary:	Headers for developing programs that will use libwebsockets
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia programów wykorzystujących libwebsockets
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files needed for developing
libwebsockets applications.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia aplikacji
opertych na libwebsockets.

%prep
%setup -q
%patch0 -p1

%build
mkdir -p build
cd build

export CFLAGS="%{rpmcflags} -pthread"
%cmake \
	-DLWS_IPV6=ON \
	-DLWS_LINK_TESTAPPS_DYNAMIC=ON \
	-DLWS_SUPPRESS_DEPRECATED_API_WARNINGS=ON \
	-DLWS_UNIX_SOCK=ON \
	-DLWS_USE_BUNDLED_ZLIB=OFF \
	-DLWS_WITH_ACME=ON \
	-DLWS_WITH_DISKCACHE=ON \
	-DLWS_WITH_FTS=ON \
	-DLWS_WITH_HTTP2=ON \
	-DLWS_WITH_HTTP_PROXY=ON \
	-DLWS_WITH_LIBEVENT=OFF \
	-DLWS_WITH_LIBEV=ON \
	-DLWS_WITH_LIBUV=ON \
	-DLWS_WITH_LWSAC=ON \
	-DLWS_WITHOUT_BUILTIN_GETIFADDRS=ON \
	-DLWS_WITHOUT_BUILTIN_SHA1=ON \
	-DLWS_WITHOUT_CLIENT=OFF \
	-DLWS_WITHOUT_SERVER=OFF \
	-DLWS_WITHOUT_TESTAPPS=ON \
	-DLWS_WITHOUT_TEST_CLIENT=ON \
	-DLWS_WITHOUT_TEST_PING=ON \
	-DLWS_WITHOUT_TEST_SERVER_EXTPOLL=ON \
	-DLWS_WITHOUT_TEST_SERVER=ON \
	-DLWS_WITH_RANGES=ON \
	-DLWS_WITH_SOCKS5=ON \
	-DLWS_WITH_STATIC=OFF \
	-DLWS_WITH_THREADPOOL=ON \
	-DLWS_WITH_ZIP_FOPS=ON \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# static library not built
%{__rm} $RPM_BUILD_ROOT%{_pkgconfigdir}/libwebsockets_static.pc

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' \
	$RPM_BUILD_ROOT%{_libdir}/cmake/libwebsockets/LibwebsocketsTargets.cmake

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md changelog
%attr(755,root,root) %{_libdir}/libwebsockets.so.19
%attr(755,root,root) %{_libdir}/libwebsockets-evlib_ev.so
%attr(755,root,root) %{_libdir}/libwebsockets-evlib_uv.so

%files devel
%defattr(644,root,root,755)
%doc READMEs
%attr(755,root,root) %{_libdir}/libwebsockets.so
%{_includedir}/libwebsockets
%{_includedir}/libwebsockets.h
%{_includedir}/lws_config.h
%{_pkgconfigdir}/libwebsockets.pc
%{_libdir}/cmake/libwebsockets
