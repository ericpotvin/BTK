Name:       BTK
Version:    1
Release:    0.0
Summary:    Bash ToolKit - UnitTests and Code Coverage tools
License:    MIT
Group:      btk
Source0:    btk.tar.gz

BuildArch:  noarch

Requires:   python

%description
Bash ToolKit: Test your code and create Code Coverage for it!

%prep
%setup -q -n btk

%build
# %%configure
# %%make %{?_smp_mflags}

%install
install -m 0755 -d $RPM_BUILD_ROOT/opt/btk
install -m 0755 -d $RPM_BUILD_ROOT/usr/share/btk/
install -m 0755 -d $RPM_BUILD_ROOT/%{_bindir}

# %%  copy files
cp -a bin/* $RPM_BUILD_ROOT/%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT/opt/btk/
cp -a html/* $RPM_BUILD_ROOT/usr/share/btk/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir /opt/btk
%dir /usr/share/btk/
/opt/btk/*
/usr/share/btk/*
%{_bindir}/btk*
