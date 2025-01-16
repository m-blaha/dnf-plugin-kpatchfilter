Name:           dnf-plugin-kpatchfilter
Version:        1.0.0
Release:        1%{?dist}
Summary:        Filter out kernel-core package versions not supported by kpatch

License:        GPL-2.0-or-later
URL:            https://github.com/m-blaha/%{name}
Source0:        %{url}/archive/v%{version}-pre/%{name}-%{version}-pre.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  cmake

Requires:       python3-dnf
Requires:       python3-dnf-plugins-core

Provides:       dnf-plugin-versionlock = %{version}-%{release}

%description
Dnf plugin to filter out kernel-core package versions not supported by kpatch.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%{python3_sitelib}/dnf-plugins/kpatchfilter.py
%{python3_sitelib}/dnf-plugins/__pycache__/kpatchfilter.*
%config(noreplace) %{_sysconfdir}/dnf/plugins/kpatchfilter.conf

%changelog

