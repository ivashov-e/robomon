#!flask/bin/python
from flask import Flask, json, jsonify, request, Response
from flask_cors import CORS
import sys, time, datetime, requests, re
import mysql.connector
from mysql.connector import Error

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    robot_id = request.args.get('roboid')
    placeid = request.args.get('placeid')
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    product = request.args.get('product')
    if robot_id == '':
        robot_id = 'ANY (select robotid from ztta_robots)'
#    else:
#        sql = 'select robotid from ztta_robots where robotname = "' + str(robot_id) + '"'
#        robot_db_id = dbrd(sql)[0]
#        robot_id = robot_db_id[0]
#        print robot_id
    if placeid == '':
        placeid = 'ANY (select place from ztta_robots)'
    else:
        placeid = "'"+str(placeid)+"'"
    if product == '':
        product = 'ANY (select progname from ztta_robometr)'
    else:
        product = "'"+str(product)+"'"
    if starttime == '':
        starttime = time.time() - 86400
    if endtime == '':
        endtime = time.time()
#    sql = "select ztta_robots.place, ztta_robots.robotname, ztta_robometr.progname from ztta_robometr where ztta_robots.place= "+placeid+" and ztta_robots.robotid = "+  str(robot_id) +" and eventdate between "+ str(starttime)+" and "+str(endtime)+" and robotstatus = 'e' and progname = "+str(product)+" group by progname;"
    sql = "select ztta_robots.place, ztta_robometr.progname, count(ztta_robometr.progname) from ztta_robometr left join ztta_robots on ztta_robots.robotid=ztta_robometr.robotid where eventdate between "+ str(starttime)+" and "+str(endtime)+" and robotstatus = 'e' and progname = "+str(product)+" and  ztta_robots.place = "+placeid+" group by ztta_robometr.progname;"
    print sql
    myresult = dbrd(sql)
    print myresult
    ret=[]
    for tmpres in myresult:
        robo = {
            'workshop': tmpres[0],
#            'machine': str(tmpres[1]),
            'product': tmpres[1],
            'count': tmpres[2]
            #'end_time': tmpres[3],
             }
        ret.append(robo)
    return json.dumps({'mydata': ret},ensure_ascii=False, sort_keys=False)    


@app.route("/graphtotal")
def graphtotal():
    robot_id = request.args.get('roboid')
    placeid = request.args.get('placeid')
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
#    product = request.args.get('product')
    if robot_id == '':
#        roboidsql= 'select robotid from ztta_robots;'
#        robotslist=dbrd(roboidsql)
#        print robotslist
        robot_id = 'ANY (select robotid from ztta_robots)'
    else:
        sql = 'select robotid from ztta_robots where robotname = "' + str(robot_id) + '"'
        robot_db_id = dbrd(sql)[0]
        robot_id = robot_db_id[0]
        #robotslist = robot_id
        print robot_id
        
    if placeid == '':
        placeidsql= 'select place from ztta_robots;'
        placelist=dbrd(placeidsql)
        print placelist        
        placeid = 'ANY (select place from ztta_robots)'
    else:
        placeid = "'"+str(placeid)+"'"
        placelist = placeid
    
    if starttime == '':
        starttime = time.time() - 86400
    if endtime == '':
        endtime = time.time()
    ret=[]
    sql = "select ztta_robots.place, ztta_robots.robotname, count(ztta_robometr.robotid) from ztta_robometr left join ztta_robots on ztta_robots.robotid=ztta_robometr.robotid where eventdate between "+ str(starttime)+" and "+str(endtime)+" and robotstatus = 'u' and  ztta_robots.place = "+placeid+" and ztta_robots.robotid = "+str(robot_id)+" group by ztta_robots.robotname;"
    print sql
    myresult = dbrd(sql)
    ret=[]
    for tmpres in myresult:
        robo = {
            'workshop': tmpres[0],
            'machine': str(tmpres[1]),
            'count': tmpres[2]
             }
        ret.append(robo)
    return json.dumps({'mydata': ret},ensure_ascii=False, sort_keys=False)    


@app.route("/graph")
def graph():
    robot_id = request.args.get('roboid')
    placeid = request.args.get('placeid')
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
#    product = request.args.get('product')
    if robot_id == '':
        roboidsql= 'select robotid from ztta_robots;'
        robotslist=dbrd(roboidsql)
        print robotslist
        robot_id = 'ANY (select robotid from ztta_robots)'
    else:
        sql = 'select robotid from ztta_robots where robotname = "' + str(robot_id) + '"'
        #robot_db_id = dbrd(sql)[0]
        #robot_id = robot_db_id[0]
        robotslist = robot_id
        print robot_id
        
    if placeid == '':
        placeidsql= 'select place from ztta_robots;'
        placelist=dbrd(placeidsql)
        print placelist        
        placeid = 'ANY (select place from ztta_robots)'
    else:
        placeid = "'"+str(placeid)+"'"
        placelist = placeid
    
    if starttime == '':
        starttime = time.time() - 86400
    if endtime == '':
        endtime = time.time()
        
