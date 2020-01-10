Name:           virt-v2v
Version:        0.9.1
Release:        4%{?dist}%{?extra_release}
Summary:        Convert a virtual machine to run on KVM

Group:          Applications/System
License:        GPLv2+ and LGPLv2+
URL:            http://git.fedorahosted.org/git/virt-v2v.git
Source0:        https://fedorahosted.org/releases/v/i/virt-v2v/%{name}-v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Windows dependencies
# Taken from the RHEV Tools CD
# N.B. Old tools are supported on new RHEV, but not vice-versa. Don't upgrade
# this blindly! The tool will automatically update itself.
Source1:        RHEV-Application_Provisioning_Tool_46267.exe

# The source of rhsrvany
# rhsrvany is included in upstream virt-v2v as a git submodule. It doesn't
# currently have a functioning upstream or any releases. Wherever possible, We
# export patches for RHEL from upstream git. However, as rhsrvany has been added
# as a submodule, a patch doesn't work. We therefore include an exported tarball
# of the rhsrvany source at the relevant commit.
#
# This tarball has been created from a development source tree as follows:
# 1. (cd rhsrvany && git clean -xdf)
# 2. ./Build rhsrvany_conf
# 3. tar zcvf rhsrvany-<commit>.tar.gz rhsrvany/ --exclude .git
Source2:        rhsrvany-9cb29d2b.tar.gz

# Backported upstream patches
# Naming scheme: <name>-<version>-<local sequence number>-<git commit>.patch
#  name:         virt-v2v
#  version:      the version of virt-v2v the patch was originally rebased to
#  local seq no: the order the patches should be applied in
#  git commit:   the first 8 characters of the git commit hash

# fe42743 Windows: Upload virtio drivers in _prepare_virtio_drivers
Patch0:   virt-v2v-0.9.1-00-fe42743.patch

# 960a68f Windows: Disable the rhelscsi service
Patch1:   virt-v2v-0.9.1-01-960a68f.patch

# 2b39118 Windows: Make firstboot a dynamically-generated script
Patch2:   virt-v2v-0.9.1-02-2b39118.patch

# fd09aa8 Windows: Uninstall Xen PV driver on first boot
Patch3:   virt-v2v-0.9.1-03-fd09aa8.patch

# 8c00f13 Windows: Remove firstboot.bat
Patch4:   virt-v2v-0.9.1-04-8c00f13.patch

# 5b61f97 build: Add missing return 0 to ACTION_po
Patch5:   virt-v2v-0.9.1-05-5b61f97.patch

# fbe13fc build: Use preferred Module::Build->do_system in favour of system()
Patch6:   virt-v2v-0.9.1-06-fbe13fc.patch

# 23f1a36 build: Make syntaxcheck handle files with dos line endings
Patch7:   virt-v2v-0.9.1-07-23f1a36.patch

# 988f67a build: Create new submodules target to initialise git submodules
Patch8:   virt-v2v-0.9.1-08-988f67a.patch

# 49488e7 build: Build rhsrvany from source (MODIFIED PATCH)
Patch9:   virt-v2v-0.9.1-09-49488e7.patch

# 6bc7fd08 Don't allow creation of guests which don't use either raw or qcow2
Patch10:  virt-v2v-0.9.1-10-6bc7fd08.patch

# Unfortunately, despite really being noarch, we have to make virt-v2v arch
# dependent to avoid build failures on architectures where libguestfs isn't
# available.
%if 0%{?rhel} >= 6
ExclusiveArch:  x86_64
%else
ExclusiveArch:  %{ix86} x86_64
%endif

# Build system direct requirements
BuildRequires:  gettext
BuildRequires:  perl
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Module::Find)

