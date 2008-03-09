#!/opt/local/bin/perl

use Spreadsheet::ParseExcel;
use Data::Dumper;
my $xls = new Spreadsheet::ParseExcel;
my $book = $xls->Parse('/Users/shantanoo/Downloads/Answers.xls') || die(":(((");

for($sheet=0;$sheet<$book->{SheetCount};$sheet++) {
    $wks = $book->{Worksheet}[$sheet];
    my $ques = 1;
    for($iR = $wks->{MinRow}; defined $wks->{MaxRow} && $iR <= $wks->{MaxRow}; $iR++) {
        $data = $wks->{Cells}[$iR][4];
        if($data->{Val} =~ /^[A-Z]$/) {
            $answer->{$sheet}->{$ques} = $data->{Val};
            $ques++;
        }
    }
}

@names = `ls /Users/shantanoo/Downloads/answers`;
chomp @names;
foreach my $name (@names) {
    print "$name\n";
    my $x= calculate($answer, "/Users/shantanoo/Downloads/answers/".$name); 
    foreach $key (sort(keys(%{$x}))) {
        print sprintf ("\t%10s ---> %s\n",$key, $x->{$key});
    }
    print "\n\n";

}

sub calculate {
    my $answers = shift;
    my $file = shift;
    my $xls = new Spreadsheet::ParseExcel;
    my $book = $xls->Parse($file);
    my $score;
    my @sheet_name = qw/Basic Word Excel PowerPoint/;
    my @marks = qw/2 1.5 1.5 2/;
    for($sheet=0;$sheet<$book->{SheetCount};$sheet++) {
        $wks = $book->{Worksheet}[$sheet];
        my $ques = 1;
        for($iR = $wks->{MinRow}; defined $wks->{MaxRow} && $iR <= $wks->{MaxRow}; $iR++) {
            $data = $wks->{Cells}[$iR][4];
            if($data->{Val} =~ /^[A-Z]$/) {
                $score->{$sheet_name[$sheet]} += int($marks[$sheet]) if($answers->{$sheet}->{$ques} eq $data->{Val});
                $ques++;
            }
        }
    }
    $score->{total} += $score->{$sheet_name[$_]} for(0..3);
    return($score);
}
