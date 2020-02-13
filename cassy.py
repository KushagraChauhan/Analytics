'''this is cassandra db connection with python'''

from cassandra.cluster import Cluster

cluster = Cluster() # cluster = Cluster(['192.168.0.1', '192.168.0.2']) to specidy IP

#establish a connection
session = cluster.connect()
rows = session.execute('')
