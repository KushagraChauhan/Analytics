'''Analytics with Cassandra Database'''

from flask import Flask, render_template, request, jsonify
import json
from flask_cqlalchemy import CQLAlchemy
import uuid
from multiprocessing import Value

app = Flask(__name__)
app.config['CASSANDRA_HOSTS'] = ['127.0.0.1']
app.config['CASSANDRA_KEYSPACE'] = "trial"
db = CQLAlchemy(app)

class Persons(db.Model):
    __keyspace__ = 'trial'
    uid = db.columns.UUID(primary_key = True, default = uuid.uuid4)
    name = db.columns.Text(primary_key = True)
    addr = db.columns.Text()
    count = db.columns.Text()

@app.route('/unique')
def show_user():
    for user in Persons.objects().all():
        print(user)
    return "hi"

class Count(db.Model):
    __keyspace__ = 'trial'
    id = db.columns.Integer(primary_key=True)
    count = db.columns.Integer()

counter = Value('i', 0)
@app.route('/count')
def index():
    #sync_table(Count)
    with counter.get_lock():
        counter.value += 1
        unique_count = counter.value
        Count.objects(id=1).update(count=unique_count)
    print(counter)

    return "hi"

class Ltime(db.Model):
    __keyspace__ = 'trial'
    id = db.columns.Integer(primary_key=True)
    time = db.columns.Text()
    zone = db.columns.Text()

@app.route('/loc', methods=['POST'])
def local_time():
    print("Local Time")
    rf=request.form
    print(rf)
    for key in rf.keys():
        data=key
    print('this is data-----',data)
    data_dic=json.loads(data)
    print('.............',data_dic.keys())
    loc_time = data_dic['time']
    print('((((((((',loc_time,')))))))')
    resp_dic={'time':loc_time,'msg':'local time'}
    resp = jsonify(resp_dic)
    resp.headers['Access-Control-Allow-Origin']='*'
    print('<<<<<<<<<',resp_dic,'>>>>>>>>>>>')
    for i in range(10):
        Ltime.objects(id=i).update(time=loc_time)
    return resp

@app.route('/zone', methods=['POST'])
def time_zone():
    print("Time Zone")
    rf=request.form
    print(rf)
    for key in rf.keys():
        data_zone=key
    print(data_zone)
    data_dic=json.loads(data_zone)
    print(data_dic.keys())
    time_zone = data_dic['zone']

    resp_dic={'zone':time_zone,'msg':'Time Zone'}
    resp = jsonify(resp_dic)
    resp.headers['Access-Control-Allow-Origin']='*'
    for i in range(10):
        Ltime.objects(id=i).update(zone=time_zone)
    return resp


class VDuration(db.Model):
    __keyspace__ = 'trial'
    id = db.columns.Integer(primary_key=True)
    timeSpent = db.columns.Integer()

@app.route('/visit', methods=['POST'])
def visit_duration():
    print("Visit Duration")
    rf=request.form
    print(rf)
    for key in rf.keys():
        data=key
    print(data)
    data_dic=json.loads(data)
    print(data_dic.keys())
    spentTime = data_dic['time']
    print(spentTime)
    #stime = spentTime +"ms"
    resp_dic={'spentTime':spentTime,'msg':'Time Spent'}
    resp = jsonify(resp_dic)
    #print(stime)
    resp.headers['Access-Control-Allow-Origin']='*'
    VDuration.objects(id=1).update(timeSpent=spentTime)
    return resp

if __name__ == '__main__':
    app.run(debug = True)
