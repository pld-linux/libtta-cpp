#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	The lossless True Audio codec C++ library
Summary(pl.UTF-8):	Biblioteka C++ kodeka The lossless True Audio
Name:		libtta-cpp
Version:	2.3
Release:	1
License:	LGPL v3
Group:		Libraries
Source0:	https://downloads.sourceforge.net/tta/%{name}-%{version}.tar.gz
# Source0-md5:	c0b934e854fef32dc8578241e7b233b3
Patch0:		%{name}-shared.patch
URL:		https://sourceforge.net/projects/tta/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains a full-futured codec library for realtime
encoding and decoding of True Audio (TTA) files.

%description -l pl.UTF-8
Ten pakiet zawiera w pełni funkcjonalną bibliotekę kodeka do
kodowania i dekodowania plików True Audio (TTA) w czasie rzeczywistym.

%package devel
Summary:	Header files for TTA C++ library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki C++ TTA
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for TTA C++ library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki C++ TTA.

%package static
Summary:	Static TTA C++ library
Summary(pl.UTF-8):	Statyczna biblioteka C++ TTA
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static TTA C++ library.

%description static -l pl.UTF-8
Statyczna biblioteka C++ TTA.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -Dp libtta.h $RPM_BUILD_ROOT%{_includedir}/libtta.hpp

# the same functionality already in libtta-c
%{__rm} $RPM_BUILD_ROOT%{_bindir}/tta

# no external dependencies
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtta++.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libtta++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtta++.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtta++.so
%{_includedir}/libtta.hpp

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtta++.a
%endif
