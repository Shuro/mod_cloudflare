Name:		mod_cloudflare
Version:	1.1.1
Release:	1%{?dist}
Summary:	CloudFlare Apcahe module mod_cloudflare to show visitor IPs in logs.

Group:		System Environment/Daemons
License:	ASL-2.0
URL:		http://www.cloudflare.com/
Source0:	https://raw.github.com/cloudflare/mod_cloudflare/master/mod_cloudflare.c
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	httpd-devel
Requires:	httpd

%description
CloudFlare acts as a proxy, which means that your visitors are routed through
the CloudFlare network and you do not see their original IP address. This
module uses HTTP headers provided by the CloudFlare proxy to log the real IP
address of the visitor.
Based on mod_remoteip.c, this apache extension will replace the
remote_ip variable in user's logs with the correct remote_ip sent
from CloudFlare. This also does authentication, only performing
the switch for requests originating from CloudFlare IPs.

%prep
%setup -c -T
cp %{SOURCE0}  .
cat > cloudflare.conf <<EOF
LoadModule cloudflare_module modules/mod_cloudflare.so
<IfModule mod_cloudflare.c>
	CloudFlareRemoteIPHeader CF-Connecting-IP
	CloudFlareRemoteIPTrustedProxy 204.93.240.0/24 204.93.177.0/24 199.27.128.0/21 173.245.48.0/20 103.22.200.0/22 141.101.64.0/18 108.162.192.0/18
	#DenyAllButCloudFlare
</IfModule>
EOF

%build
apxs -c mod_cloudflare.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/httpd/modules
install -m 755 .libs/mod_cloudflare.so %{buildroot}%{_libdir}/httpd/modules/mod_cloudflare.so
install -d %{buildroot}%{_sysconfdir}/httpd/conf.d
install -m 644 cloudflare.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/cloudflare.conf

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_libdir}/httpd/modules/mod_cloudflare.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/cloudflare.conf

%changelog
* Sun Jun 03 2012 CloudFlare <info@cloudflare.com> [1.1.1-1]
- Bugfix: Corrected behaviour when CloudFlareRemoteIPHeader is not set and
  DenyAllButCloudFlare is enabled. Will now deny.

* Sun May 20 2012 CloudFlare <info@cloudflare.com> [1.1.0-1]
- Initial offical package release.

* Mon Feb 27 2012 Alex Headley <aheadley@nexcess.net> [1.0.2-3]
- use _sysconfdir instead of /etc
- add config directive examples to config file and change config file generation

* Thu Jan 26 2012 Corey Henderson <corman@cormander.com> [1.0.2-2.el6]
- use _libdir macro instead of /usr/lib
- cloudflare.conf is small enough to not need a source file

* Wed Jan 18 2012 Corey Henderson <corman@cormander.com> [1.0.2-1.el6]
- Initial build.

