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
    img_catgeory = rf['category']
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


    resp_dic={'subcategory':img_subcategory}
    resp = jsonify(resp_dic)
    resp.headers['Access-Control-Allow-Origin']='*'


    ############################################################################
    '''Storing the data in the Cassandra db'''
    ############################################################################
    Expcentre.objects().create(url=img_url, ref=img_ref, width=img_width,
    height=img_height, platform=img_plaform, history=img_history,clickdate=date, clicktime=time,
    subcategory=img_subcategory, category=img_catgeory)

    return resp
################################################################################
'''Structure of Cassandra database'''
################################################################################

class Expcentre(db.Model):
    __keyspace__ = 'test'
    id = db.columns.UUID(primary_key = True, default = uuid.uuid4)
    url = db.columns.Text()
    ref = db.columns.Text()
    nav = db.columns.Text()
    width = db.columns.Integer()
    height = db.columns.Integer()
    platform = db.columns.Text()
    history = db.columns.Integer()
    subcategory = db.columns.Text()
    category = db.columns.Text()
    clickdate = db.columns.Date()
    clicktime = db.columns.Time()
################################################################################
################################################################################
################################################################################
'''API to get real-time data'''
###############################################################################
################################################################################
################################################################################


if __name__ == "__main__":
    app.run(debug=True)
