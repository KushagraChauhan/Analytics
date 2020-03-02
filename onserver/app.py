from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS
import json
import geoip2.database as geo
import os
import uuid
from flask_cqlalchemy import CQLAlchemy
from datetime import date
import datetime
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory
import pandas as pd
from operator import truediv
import numpy as np
app = Flask(__name__)
app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']
app.config['CASSANDRA_KEYSPACE'] = "test"
db = CQLAlchemy(app)
CORS(app)
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

    #resp.headers['Access-Control-Allow-Origin']='*'
#    return Response(df.to_json(orient="table"), mimetype='application/json')
    return json.dumps(data1, indent=4, sort_keys=True, default=str)
    #return jsonify(data1)
###############################################################################
'''API to get user group in a specific time period'''
###############################################################################
@app.route('/userdataret1',methods=['GET'])
def retreive3():
    cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
    #startdate = request.args.['startdate']
    startdate = request.args['startdate']
    enddate = request.args['enddate']
#    category = request.args['category']
#    usergroup = request.args['usergroup']
#   subcategory = request.args['subcategory']
    session = cluster.connect('test')
    session.row_factory = dict_factory
    print(startdate)
    startdate_st = startdate.strip()
    string = 'hello'
    print(string.strip())
    startdate_st = startdate.strip('()')
    print(startdate.strip())
    enddate_st = enddate.strip('()')
    print(enddate.strip('()'))
    start = datetime.datetime.strptime(startdate_st, "%Y-%m-%d")
    end = datetime.datetime.strptime(enddate_st, "%Y-%m-%d")
    delta = end - start
    print(delta.days)
    durationtime = delta.days + 1
    print(durationtime)
    print("durationtime", durationtime)
    startday = start.strftime("%d")
    endday = end.strftime("%d")
    endstart = start.strftime("%d")
    endday_mon = end.strftime("%m")
    year_start = start.strftime("%Y")
    year_end = end.strftime("%Y")
    print(startday)
    print(endday_mon)
    prevenddate = int(startday) - 1
    print('prev end',prevenddate)
    prevstartdate = prevenddate - durationtime + 1
    print('prev start',prevstartdate)
    startdate1 = "'" + startdate +"'"
    print(startdate1)
    enddate1 = "'" + enddate +"'"
    print(enddate1)
    prevstartdate1 = "'" + year_start + "-" + endday_mon + "-" + str(prevenddate) + "'"
    prevenddate1 = "'" + year_end + "-" + endday_mon + "-" + str(prevstartdate) + "'"
    #prevenddate1 = "2020-" + endday_mon + "-" +prevenddate

    print(prevstartdate1)
    print(prevenddate1)

    def pandas_factory(colnames, rows):
        return pd.DataFrame(rows, columns=colnames)
    session.row_factory = pandas_factory
    session.default_fetch_size = None
    #usergroupquery = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND usergroup={} ALLOW FILTERING;".format(startdate1, enddate1, usergroup)
    #prevusergroupquery = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND usergroup={} ALLOW FILTERING;".format(prevenddate1, prevstartdate1,usergroup)
    # usergroup = ['Customer', 'Prospect', 'Employee']
    userquery = "SELECT usergroup FROM test.Expcentreclickdata ALLOW FILTERING;"
    rslt_usergroup = session.execute(userquery)
    df_usergroup = rslt_usergroup._current_rows
    data_usergroup = df_usergroup.values.tolist()

    unique_list = []
    for x in data_usergroup:
        if x not in unique_list:
            unique_list.append(x)
    usergroup1 = str(unique_list[0]).strip('[]')
    usergroup2 = str(unique_list[1]).strip('[]')
    usergroup3 = str(unique_list[2]).strip('[]')
#group1
    usergroupquery1 = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND usergroup={} ALLOW FILTERING;".format(startdate1, enddate1, usergroup1)
    prevusergroupquery1 = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND usergroup={} ALLOW FILTERING;".format(prevenddate1, prevstartdate1, usergroup1)
