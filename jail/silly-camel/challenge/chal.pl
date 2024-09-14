#!/usr/local/bin/perl
select(STDOUT); $| = 1;

print "funny > ";
my $code = <STDIN>;
chomp $code;
close STDIN;

if ($code =~ /[\$\@\%'"`a-z]/i) {
    print "Not funny...\n";
    exit 1;
}

eval $code;