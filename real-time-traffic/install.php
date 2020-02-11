 <?php

   	$handle = sqlite_open( $_SERVER['DOCUMENT_ROOT'].'stats.db', 0666, $sqliteError ) or die(  $sqliteError  );

   	# Set the command to create a table
   	$sqlCreateTable = "CREATE TABLE stats(page text UNIQUE, ip text, views UNSIGNED int DEFAULT 0, referrer text DEFAULT '')";

   	# Execute it
   	sqlite_exec( $handle, $sqlCreateTable );

   	# Print that we are done
   	echo 'Finished!';

    // connect to mongodb
    // $m = new MongoClient();
    //
    // echo "Connection to database successfully";
    // // select a database
    // $db = $m->trial;
    //
    // echo "Database trial selected";
    //
    // $collection = $db-> createCollection("mycol", {capped : true, autoIndexId:true, size:76000, max:1000})
    //
    // echo "Collection created successfully"
    //
    // $document = array(
    //    "page" => "test",
    //    "ip" => "192.168.1.1",
    //    "views" => 3,
    //    "referrals" => "kush",
    //    );
    //
    // $collection->insert($document);
    // echo "Document inserted successfully";
    	# Open the database
?>
