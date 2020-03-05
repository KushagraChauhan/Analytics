from flask import Flask, render_template, jsonify, request, Response, make_response
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
import json
from pandas.io.json import json_normalize
import geoip2.database as geo
import os
import re
import uuid
from flask_cqlalchemy import CQLAlchemy
from datetime import date, timedelta
import datetime
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory
from cassandra.query import tuple_factory
import pandas as pd
from operator import truediv
import numpy as np
app = Flask(__name__)
app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']
app.config['CASSANDRA_KEYSPACE'] = "test"
db = CQLAlchemy(app)
CORS(app)
auth = HTTPBasicAuth()
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
    # Expcentreclickdata_test.objects().create(userid=userID, expid=expID, click_date=date, click_time=time,
    # category=category,session_id=session_id,ip=ip,subcategory=subcategory,usergroup=userGroup,device=device)
    return "Thanks"

################################################################################
'''Database for interactons on website'''
################################################################################
class Expcentreclickdata(db.Model):
    __keyspace__ = 'test'
    id = db.columns.UUID(primary_key = True, default = uuid.uuid4)
    category = db.columns.Text()
    subcategory = db.columns.Text()
    usergroup = db.columns.Text()
    userid = db.columns.Integer()
    expid = db.columns.Integer()
    device = db.columns.Text()
    session_id = db.columns.Integer()
    click_date = db.columns.Date()
    click_time = db.columns.Time()
    ip = db.columns.Text()

class Expcentreclickdata_test(db.Model):
    __keyspace__ = 'test'
    id = db.columns.UUID(primary_key = True, default = uuid.uuid4)
    category = db.columns.Text()
    subcategory = db.columns.Text()
    usergroup = db.columns.Text()
    userid = db.columns.Integer()
    expid = db.columns.Integer()
    device = db.columns.Text()
    session_id = db.columns.Integer()
    click_date = db.columns.Text()
    click_time = db.columns.Text()
    ip = db.columns.Text()

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
    data_length = len(data1)
    #data3 = pd.DataFrame(data=data2)
    #resp.headers['Access-Control-Allow-Origin']='*'
    return Response(df.to_json(force_ascii=False, orient="records"), mimetype='application/json')
    # for i in range(10):
    #     jsp = json.dumps({'usergroup':str(data1[i])}, indent=4, sort_keys=True, default=str)
    # return jsp

    #return jsonify(data1)

###############################################################################
###############################################################################
'''API to get category data within a specific period'''
###############################################################################
###############################################################################
@app.route('/categorydata',methods=['GET'])
@auth.login_required
def retrieve5():
    cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
    startdate = request.args['startdate']
    enddate = request.args['enddate']
    category = request.args['category']
    session = cluster.connect('test')
    session.row_factory = dict_factory
    startdate_st = startdate.strip()
    startdate_st = startdate.strip('()')
    enddate_st = enddate.strip('()')
    start = datetime.datetime.strptime(startdate_st, "%Y-%m-%d")
    end = datetime.datetime.strptime(enddate_st, "%Y-%m-%d")
    delta = end - start
    durationtime = delta.days + 1
    startday = start.strftime("%d")
    endday = end.strftime("%d")
    endstart = start.strftime("%d")
    endday_mon = end.strftime("%m")
    year_start = start.strftime("%Y")
    year_end = end.strftime("%Y")
    dt_prev_start = start - timedelta(durationtime)
    dt_prev_end = end - timedelta(durationtime)
    d1 = str(dt_prev_end)
    prevenddate = d1.strip("00:00:00")
    d2 = str(dt_prev_start)
    prevstartdate = d2.strip("00:00:00")
    startdate1 = "'" + startdate +"'"
    enddate1 = "'" + enddate +"'"
    prevstartdate = prevstartdate.strip()
    prevstartdate =  "'"+ prevstartdate +"'"
    prevenddate = prevenddate.strip()
    prevenddate =  "'"+ prevenddate +"'"
    def pandas_factory(colnames, rows):
        return pd.DataFrame(rows, columns=colnames)
    session.row_factory = pandas_factory
    session.default_fetch_size = None
    categoryquery = "SELECT subcategory FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND category={} ALLOW FILTERING;".format(startdate1, enddate1, category)
    rslt_category = session.execute(categoryquery)
    df_category = rslt_category._current_rows
    data_category = df_category.values.tolist()
    unique_list = []
