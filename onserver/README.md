
## FLANA 
### Web Analytics App using Flask
### Cassandra Database - NoSQL
---
***Note-*** This project is based on the configurations required by Bitnami Lamp hosted on a web-server.
Folder Structure-
```
├── ...
├── Analytics                   
│   ├── app.py         
│   ├── app.wsgi         
│   └── app.conf               
└── ...
```

In the Config file add-
		
	
	  ServerName serverdomain
	  ServerAdmin admin@$domain
	  WSGIScriptAlias /flana /path/to/analytics/app.wsgi

	 <Directory /path/to/analytics/>
      <Files app.wsgi>
         Require all granted
     </Files>
     </Directory>

***Name the WSGI file the same as your main file.***
Add the following to app.wsgi-
	
	import sys
	import logging
	import os
	logging.basicConfig(stream=sys.stderr)
	sys.path.insert(0, '/home/himanshu/analytics/')

	from app import app as application

Before proceeding any further, check whether the above configuration is working or not.
For any issues, raise an issue.

Install Cassandra based on their official documentation by clicking on the below link-
[Install Cassandra](http://cassandra.apache.org/doc/latest/getting_started/installing.html)

After installation, check this command-
		
	nodetool status
If this shows running, then proceed with this command-

	cqlsh
Here if you get an error such as-

	Connection error: ('Unable to connect to any servers', {'127.0.0.1': TypeError('ref() does not take keyword arguments',)})

Solution for the above error-

	#Enter this command in your terminal
	export CQLSH_NO_BUNDLED=true


API Names:
	
[Retrieve User Profiles](https://analytics.techeela.net/ret)
[Enter Static Data](https://analytics.techeela.net/static)
[Retrieve Static Data](https://analytics.techeela.net/staticret)
[User group data wrt time period](https://analytics.techeela.net/usergroupdata)
[Category wise data within a time peroid](https://analytics.techeela.net/categorydata)

### Happy Coding






