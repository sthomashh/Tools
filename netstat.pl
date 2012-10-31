#! /usr/bin/perl 
$|=1;
$flag = $ARGV[0];
#print $flag."\n";
if($flag eq "") {$flag = 'vne';}
$zusatz = '|grep -v 127.0.0.1|grep -v 192.168';
$aufruf = '/bin/netstat -'.$flag.$zusatz;
#print $aufruf."\n";

$max_load = 0.0;
while(true)
{
	#$cmd = `$aufruf`;
	#$cmd =~ s/\n+/\#/g;
	#$cmd =~ s/\t+/|/g;
	#$cmd =~ s/\s+/|/g;
	#$cmd =~ s/.+State\|Benutzer\|Inode\|(tcp.+)|\#Aktive\|Sockets\|.+$/$1/ig;
	#$cmd =~ s/^(.+tcp.+)\|\#Aktive\|Sockets\|.+$/$1/ig;

	$cmd .= "\n===================================================================================================\n";
	#Anzahl Internetzugriffe ermitteln
	#@a_anz = split(/#tcp/, $cmd);
	#$cmd .= $#a_anz.' Verbindungen';
	$cmd = "";
	#Load Average dazuschreiben
	$cmd3 = `w -s`;
	$cmd3 =~ s/\t+//g;
	$cmd3 =~ s/\s+//g;
	$cmd3 =~ s/\n+//g;
	$cmd3 =~ s/.+loadaverage:(\d+\.\d\d),.+$/$1/ig;
	$load = $cmd3;
	if($load>$max_load){
		$max_load = $load;
	}
	$cmd .= ' ** Max Load Average: '.$max_load;
	$cmd .= ' ** '.`/bin/date`;

	#Bildschirm loeschen
	$cmd2 = `clear`;
	print $cmd2;

	$cmd =~ s/#/\n/g;
	$cmd =~ s/\|/\t/g;
	$cmd .= "\n";
	print $cmd;
	sleep(3);
	#exit;
}