#    for i in range(len(robotslist)):
#        print ''.join(robotslist[i])
#        sql = "select ztta_robots.place, ztta_robots.robotname, ztta_robometr.progname, ztta_robometr.eventdate from ztta_robometr left join ztta_robots on ztta_robots.robotid=ztta_robometr.robotid where ztta_robots.place= "+placeid+" and ztta_robots.robotid = "+  ''.join(robotslist[i]) +" and eventdate between "+ str(starttime)+" and "+str(endtime)+" and robotstatus = 'u';"
#        print sql
#        robotres = dbrd(sql)
#        print robotres

    ret=[]
    sql = "select ztta_robometr.eventdate from ztta_robometr left join ztta_robots on ztta_robots.robotid=ztta_robometr.robotid where ztta_robots.robotid = (select robotid from ztta_robots where ztta_robots.robotname = '"+  str(robot_id) +"') and eventdate between "+ str(starttime)+" and "+str(endtime)+" and robotstatus = 'u';"
    print sql
    myresult = tuple(dbrd(sql))
    endtimetuple = ()
    for tmpres in range(len(myresult)):
        endtimetuple = tuple(myresult[tmpres])
    etimestr=''
    for tt, item in enumerate(myresult):
        etimestr=etimestr + str(item)
    etimestr = re.sub('[()]', ' ', etimestr)
    placeid = "select place from ztta_robots where robotname='" + str(request.args.get('roboid')) + "';" 
    placeid = dbrd(placeid)[0]
    placeid = ''.join(placeid)
    #placeid = str(placeid
    print placeid
    robo1 =  {'workshop': placeid,
            'machine': request.args.get('roboid'),
            'end_time': [etimestr]
    #            ret.append(robo1)
        }
    ret.append(robo1)
    return json.dumps({'mydata': ret},ensure_ascii=False, sort_keys=False) 



@app.route('/snd', methods=['POST'])
def snd():
    if request.is_json:
        content = request.get_json()
        ts = time.time()
        print content
        try:
            if content['robotstatus'] == 'e':
                chkdbsql = "select id, rtmstmp from ztta_robometr where rtmstmp = " + str(content['timeid'])+ ";"
                dbchk = dbrd(chkdbsql)
                print "Check status: ", dbchk
                if dbchk == []:
                    sql = "select product from ztta_products where progname = '"+ str(content['progid'])+"' and ucount = "+ str(content['count'])+" ;"
                    prodname = dbrd(sql)
                    print "Product: ", prodname
                    if prodname != []:
                        prodname = prodname[0]
                        print prodname
                        sql = "INSERT INTO ztta_robometr (robotid, progname, robotspeed, robotstatus, rtmstmp, ucount, eventdate) VALUES ('" + str(content['robotid']) + "', '" + str(prodname[0]) + "', '" + str(content['robotspeed'])+ "', '" + str(content['robotstatus']) +"', '"+ str(content['timeid'])+"', '"+ str(content['count'])+"', '"+ str(ts)+"');"
                        print sql
                        dbwrt(sql)
                    else:
                        sql = "INSERT INTO ztta_robometr (robotid, progname, robotspeed, robotstatus, rtmstmp, ucount, eventdate) VALUES ('" + str(content['robotid']) + "', '" + str(content['progid']) + "', '" + str(content['robotspeed'])+ "', '" + str(content['robotstatus']) +"', '"+ str(content['timeid'])+"', '"+ str(content['count'])+"', '"+ str(ts)+"');"
                        print sql
                        dbwrt(sql)
                else:
                    print 'Dont repeat!!!'
            else:
                sql = "INSERT INTO ztta_robometr (robotid, progname, robotspeed, robotstatus, ucount, eventdate) VALUES ('" + str(content['robotid']) + "', '" + str(content['progid'])+ "', '" + str(content['robotspeed'])+ "', '" + str(content['robotstatus']) +"', '"+ str(content['count'])+"', '"+ str(ts)+"');"
                dbwrt(sql)
            return 'Done'
        except:
            return Response('Wrong', status=500)
    else:
        return 'Is not JSON'

def dbwrt(query):
    try:
        mydb.ping(reconnect=True, attempts=5, delay=1)
        mycursor = mydb.cursor()
        mycursor.execute(query)
        mydb.commit()
    except Error as e:
        print ("Error with mysql",e)
#    finally:
#        if(mydb.is_connected()):
#            mydb.close()
#            print("connection closed")
            

def dbrd(query):
    try:
        mydb.ping(reconnect=True, attempts=5, delay=1)
        mycursor = mydb.cursor()
        mycursor.execute(query)
        retresult = mycursor.fetchall()
        return retresult
    except Error as e:
        print ("Error with mysql",e)
#    finally:
#        if(mydb.is_connected()):
#            mydb.close()
#            print("connection closed")    


mydb = mysql.connector.connect(
    host="localhost",
    user="robouser",
    passwd="robopass",
    database="robotmon",
    charset="utf8",
    use_unicode=True
    )

print(mydb) 

app.run(host='0.0.0.0', port=5005)