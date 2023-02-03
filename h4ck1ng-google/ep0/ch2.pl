#!/bin/perl

# Useful resource: https://www.shlomifish.org/lecture/Perl/Newbies/lecture4/processes/opens.html

# Testing out open() command execution vulnerability
open(my $fh, "./temp.txt; ls -al; cat temp.txt |");
while (my $line = <$fh>) {
    print $line
}
print("File opened");

# ; ls /; cat /flag | 
# ; cat /flag; ls /; |
