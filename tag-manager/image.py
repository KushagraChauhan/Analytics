'''Structure of DB'''
#	CREATE TABLE img(
#	id uuid PRIMARY KEY,
#	image blob
#	)
#

# # '''Python code to insert image into a Cassandra DB'''
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
import os, uuid, base64
cluster = Cluster()
session = cluster.connect('test')
# file = os.path.join(os.getcwd(), 'test.jpg')
# fid = uuid.uuid4()
# with open(file, 'rb') as f:
# 	data = f.read()
# 	res = base64.b64encode(data)
# 	res1 = res.decode('utf-8')
# 	session.execute("INSERT INTO img (id, image) VALUES (%s,%s)", (fid, res))
import pandas as pd
def pandas_factory(colnames, rows):
        return pd.DataFrame(rows, columns=colnames)
session.row_factory = pandas_factory
session.default_fetch_size = None

'''Python Code to retrieve image from Cassandra DB'''
imagequery = "SELECT image from test.img where id=ef2ff674-ee17-40d8-a908-597186348d0e ALLOW FILTERING;"
result_img = session.execute(imagequery)
#data = str(result_img)
df = result_img._current_rows
data = df.values.tolist()
listtostr = ''.join(map(str,data))
listtostr = listtostr.strip('[]')
listtostr = listtostr.strip('b')
#print(listtostr)
imgdata = base64.b64decode(listtostr)
#print(imgdata)
file = 'trial.jpg'
with open(file,'wb') as f:
	f.write(imgdata)
