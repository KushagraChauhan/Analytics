import os
#import magic
import urllib.request
import uuid, base64
from flask import Flask, flash, request, redirect, render_template, jsonify
import json
from werkzeug.utils import secure_filename
from flask_cors import CORS
from cassandra.cluster import Cluster
from flask_cqlalchemy import CQLAlchemy
app = Flask(__name__)
app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']
app.config['CASSANDRA_KEYSPACE'] = "test"
db = CQLAlchemy(app)
CORS(app)

#################################################################################
'''Get the 1px image from the analytics.js'''
#################################################################################
@app.route('/')
def start():
	return render_template('index.html')

@app.route('/tracker', methods=['POST'])
def rec_img():
    print("received klayer")
    rf = request.form
    print(rf)
    for key in rf.keys():
        data=key
    print("The data is----------",data)
    data_dic = json.loads(data)
    print("............",data_dic.keys())
    img_url = data_dic['url']
    img_width = data_dic['width']
    img_height = data_dic['height']
    img_plaform = data_dic['platform']
    img_history = data_dic['history']
    img_ref = data_dic['ref']
    img_nav = data_dic['nav']
    img_plugins = data_dic['_plugins']
    print('<<<<<<',img_url,'>>>>>>>')
    print('<<<<<<',img_width,'>>>>>>>')
    print('<<<<<<',img_height,'>>>>>>>')
    print('<<<<<<',img_plaform,'>>>>>>>')
    print('<<<<<<',img_history,'>>>>>>>')
    print('<<<<<<',img_ref,'>>>>>>>')
    print('<<<<<<',img_nav,'>>>>>>>')
    ip = request.remote_addr
    resp_dic={'url':img_url, 'msg':"details:",
    'width':img_width, 'height':img_height}
    resp = jsonify(resp_dic)
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