#########Get all the unique subcategories in the given category#################
    for x in data_category:
        if x not in unique_list:
            unique_list.append(x)
    category_length = len(unique_list)
    subcategory_unique = []
    for i in range(category_length):
        subcategory_unique.append(str(unique_list[i]).strip('[]'))
    subcategory_length = len(subcategory_unique)#Get the stripped down vresion of the unique list
    data_category_prev = []
    data_now = []
    data_prev = []
    final_result = []
##############Execute the query and save in a list#####################
    for i in range(category_length):
        subcategoryquery = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND subcategory={} ALLOW FILTERING;".format(startdate1, enddate1, subcategory_unique[i])
        prevsubcategoryquery = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND subcategory={} ALLOW FILTERING;".format(prevstartdate, prevenddate, subcategory_unique[i])
        rslt_category_now = session.execute(subcategoryquery, timeout=None)
        rslt_category_prev = session.execute(prevsubcategoryquery, timeout=None)
        df_category_now = rslt_category_now._current_rows
        df_category_prev = rslt_category_prev._current_rows
        data_category_now = df_category_now.values.tolist()
        data_category_prev = df_category_prev.values.tolist()
        data_now.append(str(data_category_now))
        data_prev.append(str(data_category_prev))
###############Calculations on the data#########################################
    z = []
    for i in range(category_length):
        try:
            u1 = data_now[i]
            u2 = data_prev[i]
            print("u2",u2)
            u1 = str(u1).strip('[]')
            u2 = str(u2).strip('[]')
            diff = int(u1) - int(u2)
            res = diff/int(u2)
            res = res*100
            my_new_list = [res]
            res_final = my_new_list.append(u1)
            res_final = my_new_list.append(subcategory_unique[i])
            final_result.append(str(my_new_list))
            x = {"subcategory":subcategory_unique[i],"count":u1, "change%":res, "duration":durationtime, "prevcount":int(u2)}
            print(x)
            y = json.dumps(x, sort_keys=True)
            z.append(json.loads(y))
        except ZeroDivisionError:
            zero_error={
            "title":"Division by zero",
            "status":"100",
            "details":"There is no value in the previous duration"
            }
            return make_response(jsonify({'errors': zero_error}), 400)
        # print ("Sorted:-----------------",sorted(z, key = lambda i: i['count'],reverse=True))
        final = sorted(z, key = lambda i: i['count'],reverse=True)

    return jsonify({'data':final})
##################################################################################
'''API for usergroup (no hardcoding)'''
#################################################################################
@app.route('/usergroupdata',methods=['GET'])
@auth.login_required
def retrieve7():
    cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
    startdate = request.args['startdate']
    enddate = request.args['enddate']
    session = cluster.connect('test')
    session.row_factory = dict_factory
    startdate_st = startdate.strip()
    startdate_st = startdate.strip('()')
    enddate_st = enddate.strip('()')
    start = datetime.datetime.strptime(startdate_st, "%Y-%m-%d")
    end = datetime.datetime.strptime(enddate_st, "%Y-%m-%d")
    delta = end - start
    durationtime = delta.days + 1
    startday = start.strftime("%d")
    endday = end.strftime("%d")
    endstart = start.strftime("%d")
    endday_mon = end.strftime("%m")
    year_start = start.strftime("%Y")
    year_end = end.strftime("%Y")
    dt_prev_start = start - timedelta(durationtime)
    dt_prev_end = end - timedelta(durationtime)
    d1 = str(dt_prev_end)
    prevenddate = d1.strip("00:00:00")
    d2 = str(dt_prev_start)
    prevstartdate = d2.strip("00:00:00")
    startdate1 = "'" + startdate +"'"
    enddate1 = "'" + enddate +"'"
    prevstartdate = prevstartdate.strip()
    prevstartdate =  "'"+ prevstartdate +"'"
    prevenddate = prevenddate.strip()
    prevenddate =  "'"+ prevenddate +"'"
    def pandas_factory(colnames, rows):
        return pd.DataFrame(rows, columns=colnames)
    session.row_factory = pandas_factory
    session.default_fetch_size = None
    userquery = "SELECT usergroup FROM test.Expcentreclickdata ALLOW FILTERING;"
    rslt_usergroup = session.execute(userquery)
    df_usergroup = rslt_usergroup._current_rows
    data_usergroup = df_usergroup.values.tolist()
    unique_list = []
    for x in data_usergroup:
        if x not in unique_list:
            unique_list.append(x)
    category_length = len(unique_list)
    subcategory_unique = []
    for i in range(category_length):
        subcategory_unique.append(str(unique_list[i]).strip('[]'))
    subcategory_length = len(subcategory_unique)#Get the stripped down vresion of the unique list
    data_category_prev = []
    data_now = []
    data_prev = []
    final_result = []
    data_date = []
