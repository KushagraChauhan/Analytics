import os
#import magic
import urllib.request
import uuid, base64
from flask import Flask, flash, request, redirect, render_template, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from cassandra.cluster import Cluster
app = Flask(__name__)
app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']
from flask_cqlalchemy import CQLAlchemy
app.config['CASSANDRA_KEYSPACE'] = "test"
db = CQLAlchemy(app)
CORS(app)


#################################################################################
'''Get the Base64 encoded string from the Web Page'''
#################################################################################
@app.route('/')
def start():
	return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_img():
    print("received img")
    rf = request.form
    print(rf)
    for key in rf.keys():
        data=key
    #print("The data is----------",data)

    data1 = data.replace("data:image/png;base64,","")
    print("data:",data1)
    resp = jsonify("received")
    resp.headers['Access-Control-Allow-Origin']='*'

    ############################################################################
    '''Storing the data in the Cassandra db'''
    ############################################################################
    cluster = Cluster()
    session = cluster.connect('test')
    fid = uuid.uuid4()
    session.execute("INSERT INTO test.Heatmap (id, imgdata) VALUES (%s,%s)", (fid, data1))
    return resp
################################################################################
'''Structure of Cassandra database'''
################################################################################
#	CREATE TABLE img(
#	id uuid PRIMARY KEY,
#	image blob
#	)

class Heatmap(db.Model):
    __keyspace__ = 'test'
    id = db.columns.UUID(primary_key = True, default = uuid.uuid4)
    imgdata = db.columns.Text()
################################################################################
################################################################################
################################################################################

if __name__ == "__main__":
    app.run(debug=True)
