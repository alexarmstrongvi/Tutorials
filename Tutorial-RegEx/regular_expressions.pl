#!/usr/bin/env perl
use strict;
use warnings;
use Test::Simple tests => 8;

# References
# https://perldoc.perl.org/perlintro
# https://perldoc.perl.org/perlretut
# https://metacpan.org/pod/distribution/Test-Simple/lib/Test/Tutorial.pod

print "===== Running regular_expressions.pl =====\n";

my @matches;
my $string;
my $pattern;
################################################################################
# Perl RegExp Basics
################################################################################
ok("Match this" =~ /this/);
ok("Match this" !~ /that/);

# Using variables
$string = "Match this";
$pattern = 'this';
ok($string =~ /$pattern/);

# Special default variable $_
$_ = "Match this";
# ok(/$pattern/);

# Extracting matches
@matches = ("Match this" =~ /(this)/);
ok("$matches[0]" eq "this");

@matches = ("123" =~ /((1)(2)(3))/);
my @sol = ("1","2","3");
ok($matches[0] eq "123");
ok($matches[1] eq "1");
ok($matches[2] eq "2");
ok($matches[3] eq "3");

################################################################################


################################################################################
print "...DONE!\n\n";

exit(0);