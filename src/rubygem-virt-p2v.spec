# Automatically generated by rubygem-virt-p2v.spec.PL
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname virt-p2v
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"]')}

%global rubyabi 1.8

Name:           rubygem-virt-p2v
Version:        0.8.7
Release:        1%{?dist}%{?extra_release}
Summary:        Send a machine's storage and metadata to virt-p2v-server

Group:          Applications/System
License:        GPLv2+ and LGPLv2+
URL:            http://git.fedorahosted.org/git/virt-v2v.git
Source0:        https://fedorahosted.org/releases/v/i/virt-v2v/virt-v2v-v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Backported upstream patches
# Naming scheme: <name>-<version>-<local sequence number>-<git commit>.patch
#  name:         virt-v2v
#  version:      the version of virt-v2v the patch was originally rebased to
#  local seq no: the order the patches should be applied in
#  git commit:   the first 8 characters of the git commit hash

# We only build virt-p2v for i686 as we need it to run on the widest possible
# set of hardware from a single boot image.
ExclusiveArch:  i686

BuildRequires:  perl(Module::Build)

BuildRequires:  rubygems
BuildRequires:  rubygem(rake)
BuildRequires:  ruby-devel

# rblibssh2 dependencies
BuildRequires:  libssh2-devel

Requires:   ruby(abi) = %{rubyabi}
Requires:   rubygems
Requires:   rubygem(gtk2)
Requires:   ruby(dbus)

Requires:   /sbin/blockdev
Requires:   /usr/bin/hwloc-info
Requires:   NetworkManager
Requires:   /usr/bin/openvt

Provides:   rubygem(%{gemname}) = %{version}


%description
virt-p2v is a client which connects to a virt-p2v-server and transfer's the host
machine's storage and metadata. virt-p2v is intended to be run from a live
image, so it is unlikely you want to install it directly.


%package doc
Summary:    Documentation for %{name}
Group:      Documentation
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}


%description doc
Documentation for %{name}


%package -n virt-p2v-image-builder
Summary:    Create a virt-p2v bootable image
BuildArch:  noarch

# image builder script requires
Requires:   /usr/bin/ksflatten
Requires:   /usr/sbin/setenforce
Requires:   /usr/bin/livecd-creator

# Kickstart nochroot scripts requires
Requires:   /usr/bin/livecd-iso-to-disk
Requires:   /usr/bin/livecd-iso-to-pxeboot
Requires:   /usr/bin/image-minimizer


%description -n virt-p2v-image-builder
virt-p2v-image-builder is a tool to create a bootable virt-p2v live image.


%prep
%setup -q -n virt-v2v-v%{version}


%build
# Need this to pull the version number out
%{__perl} Build.PL

pushd p2v/client
rake gem
popd

mkdir -p .%{gemdir}
export CONFIGURE_ARGS="--with-cflags='%{optflags}' --with-ldflags='%{optflags}'"
gem install --local --install-dir .%{gemdir} \
            --force -V --rdoc p2v/client/pkg/%{gemname}-%{version}.gem


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{gemdir} %{buildroot}%{ruby_sitearch}
cp -a .%{gemdir}/* %{buildroot}%{gemdir}/

mv %{buildroot}%{geminstdir}/ext/rblibssh2/rblibssh2.so \
   %{buildroot}%{ruby_sitearch}
rm -rf %{buildroot}%{geminstdir}/ext \
       %{buildroot}%{geminstdir}/lib/rblibssh2.so

mv %{buildroot}%{gemdir}/bin/* %{buildroot}%{_bindir}
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

cp COPYING %{buildroot}/%{geminstdir}

# Install p2v-image-builder
%global builderdir %{_datadir}/virt-p2v-image-builder
builder=%{buildroot}/%{_bindir}/virt-p2v-image-builder
mkdir -p %{buildroot}%{builderdir}
cp p2v/image-builder/*.ks %{buildroot}%{builderdir}
cp p2v/image-builder/virt-p2v-image-builder $builder

# Set the default data directory
sed -i -e 's,^DEFAULT_DATADIR=.*,DEFAULT_DATADIR=%{builderdir},' $builder


%check
pushd p2v/client
# No tests yet
#rake test
popd


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, -)
%{_bindir}/virt-p2v
%{_bindir}/virt-p2v-launcher
%dir %{geminstdir}
%{geminstdir}/bin
%{geminstdir}/lib
%doc %{geminstdir}/COPYING
%doc %{geminstdir}/Manifest
%doc %{geminstdir}/Rakefile
%doc %{geminstdir}/%{gemname}.gemspec
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%{ruby_sitearch}/rblibssh2.so


%files doc
%defattr(-, root, root, -)
%{gemdir}/doc/%{gemname}-%{version}


%files -n virt-p2v-image-builder
%defattr(-, root, root, -)
%attr(0755, root, root) %{_bindir}/virt-p2v-image-builder
%{builderdir}


%changelog
