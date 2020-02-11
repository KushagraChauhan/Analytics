<?php
# Connect to the database
# Connect to the database
$handle = sqlite_open( $_SERVER['DOCUMENT_ROOT'].'/stats.db', 0666, $sqliteError ) or die( $sqliteError );

# Use the same-origin policy to prevent cross-site scripting (XSS) attacks
# Remember to replace http://yourdomain.com/ with your actual domain
if( strpos( $_SERVER['HTTP_REFERER'], 'http://techeela.org/' ) !== 0 ) {
     die( "Do not call this script manually or from an external source." );
}

# Obtain the necessary information, strip HTML tags, and escape the string for backup proetection
$page = sqlite_escape_string( strip_tags( $_POST['page'] ) );
$referrer = sqlite_escape_string( strip_tags( $_POST['referrer'] ) );
$ip = sqlite_escape_string( strip_tags( $_SERVER['REMOTE_ADDR'] ) );


# Query the database so we can update old information
$sqlGet = 'SELECT * FROM stats WHERE page = \''.$page.'\'';
$result = sqlite_query( $handle, $sqlGet );

# Set up a few variables to hold old information
$views = 0;
$ips = '';
$referrers = '';

# Check if old information exists
if( $result && ( $info = sqlite_fetch_array( $result ) ) ) {
	# Get this information
	$views = $info['views'];
	$ips = $info['ip'].' ';
	if( $info['referrer'] )
		$referrers = $info['referrer'].' ';

	# Set a flag to state that old information was found
	$flag = true;
}

# Create arrays for all referrers and ip addresses
$ref_num = array();
$ip_num = array();

# Find each referrer
$values = split( ' ', $referrers );

# Set a regular expression string to parse the referrer
$regex = '%(\d+)\((.*?)\)%';

# Loop through each referrer
foreach( $values as $value ) {
	# Find the number of referrals and the URL of the referrer
	preg_match( $regex, $value, $matches );

	# If the two exist
	if( $matches[1] && $matches[2] )
		# Set the corresponding value in the array ( referrer link -> number of referrals )
		$ref_num[$matches[2]] = intval( $matches[1] );
}

# If there is a referrer on this visit
if( $referrer )
	# Add it to the array
	$ref_num[$referrer]++;

# Get the IPs
$values = split( ' ', $ips );

# Repeat the same process as above
foreach( $values as $value ) {
	# Find the information
	preg_match( $regex, $value, $matches );

	# Make sure it exists
	if( $matches[1] && $matches[2] )
		# Add it to the array
		$ip_num[$matches[2]] = intval( $matches[1] );
}

# Update the array with the current IP.
$ip_num[$ip]++;

# Reset the $ips string
$ips = '';

# Loop through all the information
foreach( $ip_num as $key => $val ) {
	# Append it to the string (separated by a space)
	$ips .= $val.'('.$key.') ';
}

# Trim the String
$ips = trim( $ips );

# Reset the $referrers string
$referrers = '';

# Loop through all the information
foreach( $ref_num as $key => $val ) {
	# Append it
	$referrers .= $val.'('.$key.') ';
}

# Trim the string
$referrers = trim( $referrers );

# Update the number of views
$views++;

# If we did obtain information from the database
# (the database already contains some information about this page)
if( $flag )
	# Update it
	$sqlCmd = 'UPDATE stats SET ip=\''.$ips.'\', views=\''.$views.'\', referrer=\''.$referrers.'\' WHERE page=\''.$page.'\'';

# Otherwise
else
	# Insert a new value into it
	$sqlCmd = 'INSERT INTO stats(page, ip, views, referrer) VALUES \''.$page.'\', \''.$ips.'\',\''.$views.'\',\''.$referrers.'\'';

# Execute the commands
sqlite_exec( $handle, $sqlCmd );
?>
