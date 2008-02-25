#!/usr/bin/perl

use Data::Dumper;
use Getopt::Long;

my ($file, $holidays, $search_name, $days_in_month);

my $buffer_time = 5; # time in mins before late is considered for penalty leave.

sub get_opts {
	&GetOptions('file=s' => \$file, 'holidays=s' => \$holidays, 'name=s' => \$search_name, 'days_in_month=s' => \$days_in_month);
}

# Main Function
get_opts();
open F,"<$file";
my $data;

while(<F>) {
	my $line = $_;
	my $tmp = process_data($_, $search_name);

	$data->{$tmp->{name}}->{half_day}->{count} += $tmp->{half_day}->{count};
	$data->{$tmp->{name}}->{full_day}->{count} += $tmp->{full_day}->{count};
	push @{$data->{$tmp->{name}}->{half_day}->{dates}}, $tmp->{half_day}->{date} if($tmp->{half_day}->{date});
	push @{$data->{$tmp->{name}}->{full_day}->{dates}}, $tmp->{full_day}->{date} if($tmp->{full_day}->{date});
	$data->{$tmp->{name}}->{penalty} += $tmp->{penalty};
	push @{$data->{$tmp->{name}}->{date}}, $tmp->{date};
}
foreach my $name (sort keys(%$data)) {
	next if(!$name);
	print "Name: $name\n";
	print "\tLeave:\n";
	print "\t\tFull Day: $data->{$name}->{full_day}->{count}\n";
	print "\t\tHalf Day: $data->{$name}->{half_day}->{count}\n";
	print "\tDates:\n";
	print "\t\tFull Day: ".join(', ',@{$data->{$name}->{full_day}->{dates}})."\n" if($data->{$name}->{full_day}->{count});
	print "\t\tHalf Day: ".join(', ',@{$data->{$name}->{half_day}->{dates}})."\n" if($data->{$name}->{half_day}->{count});
	print "\tPenalties: $data->{$name}->{penalty}\n";
	print "\tPenalty Leaves (/3): ". int(($data->{$name}->{penalty})/3.0) ."\n";
	my $tmp = calculate_leaves($data->{$name},$holidays, $days_in_month);
	print "\tLeaves (Non-holiday dates when entry was not done):\n";
	print "\t\t$tmp->{month} $tmp->{year}\n";
	print "\t\t".join(", ",@{$tmp->{days}})."\n";
	#print Dumper($data->{$name});
}


sub process_data {
	# body...
	my $retval;
	my $line = shift;
	my $check_name = shift;
	$line =~ s/^\s+|\s+$//g;
	my ($name, $date, $in_time, $out_time, $remark) = split(/,/,$line,5);
	return if($name !~ /$check_name/ && $check_name);

	if($remark =~ /Late In By (\d{2}):(\d{2}):\d{2}/) {
		$time_min = ($1 * 60) + $2;
		if ($time_min >= 30) {
			$retval->{half_day}->{count}++;
			$retval->{half_day}->{date} = $date;
		}
		else {
			$retval->{penalty}++ if($time_min > $buffer_time);
		}
	}
	
	if($remark =~ /Early Out By \-(\d{2}):(\d{2}):\d{2}/){
		$time_min = ($1 * 60) + $2;
		if ($time_min >= 30) {
			$retval->{half_day}->{count}++;
			$retval->{half_day}->{date} = $date;
		} 
		else {
			$retval->{penalty}++ if($time_min > $buffer_time);
		}
	}
	if ($remark =~ /Late In For First Half Leave By (\d{2}):(\d{2}):\d{2}/) {
		
		$time_min = ($1 * 60) + $2;
		if ($time_min >= 30) {
			$retval->{full_day}->{count}++;
			$retval->{full_day}->{date} = $date;
		}
		else {
			$retval->{penalty}++ if($time_min > $buffer_time);
			$retval->{half_day}->{count}++;
			$retval->{half_day}->{date} = $date;
		}		
	}
	if ($remark =~ /Early Out For Second Half Leave By \-(\d{2}):(\d{2}):\d{2}/) {
		$time_min = ($1 * 60) + $2;
		if ($time_min >= 30) {
			$retval->{full_day}->{count}++;
			$retval->{full_day}->{date} = $date;
		}
		else {
			$retval->{penalty}++;
			$retval->{half_day}->{count}++ if($time_min > $buffer_time);
			$retval->{half_day}->{date} = $date;
		}
		
	}
	$retval->{name} = $name;
	$retval->{date} = $date;
	
	return($retval);
}

sub calculate_leaves {
	my ($data_record, $holidays, $days_in_month) = (@_);
	my @tmp;
	my ($day, $mon, $year);
	my $retval;
	for(my $x=1;$x<=int($days_in_month);$x++) {push @tmp, $x;}
	%{$days} = map {$_ => undef} @tmp;
	delete $days->{$_} for(split(/,/,$holidays));
	foreach my $date (@{$data_record->{date}}) {
		($day, $mon, $year) = split('-', $date);
		delete $days->{int($day)};
	}
	@{$retval->{days}} = keys(%{$days});
	$retval->{month} = $mon;
	$retval->{year} = $year;
	return($retval);
	
}


