Name:           sweb
Version:        0.1.0
Release:        1%{?dist}
Summary:        Simple web browser

License:        MIT
URL:            https://github.com/Ad4mCZ/sweb
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel 
BuildRequires:  pyproject-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  python3-poetry-core

Requires:       python3-pyqt6
Requires:       python3-pyqt6-webengine

%description
Web browser designed for ease of use with intention to bridge the gap between senior citizens and technology.


%prep
%autosetup -n %{name}-%{version}

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files sweb
desktop-file-install --dir=%{buildroot}%{_datadir}/applications sweb.desktop
install -Dm644 -t %{buildroot}%{_datadir}/icons/sweb sweb/icons/*
install -Dm644 sweb/config.json -t %{buildroot}%{_sysconfdir}/sweb

%check
export QT_QPA_PLATFORM=offscreen
%pyproject_check_import

%files -f %{pyproject_files}
%{_bindir}/sweb
%{_datadir}/applications/sweb.desktop
%{_datadir}/icons/sweb/*
%{_sysconfdir}/sweb/config.json

%changelog
* Sun Oct 18 2026 vassili
- 
