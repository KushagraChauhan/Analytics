<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Live Traffic Display</title>
</head>
<body>

<?php
	# Open up the database
	$handle = sqlite_open( $_SERVER['DOCUMENT_ROOT'].'/stats.db', 0666, $sqliteError ) or die( $sqliteError );

	# Get all the statistics
	$sqlGet = 'SELECT * FROM stats';
	$result = sqlite_query( $handle, $sqlGet );

	# Create an unordered list
	echo "<ul>\n";

	# If there are results
	if( $result ) {
		$page_views = 0;
		$unique_visitors = 0;

		# Fetch them
		while( ($info = sqlite_fetch_array( $result ) ) ) {
			# Get the page, views, IPs, and referrers
			$page = $info['page'];
			$views = $info['views'];
			$ips = $info['ip'];
			$referrers = $info['referrer'];

			# Print out a list element with the $page/$views information if( $views == 1 ) echo "\t<li>\n\t\t<p>$page was viewed $views time:</p>\n"; else echo "\t<li>\n\t\t<p>$page was viewed $views times:</p>\n"; # Update the number of page views $page_views += $views; # Parse the data of IPs and Referrers using process.php's code preg_match_all( '%(\d+)\((.*?)\)%', $ips, $matches ); # Find the size of the data $size = count( $matches[1] ); # Create a sub list echo "\t\t<ul>\n"; # Loop through all the IPs for( $i = 0; $i < $size; $i++ ) { # Find the number of visits $num = $matches[1][$i]; # Find the IP address $ip = $matches[2][$i]; # Print the info in a list element if( $num == 1 ) echo "\t\t\t<li>$num time by $ip</li>\n"; else echo "\t\t\t<li>$num times by $ip</li>\n"; # Update the number of unique visitors $unique_visitors++; } # Repeat the whole process for referrers preg_match_all( '%(\d+)\((.*?)\)%', $referrers, $matches ); $size = count( $matches[1] ); # Loop through each one for( $i = 0; $i < $size; $i++ ) { $num = $matches[1][$i]; $referrer = $matches[2][$i]; # Print out the info if( $num == 1 ) echo "\t\t\t<li>$num referral by $referrer</li>\n"; else echo "\t\t\t<li>$num referrals by $referrer</li>\n"; } # End the sub-list echo "\t\t</ul>\n"; # End the list element echo "\t</li>\n"; } echo "\t<li>Total unique visitors: $unique_visitors</li>\n"; echo "\t<li>Total page views: $page_views</li>\n"; } # End the unordered list echo "</ul>\n"; # Close the database sqlite_close($handle); ?> </body> </html>

?>

</body>
</html>
