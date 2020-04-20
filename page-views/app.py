import urllib.request
import uuid, base64
from uuid import UUID, uuid4
from flask import Flask, flash, request, redirect, render_template, jsonify, send_file, Response
import json
from werkzeug.utils import secure_filename
from flask_cors import CORS
from cassandra.cluster import Cluster
import pytz, datetime
from datetime import date, timedelta
from flask_cqlalchemy import CQLAlchemy
import pandas as pd
app = Flask(__name__)
app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']
app.config['CASSANDRA_KEYSPACE'] = "test"
db = CQLAlchemy(app)
CORS(app)

#################################################################################
'''Get the 1px image from the analytics.js'''
#################################################################################
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/pageview', methods=['POST'])
def pageview():
    print("received img")
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
    img_catgeory = data_dic['category']
    img_subcategory = data_dic['subcategory']
    img_date = data_dic['date']
    img_time = data_dic['time']
    resp_dic={'subcategory':img_subcategory}
    resp = jsonify(resp_dic)
    resp.headers['Access-Control-Allow-Origin']='*'
    expire_date = datetime.datetime.now()
    expire_date = expire_date + datetime.timedelta(days=730)
    expire_date_1 = expire_date + datetime.timedelta(seconds=1800)
    if '_utma' in request.cookies:
        utma = UUID(request.cookies['_utma'])
    else:
        utma = uuid4()
    resp.set_cookie('_utma', str(utma), expires=expire_date)
    if '_utmb' in request.cookies:
        utmb = UUID(request.cookies['_utmb'])
    else:
        utmb = uuid4()
    resp.set_cookie(
        '_utmb', str(utmb), expires=expire_date_1)


    ############################################################################
    '''Storing the data in the Cassandra db'''
    ############################################################################
    Pageviews.objects().create(url=img_url, ref=img_ref, width=img_width,
    height=img_height, platform=img_plaform, history=img_history,clickdate=img_date, clicktime=img_time,
    subcategory=img_subcategory, category=img_catgeory, utma=utma, utmb=utmb)

    # # Prevent HTTP caching.
    # resp.headers['Last-Modified'] = now
    # resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    # resp.headers['Pragma'] = 'no-cache'
    # resp.headers['Expires'] = '0'

    return resp
################################################################################
'''Structure of Cassandra database'''
################################################################################

class Pageviews(db.Model):
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
    viewdate = db.columns.Date()
    viewtime = db.columns.Time()
    utma = db.columns.UUID(default = uuid.uuid4)
    utmb = db.columns.UUID(default = uuid.uuid4)
    userID = db.columns.UUID(default = uuid.uuid4)

################################################################################
################################################################################
'''API to get the page-view count'''
################################################################################
################################################################################

@app.route('/pageviewcount',methods=['GET'])
def pageviewcount():
    cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
    session = cluster.connect('test')

    def pandas_factory(colnames, rows):
        return pd.DataFrame(rows, columns=colnames)
    session.row_factory = pandas_factory
    session.default_fetch_size = None

    pageviewquery = "SELECT COUNT(*) FROM test.Pageviews ALLOW FILTERING;"
    rslt_pageview = session.execute(pageviewquery, timeout=None)
    df_pageview = rslt_pageview._current_rows
    return Response(df_pageview.to_json(force_ascii=False, orient="records"), mimetype='application/json')

###################################################################################
if __name__ == "__main__":
    app.run(debug=True)
