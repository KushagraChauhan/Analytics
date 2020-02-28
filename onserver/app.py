from flask import Flask, render_template, jsonify, request, Response
import json
import geoip2.database as geo
import os
import uuid
from flask_cqlalchemy import CQLAlchemy
import datetime
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory
import pandas as pd

app = Flask(__name__)
app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']
app.config['CASSANDRA_KEYSPACE'] = "test"
db = CQLAlchemy(app)

################################################################################
'''Get details of the user through JS'''
'''Store the details in an image of 1px and send to the Flask app'''
################################################################################
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/details", methods=['POST'])
def rec_img():
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

    currentDT = datetime.datetime.now()

    Usertime.objects().create(url=img_url, ref=img_ref, width=img_width,
    height=img_height, platform=img_plaform, history=img_history, ip=ip,time1=datetime.datetime.utcnow(),
    time2=currentDT.strftime("%H:%M:%S"))

################################################################################
'''Structure of Cassandra database'''
################################################################################
class Usertime(db.Model):
    __keyspace__ = 'test'
    id = db.columns.UUID(primary_key = True, default = uuid.uuid4)
    url = db.columns.Text()
    ref = db.columns.Text()
    nav = db.columns.Text()
    width = db.columns.Integer()
    height = db.columns.Integer()
    platform = db.columns.Text()
    history = db.columns.Integer()
    ip = db.columns.Text()
    time1 = db.columns.Date()
    time2 = db.columns.Time()
################################################################################
'''get the geolocation of the user'''
################################################################################
@app.route("/ip", methods=["GET"])
def location():
    ip = request.remote_addr
    city = getCity(ip)
    country = getCountry(ip)
    return city +' ' + country

def getCity(ip):
    ip = request.remote_addr
    MYDIR = os.path.dirname(os.path.abspath(__file__))
    data=os.path.join(MYDIR, "GeoLite2-City.mmdb")
    reader = geo.Reader(data)
    response = reader.city(ip)
    return response.city.name
def getCountry(ip):
    ip = request.remote_addr
    MYDIR = os.path.dirname(os.path.abspath(__file__))
    data1=os.path.join(MYDIR, "GeoLite2-Country.mmdb")
    reader = geo.Reader(data1)
    response = reader.country(ip)
    return response.country.name

################################################################################
'''API to send user profile from DB'''
###############################################################################
@app.route('/ret')
def retreive():
    cluster = Cluster(contact_points=['127.0.0.1'], port=9042)

    session = cluster.connect('test')
    session.row_factory = dict_factory

    query = "SELECT ip, url, time1, ref, nav, time2, platform, width, height FROM {}.{};".format('test', 'usertime')

    def pandas_factory(colnames, rows):
        return pd.DataFrame(rows, columns=colnames)

    session.row_factory = pandas_factory
    session.default_fetch_size = None

    rslt = session.execute(query, timeout=None)
    df = rslt._current_rows
    data1 = df.to_json ()

    return Response(df.to_json(orient="split"), mimetype='application/json')
################################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###################### I N T E R A C T I O N S ################################
###################### ON              WEBSITE ################################
###############################################################################
###############################################################################
###############################################################################
@app.route("/static")
def index1():
    return render_template('static.html')

@app.route('/process',methods= ['POST'])
def process():
    userID = request.form['userID']
    expID = request.form['expID']
    date = request.form['date']
    time = request.form['time']
    subcategory = request.form['subcategory']
    userGroup = request.form['userGroup']
    session_id = request.form['session_id']
    category = request.form['category']
    device = request.form['device']
    ip = request.form['ip']

    Expcentreclickdata.objects().create(userid=userID, expid=expID, click_date=date, click_time=time,
    category=category,session_id=session_id,ip=ip,subcategory=subcategory,usergroup=userGroup,device=device)
    return "Thanks"

################################################################################
'''Database for interactons on website'''
################################################################################
class Expcentreclickdata(db.Model):
    __keyspace__ = 'test'
    #id = db.columns.UUID(primary_key = True, default = uuid.uuid4)
    expid = db.columns.Integer()
    click_date = db.columns.Date()
    click_time = db.columns.Time()
    category = db.columns.Text()
    session_id = db.columns.Integer()
    ip = db.columns.Text()
    device = db.columns.Text()
    userid = db.columns.Integer(primary_key=True)
    subcategory = db.columns.Text()
    usergroup = db.columns.Text()

################################################################################
################################################################################
'''API to retrieve all user data'''
###############################################################################
@app.route('/userdataret')
def retreive2():
    cluster = Cluster(contact_points=['127.0.0.1'], port=9042)

    session = cluster.connect('test')
    session.row_factory = dict_factory

    #query = "SELECT userid, value, time1, usergroup FROM {}.{};".format('test', 'userdata')
    query = "SELECT usergroup, click_date, click_time, ip, device, category, subcategory, expid, session_id,userid  FROM {}.{};".format('test', 'expcentreclickdata')
    query1 = "SELECT click_date FROM test.expcentreclickdata;"
    def pandas_factory(colnames, rows):
        return pd.DataFrame(rows, columns=colnames)

    session.row_factory = pandas_factory
    session.default_fetch_size = None

    rslt = session.execute(query, timeout=None)
    df = rslt._current_rows
    data1 = df.values.tolist ()
    data2 = df.to_json()
    print(data1)
#    return Response(df.to_json(orient="split"), mimetype='application/json')
    return json.dumps(data1, indent=4, sort_keys=True, default=str)
    #return jsonify(data1)
###############################################################################
'''API to get user data in a specific time period'''
###############################################################################
@app.route('/userdataret1',methods=['GET'])
def retreive3():
    cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
    #startdate = request.args.['startdate']
    startdate = request.args['startdate']
    enddate = request.args['enddate']
    usergroup = request.args['usergroup']
    session = cluster.connect('test')
    session.row_factory = dict_factory

    #query1 = "SELECT Count(*) FROM test.Expcentreclickdata WHERE usergroup={} AND click_date>start_date&, click_date={} ALLOW FILTERING;".format{}
    query2 = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND usergroup={} ALLOW FILTERING;".format(startdate, enddate,usergroup)
    query3 = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND usergroup={} ALLOW FILTERING;".format(startdate, enddate,usergroup)

    #query = "SELECT userid, value, time1, usergroup FROM {}.{};".format('test', 'userdata')

    def pandas_factory(colnames, rows):
        return pd.DataFrame(rows, columns=colnames)

    session.row_factory = pandas_factory
    session.default_fetch_size = None

    rslt = session.execute(query2, timeout=None)
    print(rslt)
    df = rslt._current_rows
    print(df)
    data1 = df.values.tolist ()
    #return Response(df.to_json(), mimetype='application/json')
    jsp = json.dumps(data1, indent=4, sort_keys=True, default=str)
    return Response(jsp)
###############################################################################
###############################################################################

if __name__ == "__main__":
    app.run(debug=True)