#group2
    usergroupquery2 = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND usergroup={} ALLOW FILTERING;".format(startdate1, enddate1, usergroup2)
    prevusergroupquery2 = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND usergroup={} ALLOW FILTERING;".format(prevenddate1, prevstartdate1, usergroup2)
#group3
    usergroupquery3 = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND usergroup={} ALLOW FILTERING;".format(startdate1, enddate1, usergroup3)
    prevusergroupquery3 = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND usergroup={} ALLOW FILTERING;".format(prevenddate1, prevstartdate1, usergroup3)

    #categoryquery = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND category={} ALLOW FILTERING;".format(startdate, enddate,category)
    #prevcategoryquery = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND category={} ALLOW FILTERING;".format(prevenddate1, prevstartdate1,category)
###############################################################################
    def pandas_factory(colnames, rows):
        return pd.DataFrame(rows, columns=colnames)

    session.row_factory = pandas_factory
    session.default_fetch_size = None
    ####################
    '''For group1'''
    ####################
    rslt_userdata_now1 = session.execute(usergroupquery1, timeout=None)
    rslt_userdata_prev1 = session.execute(prevusergroupquery1, timeout=None)
    df_userdata_now1= rslt_userdata_now1._current_rows
    df_userdata_prev1 = rslt_userdata_prev1._current_rows
    data_userdata_now1 = df_userdata_now1.values.tolist ()
    data_userdata_prev1 = df_userdata_prev1.values.tolist()
    ####################
    '''For group2'''
    ####################
    rslt_userdata_now2 = session.execute(usergroupquery2, timeout=None)
    rslt_userdata_prev2 = session.execute(prevusergroupquery2, timeout=None)
    df_userdata_now2 = rslt_userdata_now2._current_rows
    df_userdata_prev2 = rslt_userdata_prev2._current_rows
    data_userdata_now2 = df_userdata_now2.values.tolist ()
    data_userdata_prev2 = df_userdata_prev2.values.tolist()
    ####################
    '''For group3'''
    ####################
    rslt_userdata_now3 = session.execute(usergroupquery3, timeout=None)
    rslt_userdata_prev3 = session.execute(prevusergroupquery3, timeout=None)
    df_userdata_now3 = rslt_userdata_now3._current_rows
    df_userdata_prev3 = rslt_userdata_prev3._current_rows
    data_userdata_now3 = df_userdata_now3.values.tolist ()
    data_userdata_prev3 = df_userdata_prev3.values.tolist()
#######################################################################
    # rslt_category_now = session.execute(categoryquery, timeout=None)
    # rslt_category_prev = session.execute(prevcategoryquery, timeout=None)
    # df_category_now = rslt_category_now._current_rows
    # df_category_prev = rslt_category_prev._current_rows
    # data_category_now = df_category_now.values.tolist ()
    # data_category_prev = df_category_prev.values.tolist()
# ####################################################################

###Group1 calculation
    data_userdata_percenatge = []
    u1 = data_userdata_now1[0]
    u2 = data_userdata_prev1[0]
    print(u2)
    print(u1)
    diff = list(np.array(u1) - np.array(u2))
    u1 = str(u1).strip('[]')
    print("difference:",diff)
    res1 = list(map(truediv, diff , u2))
    my_new_list1 = [i * 100 for i in res1]
    res_final1 = my_new_list1.append(u1)
    print(my_new_list1)
    res_final1 = my_new_list1.append(usergroup1)

###Group2 calculation
    data_userdata_percenatge = []
    u3 = data_userdata_now2[0]
    u4 = data_userdata_prev2[0]
    print(u3)
    print(u4)
    diff = list(np.array(u3) - np.array(u4))
    u3 = str(u3).strip('[]')
    print("difference:",diff)
    res2 = list(map(truediv, diff , u4))
    my_new_list2 = [i * 100 for i in res2]
    res_final2 = my_new_list2.append(u3)
    print(my_new_list2)
    res_final2 = my_new_list2.append(usergroup2)