# Runtime perl modules also required at build time for use_ok test
BuildRequires:  perl(Archive::Extract)
BuildRequires:  perl(DateTime)
BuildRequires:  perl(Digest::SHA1)
BuildRequires:  perl(IO::String)
BuildRequires:  perl(Locale::TextDomain)
BuildRequires:  perl(Module::Pluggable)
BuildRequires:  perl(Net::HTTPS)
BuildRequires:  perl(Net::SSL)
BuildRequires:  perl(Sys::Syslog)
BuildRequires:  perl(Sys::Virt)
BuildRequires:  perl(Term::ProgressBar)
BuildRequires:  perl(URI)
BuildRequires:  perl(XML::DOM)
BuildRequires:  perl(XML::DOM::XPath)

BuildRequires:  perl-Sys-Guestfs >= 1:1.14.0
BuildRequires:  perl-hivex >= 1.2.2

# For building rhsrvany
BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-gcc

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Required for the name optional argument to add_drive_opts
Requires:       perl-Sys-Guestfs >= 1:1.14.0

# Undocumented from antiquity
Requires:       perl-hivex >= 1.2.2

# Required for passing flags to get_xml_description
Requires:       perl(Sys::Virt) >= 0.2.4

# Net::SSL and Net::HTTPS are loaded with require rather than use, which
# rpmbuild doesn't seem to discover automatically.
Requires:       perl(Net::SSL)
Requires:       perl(Net::HTTPS)

# Need >= 0.8.1 for rpc fix talking to RHEL 5 libvirt
Requires:       libvirt >= 0.8.1

# For GuestOS transfer image
Requires:       /usr/bin/mkisofs

# For guest image inspection
Requires:       /usr/bin/qemu-img

# For ssh transfers
Requires:       /usr/bin/ssh

# For libguestfs built with mdadm_conf lens
Requires:     libguestfs >= 1.16.19-1.el6


%description
virt-v2v is a tool for converting and importing virtual machines to
libvirt-managed KVM, or Red Hat Enterprise Virtualization. It can import a
variety of guest operating systems from libvirt-managed hosts and VMware ESX.


%prep
%setup -q -n %{name}-v%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

# If we handled git's diff format correctly, this would be deleted by Patch9
rm windows/rhsrvany.exe

# Patch9 adds rhsrvany as a submodule. The contents of the submodule are
# contained in this tarball.
rm rhsrvany
tar zxvf %{SOURCE2}

%build
%{__perl} Build.PL
./Build
./Build rhsrvany

# perl doesn't need debuginfo
%define debug_package %{nil}


%install
rm -rf %{buildroot}
./Build install \
    --destdir %{buildroot} \
    --installdirs vendor \
    --install_path locale=%{_datadir}/locale \
    --install_path confdoc=%{_mandir}/man5

# Create lib directory, used for holding software to be installed in guests
statedir=%{buildroot}%{_localstatedir}/lib/virt-v2v
mkdir -p $statedir/software

# Copy Windows dependencies into place
windir=$statedir/software/windows
mkdir -p $windir

# firstboot.bat expects the RHEV APT installer to be called rhev-apt.exe
cp %{SOURCE1} $windir/rhev-apt.exe

# Copy built rhsrvany.exe into place. There's no need for it to be executable
cp rhsrvany/RHSrvAny/rhsrvany.exe $windir/
chmod 0644 $windir/rhsrvany.exe

mkdir -p %{buildroot}%{_sysconfdir}
cp v2v/virt-v2v.conf %{buildroot}%{_sysconfdir}/
cp v2v/virt-v2v.db $statedir/

%find_lang %{name}

# Not clear why this is being created as there is nothing arch-specific in
# virt-v2v. It isn't packaged, though, so we need to delete it.
[ -d "%{buildroot}/%{perl_archlib}" ] &&
  find %{buildroot}/%{perl_archlib} -name .packlist -type f | xargs rm


%check
./Build test


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)

%doc TODO.txt
%doc META.yml
%doc ChangeLog
%doc COPYING COPYING.LIB

