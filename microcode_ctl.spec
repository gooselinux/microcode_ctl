Summary:        Tool to update x86/x86-64 CPU microcode.
Name:           microcode_ctl
Version:        1.17
Release:        3%{?dist}
Epoch:          1
Group:          System Environment/Base
License:        GPLv2+
URL:            http://www.urbanmyth.org/microcode/
Source0:        http://www.urbanmyth.org/microcode/microcode_ctl-%{version}.tar.gz
Source1:        microcode_ctl.init
# Microcode now distributed directly by Intel, at
# http://downloadcenter.intel.com (just search for microcode)
Source2:        microcode-20100209.dat
Buildroot:      %{_tmppath}/%{name}-%{version}-root
Requires(pre):  /sbin/chkconfig /sbin/service
Requires(pre):  grep gawk coreutils
Obsoletes:      kernel-utils
ExclusiveArch:  %{ix86} x86_64

Patch1: microcode_ctl.patch

%description
microcode_ctl - updates the microcode on Intel x86/x86-64 CPU's

%prep
%setup -q
%patch1 -p1

%build
make CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/usr/share/man/man{1,8}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig

make DESTDIR=%{buildroot} PREFIX=%{_prefix} \
     INSDIR=/sbin MANDIR=%{_mandir}/man8 RCDIR=%{_sysconfdir} install clean

install %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/microcode_ctl
install -m 644 %{SOURCE2} %{buildroot}/lib/firmware/microcode.dat

chmod -R a-s %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_sysconfdir}/init.d/microcode_ctl
/lib/firmware/*
/sbin/microcode_ctl
%attr(0644,root,root) %{_mandir}/*/*



%preun
if [ "$1" = "0" ] ; then
    /sbin/chkconfig --del microcode_ctl
fi

%post
# Only enable on Intel 686's and above.
vendor=`cat /proc/cpuinfo | grep "^vendor_id" | sort -u | awk -F ": " '{ print $2 }'`
[ "$vendor" != "GenuineIntel" ] && exit 0
family=`cat /proc/cpuinfo | grep "^cpu family" | sort -u | awk -F ": " '{ print $2 }'`
[ $family -lt 6 ] && exit 0
/sbin/chkconfig --add microcode_ctl

%triggerpostun -- kernel-utils
# Only enable on Intel 686's and above.
vendor=`cat /proc/cpuinfo | grep "^vendor_id" | sort -u | awk -F ": " '{ print $2 }'`
[ "$vendor" != "GenuineIntel" ] && exit 0
family=`cat /proc/cpuinfo | grep "^cpu family" | sort -u | awk -F ": " '{ print $2 }'`
[ $family -lt 6 ] && exit 0
/sbin/chkconfig --add microcode_ctl
exit 0

%changelog
* Tue Feb 23 2010 Anton Arapov <anton@redhat.com> - 1:1.17-3
- Update to microcode-20100209.dat [488319]

* Fri Feb 19 2010 Kyle McMartin <kyle@redhat.com> - 1:1.17-2
- Don't use a CVS release for RHEL, otherwise it'll always be a branch
  and irritating.
- Fix syntax error in microcode_ctl.init.
- Resolves: rhbz#552246.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1:1.17-1.41.1
- Rebuilt for RHEL 6

* Wed Sep 30 2009 Dave Jones <davej@redhat.com>
- Update to microcode-20090927.dat

* Fri Sep 11 2009 Dave Jones <davej@redhat.com>
- Remove some unnecessary code from the init script.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-1.52.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 25 2009 Dave Jones <davej@redhat.com>
- Shorten sleep time during init.
  This really needs to be replaced with proper udev hooks, but this is
  a quick interim fix.

* Wed Jun 03 2009 Kyle McMartin <kyle@redhat.com> 1:1.17-1.50
- Change ExclusiveArch to i586 instead of i386. Resolves rhbz#497711.

* Wed May 13 2009 Dave Jones <davej@redhat.com>
- update to microcode 20090330

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-1.46.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 12 2008 Dave Jones <davej@redhat.com>
- update to microcode 20080910

* Tue Apr 01 2008 Jarod Wilson <jwilson@redhat.com>
- Update to microcode 20080401

* Sat Mar 29 2008 Dave Jones <davej@redhat.com>
- Update to microcode 20080220
- Fix rpmlint warnings in specfile.

* Mon Mar 17 2008 Dave Jones <davej@redhat.com>
- specfile cleanups.

* Fri Feb 22 2008 Jarod Wilson <jwilson@redhat.com>
- Use /lib/firmware instead of /etc/firmware

* Wed Feb 13 2008 Jarod Wilson <jwilson@redhat.com>
- Fix permissions on microcode.dat

* Thu Feb 07 2008 Jarod Wilson <jwilson@redhat.com>
- Spec cleanup and macro standardization.
- Update license
- Update microcode data file to 20080131 revision.

* Mon Jul  2 2007 Dave Jones <davej@redhat.com>
- Update to upstream 1.17

* Thu Oct 12 2006 Jon Masters <jcm@redhat.com>
- BZ209455 fixes.

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Fri Jun 16 2006 Bill Nottingham <notting@redhat.com>
- remove kudzu requirement
- add prereq for coreutils, awk, grep

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Fri Jan 27 2006 Dave Jones <davej@redhat.com>
- Update to upstream 1.13

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 14 2005 Dave Jones <davej@redhat.com>
- initscript tweaks.

* Tue Sep 13 2005 Dave Jones <davej@redhat.com>
- Update to upstream 1.12

* Wed Aug 17 2005 Dave Jones <davej@redhat.com>
- Check for device node *after* loading the module. (#157672)

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Thu Feb 17 2005 Dave Jones <davej@redhat.com>
- s/Serial/Epoch/

* Tue Jan 25 2005 Dave Jones <davej@redhat.com>
- Drop the node creation/deletion change from previous release.
  It'll cause grief with selinux, and was a hack to get around
  a udev shortcoming that should be fixed properly.

* Fri Jan 21 2005 Dave Jones <davej@redhat.com>
- Create/remove the /dev/cpu/microcode dev node as needed.
- Use correct path again for the microcode.dat.
- Remove some no longer needed tests in the init script.

* Fri Jan 14 2005 Dave Jones <davej@redhat.com>
- Only enable microcode_ctl service if the CPU is capable.
- Prevent microcode_ctl getting restarted multiple times on initlevel change (#141581)
- Make restart/reload work properly
- Do nothing if not started by root.

* Wed Jan 12 2005 Dave Jones <davej@redhat.com>
- Adjust dev node location. (#144963)

* Tue Jan 11 2005 Dave Jones <davej@redhat.com>
- Load/Remove microcode module in initscript.

* Mon Jan 10 2005 Dave Jones <davej@redhat.com>
- Update to upstream 1.11 release.

* Sat Dec 18 2004 Dave Jones <davej@redhat.com>
- Initial packaging, based upon kernel-utils.

