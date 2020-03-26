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
    print("received 1px image")
    rf = request.json
    print(rf)
    print("The data is----------",rf['subcategory'])
    img_url = rf['url']
    img_width = rf['width']
    img_height = rf['height']
    img_plaform = rf['platform']
    img_history = rf['history']
    img_ref = rf['ref']
    img_nav = rf['nav']
    date = rf['date']
    time = rf['time']
    img_subcategory = rf['subcategory']
    print('<<<<<<',img_url,'>>>>>>>')
    print('<<<<<<',img_width,'>>>>>>>')
    print('<<<<<<',img_height,'>>>>>>>')
    print('<<<<<<',img_plaform,'>>>>>>>')
    print('<<<<<<',img_history,'>>>>>>>')
    print('<<<<<<',img_ref,'>>>>>>>')
    print('<<<<<<',img_nav,'>>>>>>>')
    print('<<<<<<',date,'>>>>>>>')
    print('<<<<<<',time,'>>>>>>>')

    ip = request.remote_addr
    resp_dic={'subcategory':img_subcategory}
    resp = jsonify(resp_dic)
    resp.headers['Access-Control-Allow-Origin']='*'

    return resp
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


################################################################################
################################################################################
################################################################################

if __name__ == "__main__":
    app.run(debug=True)