##############Execute the query and save in a list#####################
    for i in range(category_length):
        subcategoryquery = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND usergroup={} ALLOW FILTERING;".format(startdate1, enddate1 , subcategory_unique[i])
        prevsubcategoryquery = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND usergroup={} ALLOW FILTERING;".format(prevstartdate, prevenddate, subcategory_unique[i])
        clickdatequey = "SELECT click_date FROM test.Expcentreclickdata WHERE usergroup={} ALLOW FILTERING;".format(subcategory_unique[i])
        rslt_category_now = session.execute(subcategoryquery, timeout=None)
        rslt_category_prev = session.execute(prevsubcategoryquery, timeout=None)
        rslt_clickdate = session.execute(clickdatequey, timeout=None)
        df_category_now = rslt_category_now._current_rows
        df_category_prev = rslt_category_prev._current_rows
        df_clickdate = rslt_clickdate._current_rows
        data_category_now = df_category_now.values.tolist()
        data_category_prev = df_category_prev.values.tolist()
        data_clickdate = df_clickdate.values.tolist()
        data_now.append(str(data_category_now))
        data_prev.append(str(data_category_prev))
        data_date.append(str(data_clickdate))
######################Calculation##############################################
    z = []
    sub = []
    for i in range(category_length):
        try:
            u1 = data_now[i]
            u2 = data_prev[i]
            print("u2",u2)
            u1 = str(u1).strip('[]')
            u2 = str(u2).strip('[]')
            diff = int(u1) - int(u2)
            res = diff/int(u2)
            res = res*100
            my_new_list = [res]
            res_final = my_new_list.append(u1)
            res_final = my_new_list.append(subcategory_unique[i])
            final_result.append(str(my_new_list))
            print(subcategory_unique[i])
            sub.append(str(subcategory_unique[i]).replace("'", ""))
            print("SUB:",sub)
            x = {"User Group":sub[i],"count":int(u1), "change%":res, "duration":durationtime}
            y = json.dumps(x, sort_keys=True)
            z.append(json.loads(y))
            print(z)
        except ZeroDivisionError:
            zero_error={
            "title":"Division by zero",
            "status":"100",
            "details":"There is no value in the previous duration"
            }
            return make_response(jsonify({'errors': zero_error}), 400)

    return jsonify({'data':z})


#############################################
#Sort_keys = true
#show previous data in response
#
#######################################################################################
'''Not found error'''
######################################################################################
@app.errorhandler(404)
def not_found(error):
    not_found_error={
    "title":"Not found",
    "status":"404",
    "details":"Please check your url"
    }
    return make_response(jsonify({'errors': not_found_error}), 404)
########################################################################################
'''Authorization error'''
########################################################################################
@auth.get_password
def get_password(username):
    if username == 'kush':
        return 'hello'
    return None

@auth.error_handler
def unauthorized():
    auth_error={
    "title":"Unauthorized access",
    "status":"401",
    "details":"Please check your credentials"
    }
    return make_response(jsonify({'error': auth_error}), 401)
#######################################################################################

if __name__ == "__main__":
    app.run(debug=True)
