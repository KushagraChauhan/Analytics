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
##################################################################################
'''Experiments with CQL'''
##################################################################################
@app.route('/usergroupdata1',methods=['GET'])
def retrieve8():
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
######################Execute the query and save in a list#####################


################
# CREATE OR REPLACE FUNCTION state_group_and_count( state map<text, int>, type text )
# CALLED ON NULL INPUT
# RETURNS map<text, int>
# LANGUAGE java AS '
# Integer count = (Integer) state.get(type);  if (count == null) count = 1; else count++; state.put(type, count); return state; ' ;
#
# CREATE OR REPLACE AGGREGATE group_and_count(text)
# SFUNC state_group_and_count
# STYPE map<text, int>
# INITCOND {};
################
    for i in range(category_length):
        #function query = "CREATE FUNCTION IF NOT EXISTS timeAgo(minutes int) CALLED ON NULL INPUT RETURNS timestamp LANGUAGE java AS ' long now = System.currentTimeMillis(); if (minutes == null) return new Date(now); return new Date(now - (minutes.intValue() * 60 * 1000));';"
        expquery = "SELECT timeAgo(60) from test.t ALLOW FILTERING;"
        subcategoryquery = "SELECT COUNT(*) FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} AND usergroup={} ALLOW FILTERING;".format(startdate1, enddate1 , subcategory_unique[i])
        prevsubcategoryquery = "SELECT group_and_count(usergroup)FROM test.Expcentreclickdata WHERE click_date>{} AND click_date<{} ALLOW FILTERING;".format(prevstartdate, prevenddate)
        clickdatequey = "SELECT click_date FROM test.Expcentreclickdata WHERE usergroup={} ALLOW FILTERING;".format(subcategory_unique[i])
        rslt_category_now = session.execute(subcategoryquery, timeout=None)
        rslt_category_prev = session.execute(prevsubcategoryquery, timeout=None)
        rslt_clickdate = session.execute(clickdatequey, timeout=None)
        df_category_now = rslt_category_now._current_rows
        df_category_prev = rslt_category_prev._current_rows
        df_clickdate = rslt_clickdate._current_rows
        data_category_now = df_category_now.to_json()
        data_category_prev = df_category_prev.values.tolist()
        data_clickdate = df_clickdate.values.tolist()
    #    print('df:',df_category_now)
    #    print(rslt_category_now)
    #    print("category now ",data_category_now)
        data_now.append(str(data_category_now))
        data_prev.append(str(data_category_prev))
        data_date.append(str(data_clickdate))
        rslt_exp = session.execute(expquery, timeout=None)
        df = rslt_exp._current_rows
    #    print(df)
    #print("data now:",data_now)
    print("data prev",data_prev)
######################Calculation##############################################
    z = []
    for i in range(category_length):
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
        sub = str(subcategory_unique[i]).strip('')
        print("SUB:",sub)
        x = {"User Group":subcategory_unique[i],"count":int(u1), "change%":res, "duration":durationtime}
        y = json.dumps(x)
        z.append(json.loads(y))
        print(z)
        row_json = json.dumps(z)

    return row_json

###############################################################################
