#!/usr/bin/perl
#Simply put, the .apply function in pandas acts pretty slowly to generate one new column based on 4 existing ones.
#Perl can add this to the file much more simply. Really. And then it's done.
#perl -MMath::Trig -e '$_=<>;s/.$/, trip_latlon_distance$&/;print;sub hvsn{my($t1,$n1,$t2,$n2)=map(deg2rad($_), @_);return 3960*2*asin(sqrt(sin(($t2-$t1)/2)**2+cos($t1)*cos($t2)*sin(($n2-$n1)/2)**2));}while(<>){my @row=split(/,/);my $miles=hvsn(@row[10..13]);s/.$/,$miles$&/;print}' trip_data_3.csv > trip_data_3_trip_latlon_dist.csv

use Math::Trig;
$_=<>; # Modify the header row
s/.$/, trip_latlon_distance$&/;
print;
sub hvsn{ # t:lat n:long
    my ($t1, $n1, $t2, $n2) = map(deg2rad($_), @_);
    return 3960 * 2 * asin(sqrt(
        sin( ($t2 - $t1) / 2 )**2 +
        cos($t1) * cos($t2) *
        sin( ($n2 - $n1) / 2 )**2
        ));
}
while(<>){ # Modify each data row
    my @row = split(/,/);
    my $miles = hvsn(@row[10..13]);
    s/.$/,$miles$&/;
    print
}
