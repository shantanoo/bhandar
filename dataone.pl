#!/usr/bin/perl

use lib '/opt/local/lib/perl5/vendor_perl';
use WWW::Mechanize;
use Getopt::Long;
use Data::Dumper;

&GetOptions('u=s'=>\$user,'p=s'=>\$passwd,'mon=s'=>\$mon,'year=s'=>\$yr,'o=s'=>\$outfile);
$mon = uc($mon);
if(!$user || !$passwd || !$mon || !$yr) {
    print "Usage: $0 -u <username> -p <password> -mon <month> -year <year>\n";
    print "\tWhere,\n";
    print "\t\t<username> = BSNL Portail ID\n";
    print "\t\t<password> = Password\n";
    print "\t\t<month> = 3 letter abbrevation of month. e.g. JAN\n";
    print "\t\t<year> = Year\n";
    exit(1);
}
if($outfile) {
    open F,">$outfile" || die("Unable to open file $outfile\n");
} else {
    open F,">&STDOUT";
}
my $m = WWW::Mechanize->new();
$m->post('http://p3hosting.bsnl.in:9080/BroadBandCustomerPortal/UserAuthenticationController',['adminid'=>$user, 'password'=>$passwd]);
$m->get('http://p3hosting.bsnl.in:9080/BroadBandCustomerPortal/UsageDetails.jsp?h1=&mon='.$mon.'-'.$yr);
print F $m->content;