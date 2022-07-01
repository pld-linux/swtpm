# TODO: handle selinux policy files
#
# Conditional build:
%bcond_without	tests	# unit/functional tests

Summary:	Software TPM Emulator
Summary(pl.UTF-8):	Programowy emulator TPM
Name:		swtpm
Version:	0.7.3
Release:	1
License:	BSD
Group:		Development/Tools
#Source0Download: https://github.com/stefanberger/swtpm/releases
Source0:	https://github.com/stefanberger/swtpm/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	cd3a35094cbc627c07dd4d54c56c8e5b
URL:		https://github.com/stefanberger/swtpm
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.11
BuildRequires:	gawk
BuildRequires:	glib2-devel >= 2.0
# certtool
BuildRequires:	gnutls >= 3.4.0
BuildRequires:	gnutls-devel >= 3.4.0
BuildRequires:	json-glib-devel
BuildRequires:	libfuse-devel
BuildRequires:	libseccomp-devel
BuildRequires:	libtasn1-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libtpms-devel >= 0.6
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	sed >= 4.0
%if %{with tests}
# tcsd?
BuildRequires:	expect
# netstat (or ss from iproute2)
BuildRequires:	net-tools
BuildRequires:	socat
%endif
Requires:	expect
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SWTPM package provides TPM emulators with different front-end
interfaces to libtpms. TPM emulators provide socket interfaces
(TCP/IP and Unix) and the Linux CUSE interface for the creation of
multiple native /dev/vtpm* devices.

The SWTPM package also provides several tools for using the TPM
emulator, creating certificates for a TPM, and simulating the
manufacturing of a TPM by creating a TPM's EK and platform
certificates etc.

%description -l pl.UTF-8
Pakiet SWTPM zapewnia emulatory TPM z różnymi interfejsami
frontendowymi do libtpms. Emulatory udostępniają interfejsy gniazdowe
(TCP/IP i uniksowe) oraz interfejs linuksowy CUSE do tworzenia wielu
natywnych urządzeń /dev/vtpm*.

Pakiet zawiera także kilka narzędzi do używania emulatora TPM,
tworzenia certyfikatów dla TPM oraz symulowania wytwarzania TPM
poprzez tworzenie EK dla TPM, certyfikatów platformy itp.

%package devel
Summary:	Header file with SWTPM ioctl definitions
Summary(pl.UTF-8):	Plik nagłówkowy z definicjami ioctl SWTPM
Group:		Development/Libraries
BuildArch:	noarch

%description devel
Header file with SWTPM ioctl definitions.

%description devel -l pl.UTF-8
Plik nagłówkowy z definicjami ioctl SWTPM.

%prep
%setup -q

%{__sed} -i -e '1s,/usr/bin/env bash,/bin/bash,' samples/{swtpm-create-tpmca,swtpm-create-user-config-files.in}
%{__sed} -i -e '1s,/usr/bin/env sh,/bin/sh,' samples/swtpm-localca.in

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	EXPECT=/usr/bin/expect \
	NETSTAT=/bin/netstat \
	SOCAT=/usr/bin/socat \
	--disable-silent-rules \
	--disable-static \
	--without-selinux
%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/swtpm/lib*.{la,so}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README TODO
%attr(755,root,root) %{_bindir}/swtpm
%attr(755,root,root) %{_bindir}/swtpm_bios
%attr(755,root,root) %{_bindir}/swtpm_cert
%attr(755,root,root) %{_bindir}/swtpm_cuse
%attr(755,root,root) %{_bindir}/swtpm_ioctl
%attr(755,root,root) %{_bindir}/swtpm_localca
%attr(755,root,root) %{_bindir}/swtpm_setup
%dir %{_libdir}/swtpm
%attr(755,root,root) %{_libdir}/swtpm/libswtpm_libtpms.so.*
%dir %{_datadir}/swtpm
%attr(755,root,root) %{_datadir}/swtpm/swtpm-create-tpmca
%attr(755,root,root) %{_datadir}/swtpm/swtpm-create-user-config-files
%attr(755,root,root) %{_datadir}/swtpm/swtpm-localca
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/swtpm-localca.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/swtpm-localca.options
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/swtpm_setup.conf
%{_mandir}/man8/swtpm.8*
%{_mandir}/man8/swtpm-create-tpmca.8*
%{_mandir}/man8/swtpm-localca.8*
%{_mandir}/man8/swtpm_bios.8*
%{_mandir}/man8/swtpm_cert.8*
%{_mandir}/man8/swtpm_cuse.8*
%{_mandir}/man8/swtpm_ioctl.8*
%{_mandir}/man8/swtpm_localca.8*
%{_mandir}/man8/swtpm_setup.8*
# FIXME: should be man5
%{_mandir}/man8/swtpm-localca.conf.8*
%{_mandir}/man8/swtpm-localca.options.8*
%{_mandir}/man8/swtpm_setup.conf.8*

%files devel
%defattr(644,root,root,755)
%{_includedir}/swtpm
%{_mandir}/man3/swtpm_ioctls.3*