###Group3 calculation
    data_userdata_percenatge = []
    u5 = data_userdata_now3[0]
    u6 = data_userdata_prev3[0]
    print(u5)
    print(u6)
    diff = list(np.array(u5) - np.array(u6))
    u5 = str(u5).strip('[]')
    print("difference:",diff)
    res3 = list(map(truediv, diff , u6))
    my_new_list3 = [i * 100 for i in res3]
    res_final3 = my_new_list3.append(u5)
    print(my_new_list3)
    res_final3 = my_new_list3.append(usergroup3)

#     data_category_percentage = (data_category_now - data_category_prev)/data_category_prev * 100
#
#     list_userdata = sorted(data_userdata_now)
#     list_category = sorted(data_category_now)

    #return Response(data_percenatge.to_json(), mimetype='application/json')
    my_new_list = [my_new_list1, my_new_list2, my_new_list3]
    print(my_new_list[0])
    jsp = json.dumps(my_new_list, indent=4, sort_keys=True, default=str)
    return Response(jsp)
###############################################################################
###############################################################################
'''API to get category data within a specific period'''
###############################################################################
###############################################################################
@app.route('/userdataret2',methods=['GET'])
def retrieve4():
    cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
    startdate = request.args['startdate']
    enddate = request.args['enddate']
    category = request.args['category']
    session = cluster.connect('test')
    session.row_factory = dict_factory
    print(startdate)
    startdate_st = startdate.strip()
    string = 'hello'
    print(string.strip())
    startdate_st = startdate.strip('()')
    print(startdate.strip())
    enddate_st = enddate.strip('()')
    print(enddate.strip('()'))
    start = datetime.datetime.strptime(startdate_st, "%Y-%m-%d")
    end = datetime.datetime.strptime(enddate_st, "%Y-%m-%d")
    delta = end - start
    print(delta.days)
    durationtime = delta.days + 1
    print(durationtime)
    print("durationtime", durationtime)
    startday = start.strftime("%d")
    endday = end.strftime("%d")
    endstart = start.strftime("%d")
    endday_mon = end.strftime("%m")
    year_start = start.strftime("%Y")
    year_end = end.strftime("%Y")
    print(startday)
    print(endday_mon)
    prevenddate = int(startday) - 1
    print('prev end',prevenddate)
    prevstartdate = prevenddate - durationtime + 1
    print('prev start',prevstartdate)
    startdate1 = "'" + startdate +"'"
    print(startdate1)
    enddate1 = "'" + enddate +"'"
    print(enddate1)
    prevstartdate1 = "'" + year_start + "-" + endday_mon + "-" + str(prevenddate) + "'"
    prevenddate1 = "'" + year_end + "-" + endday_mon + "-" + str(prevstartdate) + "'"

    print(prevstartdate1)
    print(prevenddate1)

    def pandas_factory(colnames, rows):
        return pd.DataFrame(rows, columns=colnames)
    session.row_factory = pandas_factory
    session.default_fetch_size = None

    categoryquery = "SELECT subcategory FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND category={} ALLOW FILTERING;".format(startdate1, enddate1, category)

    rslt_category = session.execute(categoryquery)
    df_category = rslt_category._current_rows
    data_category = df_category.values.tolist()

    unique_list = []
    for x in data_category:
        if x not in unique_list:
            unique_list.append(x)
    # for i in unique_list:
    #     subcategory_unique=str(unique_list).strip('[]')
    subcategory_unique = [i.strip('[]') for i in str(unique_list)]

    print(subcategory_unique)



    jsp = json.dumps(subcategory_unique, indent=4, sort_keys=True, default=str)
    return jsp
###############################################################################
###############################################################################

if __name__ == "__main__":
    app.run(debug=True)
