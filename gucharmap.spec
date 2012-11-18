Summary:	Unicode character map
Name:		gucharmap
Version:	3.6.1
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gucharmap/3.6/%{name}-%{version}.tar.xz
# Source0-md5:	a0e0cdf05a0db8a66b2da35b4f8b7f6e
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkg-config
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	rarian
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gucharmap is a featureful unicode character map.

%package libs
Summary:	gucharmap library
Group:		Development/Libraries

%description libs
This package contains gucharmap library.

%package devel
Summary:	Headers for gucharmap
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
The gucharmap-devel package includes the header files that you will
need to use gucharmap.

%prep
%setup -q

# kill gnome common deps
sed -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__libtoolize}
%{__intltoolize}
%{__gnome_doc_prepare}
%{__aclocal } -I m4
%{__automake}
%{__autoconf}
%configure \
	--disable-scrollkeeper	\
	--disable-silent-rules	\
	--disable-static	\
	--enable-introspection	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%update_gsettings_cache

%postun
%scrollkeeper_update_postun
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*map
%{_datadir}/glib-2.0/schemas/*.xml
%{_desktopdir}/*.desktop

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libgucharmap_*.so.?
%attr(755,root,root) %{_libdir}/libgucharmap_*.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgucharmap_*.so
%{_datadir}/gir-1.0/*.gir
%{_includedir}/%{name}-2.90
%{_pkgconfigdir}/%{name}-2.90.pc

