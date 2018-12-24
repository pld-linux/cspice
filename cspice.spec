# TODO: build actual tools (for now only library is prepared, for use by other packages)
Summary:	ANSI C version of the SPICE Toolkit
Summary(pl.UTF-8):	Wersja oprogramowania SPICE Toolkit dla ANSI C
Name:		cspice
Version:	66
Release:	1
License:	NASA/CalTech
Group:		Libraries
# couldn't find pure source distribution, but binary package contains sources as well
Source0:	http://naif.jpl.nasa.gov/pub/naif/toolkit/C/PC_Linux_GCC_32bit/packages/cspice.tar.Z
# Source0-md5:	35a5e7f8e9501b503b18d94ca8a9da47
URL:		https://naif.jpl.nasa.gov/naif/toolkit.html
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ANSI C version of the SPICE Toolkit.

%description -l pl.UTF-8
Wersja oprogramowania SPICE Toolkit dla ANSI C.

%package devel
Summary:	Header files for CSPICE library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CSPICE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for CSPICE library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CSPICE.

%package static
Summary:	Static CSPICE library
Summary(pl.UTF-8):	Statyczna biblioteka CSPICE
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CSPICE library.

%description static -l pl.UTF-8
Statyczna biblioteka CSPICE.

%package doc
Summary:	Documentation for CSPICE
Summary(pl.UTF-8):	Dokumentacja do CSPICE
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
Documentation for CSPICE.

%description doc -l pl.UTF-8
Dokumentacja do CSPICE.

%prep
%setup -q -n %{name}

%{__rm} lib/*.a exe/*

%build
cd src/cspice

for f in *.c ; do
	libtool --mode=compile %{__cc} %{rpmcflags} %{rpmcppflags} -c $f
done
libtool --mode=link %{__cc} %{rpmldflags} %{rpmcflags} -o libcspice.la -lm -rpath %{_libdir} *.lo

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

libtool --mode=install install src/cspice/libcspice.la $RPM_BUILD_ROOT%{_libdir}

cp -p include/Spice*.h $RPM_BUILD_ROOT%{_includedir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcspice.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/{dscriptn.txt,version.txt,whats.new}
%attr(755,root,root) %{_libdir}/libcspice.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcspice.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcspice.so
%{_includedir}/Spice*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libcspice.a

%files doc
%defattr(644,root,root,755)
%doc doc/html/*