# For noarch packages: vendorlib
%{perl_vendorlib}/*

# Man pages
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man5/*.5*

# Executables
%attr(0755,root,root) %{_bindir}/virt-v2v
%attr(0755,root,root) %{_bindir}/virt-p2v-server

%dir %{_localstatedir}/lib/virt-v2v

%config(noreplace) %{_sysconfdir}/virt-v2v.conf
%config %{_localstatedir}/lib/virt-v2v/virt-v2v.db
%config(noreplace) %{_localstatedir}/lib/virt-v2v/software


%changelog
* Wed Oct 23 2013 Matthew Booth <mbooth@redhat.com> - 0.9.1-4
- Improved error message on unsupported target disk format (RHBZ#956580)

* Wed Sep  4 2013 Matthew Booth <mbooth@redhat.com> - 0.9.1-3
- Fix permissions on rhsrvany.exe

* Tue Sep  3 2013 Matthew Booth <mbooth@redhat.com> - 0.9.1-2
- Fix BSOD converting Windows guest with Xen PV drivers (RHBZ#809273)
- Build rhsrvany from source (RHBZ#1003058)

* Wed Jun 12 2013 Matthew Booth <mbooth@redhat.com> - 0.9.1-1
- Rebase to new upstream release

* Mon Oct 22 2012 Matthew Booth <mbooth@redhat.com> - 0.8.9-2
- Fix creation of /Temp/V2V (RHBZ#868073)
- Fix output to RHEV (RHBZ#868129)
- Clean RPM database before any rpm operations
- Fix update of xvc0 to ttyS0 in securetty
- Fix guestfs launch failure doing format conversion with libvirtxmlguest
  (RBBZ#868405)

* Wed Oct 17 2012 Matthew Booth <mbooth@redhat.com> - 0.8.9-1
- Update to new upstream release
- Don't warn on unknown floppy devices (RHBZ#794680)
- Create disks with cache=none on libvirt (RHBZ#838057)

* Wed May  2 2012 Matthew Booth <mbooth@redhat.com> - 0.8.7-6
- Disable accidentally-enabled debugging in p2v-server (RHBZ#817062)

* Fri Apr 20 2012 Matthew Booth <mbooth@redhat.com> - 0.8.7-5
- Disable serial console when converting to RHEV (RHBZ#785235)
- Improve error detection in p2v-server
- Replace augeas-libs dependency with libguestfs dependency for mdadm_conf lens

* Wed Mar  7 2012 Matthew Booth <mbooth@redhat.com> - 0.8.7-4
- Fix DNS when running network commands (RHBZ#800353)

* Mon Mar  5 2012 Matthew Booth <mbooth@redhat.com> - 0.8.7-3
- Fix warning starting virt-p2v-server (RHBZ#799869)

* Mon Mar  5 2012 Matthew Booth <mbooth@redhat.com> - 0.8.7-2
- Re-add accidentally removed versioned augeas-libs dependency

* Fri Mar  2 2012 Matthew Booth <mbooth@redhat.com> - 0.8.7-1
- New upstream version

* Fri Sep 16 2011 Matthew Booth <mbooth@redhat.com> - 0.8.3-5
- Fix regression when converting Win7 32 bit to RHEV (RHBZ#738236)

* Fri Aug 26 2011 Matthew Booth <mbooth@redhat.com> - 0.8.3-4
- Fix failure to convert a libvirt guest with no <graphics> element

* Thu Aug 25 2011 Matthew Booth <mbooth@redhat.com> - 0.8.3-3
- Add missing dependency on new Sys::Virt

* Thu Aug 25 2011 Matthew Booth <mbooth@redhat.com> - 0.8.3-2
- Fix for CVE-2011-1773
- Document limitations wrt Windows Recovery Console

* Wed Aug 17 2011 Matthew Booth <mbooth@redhat.com> - 0.8.3-1
- Include missing virt-v2v.db
- Rebase to upstream release 0.8.3

* Wed Aug 10 2011 Matthew Booth <mbooth@redhat.com> - 0.8.2-2
- Split configuration into /etc/virt-v2v.conf and /var/lib/virt-v2v/virt-v2v.db
- Improve usability as non-root user (RHBZ#671094)
- Update man pages to use -os as appropriate (RHBZ#694370)
- Warn if user specifies both -n and -b (RHBZ#700759)
- Fix cleanup when multiboot OS is detected (RHBZ#702007)
- Ensure the cirrus driver is installed if required (RHBZ#708961)
- Remove unnecessary dep on perl(IO::Handle)
- Fix conversion of xen guests using aio storage backend.
- Suppress warning for chainloader grub entries.
- Only configure a single scsi_hostadapter for converted VMware guests.

* Mon Jul 25 2011 Matthew Booth <mbooth@redhat.com> - 0.8.2-1
- Rebase to upstream release 0.8.2

* Fri Feb 25 2011 Matthew Booth <mbooth@redhat.com> - 0.7.1-4
- Fix detection of Windows XP Pro x64 (RHBZ#679017)
- Fix error message when converting Red Hat Desktop (RHBZ#678950)

* Fri Feb 11 2011 Matthew Booth <mbooth@redhat.com> - 0.7.1-3
- Add virt-v2v-0.7.1-04-caa73b27-rebased.patch (RHBZ#676553)
- Add virt-v2v-0.7.1-05-e0350878.patch (RHBZ#676323)

* Wed Feb  2 2011 Matthew Booth <mbooth@redhat.com> - 0.7.1-2
- Updated translations for nl, pl and it
- Require latest augeas (RHBZ#609448)
- Uninstall VMware Tools installed from tarball (RHBZ#623571)
- Remove obsolete BuildRequires perl(LWP::UserAgent)

* Wed Jan 26 2011 Matthew Booth <mbooth@redhat.com> - 0.7.1-1
- Rebase to upstream version 0.7.1

* Mon Jan 17 2011 Matthew Booth <mbooth@redhat.com> - 0.7.0-1
- Rebase to upstream version 0.7.0

* Thu Aug 19 2010 Matthew Booth <mbooth@redhat.com> - 0.6.2-4
- Fix copying of VirtIO drivers during Windows conversion (RHBZ#615981)

* Wed Aug 18 2010 Matthew Booth <mbooth@redhat.com> - 0.6.2-3
- Replace rhev-apt.exe, rhsrvany.exe and firstboot.bat (RHBZ#617635)
- Enable virt-v2v to run under a restrictive umask (RHBZ#624963)
- Identify RHEL 6 as OtherLinux when converting to RHEV (RHBZ#625041)

* Tue Aug 17 2010 Matthew Booth <mbooth@redhat.com> - 0.6.2-2
- Prevent Windows from replacing VirtIO with incorrect driver (RHBZ#615981)
- Remove bundled Windows VirtIO drivers (RHBZ#617635)
- Update License tag to reflect removal of proprietary drivers

* Tue Aug 10 2010 Matthew Booth <mbooth@redhat.com> - 0.6.2-1
- Rebase to new upstream version 0.6.2

* Fri Jul 23 2010 Richard W.M. Jones <rjones@redhat.com> - 0.6.1-2
- Update License tag to note that Windows drivers are distributed under
  a non-free Red Hat Proprietary license.
- Include license text next to the drivers *and* in the documentation
  directory.
- Remove .packlist files from Perl libdirs.

* Tue Jun 22 2010 Matthew Booth <mbooth@redhat.com> - 0.6.1-1
- Update to release 0.6.1 (RHBZ#558755)

* Wed May 19 2010 Richard W.M. Jones <rjones@redhat.com> - 0.5.4-1
- Update RHEL-6 branch to release 0.5.4, from RHEL-5-V2V (RHBZ#558755).

* Fri Jan 22 2010 Matthew Booth <mbooth@redhat.com> - 0.2.0-2
- Change arch to x86_64 to prevent building where qemu isn't available.

* Tue Sep 15 2009 Matthew Booth <mbooth@redhat.com> - 0.2.0-1
- Update to release 0.2.0

* Tue Sep  1 2009 Matthew Booth <mbooth@redhat.com> - 0.1.0-1
- Initial specfile
