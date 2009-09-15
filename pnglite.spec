# Upstream doesn't use a SONAME and nobody knows how stable the interface is
# Please take extra care when updating this package -- bump the following
# and rebuild dependencies (shouldn't be many) if you suspect an ABI change:
%define abi_major 0
%define abi_minor 1
%define libname %mklibname %name %abi_major
%define libnamedevel %mklibname -d %name

Name:           pnglite
Version:        0.1.17
Release:        %mkrel 2
Summary:        A lightweight C library for loading PNG images

Group:          System/Libraries
License:        Zlib
URL:            http://www.karlings.com/~danne/pnglite/
Source0:        http://downloads.sourceforge.net/pnglite/%{name}-%{version}.zip
Patch0:         pnglite-0.1.17-zlib.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  zlib-devel

%description
pnglite is a C library for loading PNG images. It was created as a
substitute for libpng in situations when libpng is more than enough. It
currently requires zlib for inflate and crc checking and it can read the
most common types of PNG images. The library has a small and simple to use
interface.

%package -n %libname
Summary:        A lightweight C library for loading PNG images
Group:          System/Libraries
Provides:       pnglite = %{version}-%{release}

%description -n %libname
pnglite is a C library for loading PNG images. It was created as a
substitute for libpng in situations when libpng is more than enough. It
currently requires zlib for inflate and crc checking and it can read the
most common types of PNG images. The library has a small and simple to use
interface.

%package -n %libnamedevel
Summary:        Files needed to build and link programs with pnglite
Group:          Development/C
Requires:       %libname = %{version}-%{release}
Provides:       pnglite-devel = %{version}-%{release}

%description -n %libnamedevel
This contains a header file and a link to library for the linker
to link against pnglite.

%prep
%setup -q -c
%patch0 -p1 -b .zlib
sed 's/\r//' -i pnglite.h

%build
gcc %{optflags} -shared -fPIC -Wl,--soname,libpnglite.so.%{abi_major} \
       -o libpnglite.so.%{abi_major}.%{abi_minor} pnglite.c

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}

install -pm 0644 pnglite.h $RPM_BUILD_ROOT%{_includedir}
install libpnglite.so.%{abi_major}.%{abi_minor} $RPM_BUILD_ROOT%{_libdir}
ln -s libpnglite.so.%{abi_major}.%{abi_minor} $RPM_BUILD_ROOT%{_libdir}/libpnglite.so.%{abi_major}
ln -s libpnglite.so.%{abi_major}.%{abi_minor} $RPM_BUILD_ROOT%{_libdir}/libpnglite.so

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files -n %libnamedevel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/*.h

