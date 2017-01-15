from bottle import route, run, template , request, response
import csv
import time
import os
import dataset


@route('/hello/<name>')
def test(name = 'default'):
    return template('Hello {{name}}!!!!!!!!!', name=name)

@route('/help')
@route('/help/')
@route('/help/<name>')
def test(name = 'menu'):
    if name == 'menu':
        output = '/pir/[dev_id]/in/[value]<br>' \
             + '/lightsensor/[dev_id]/in/[value]<br>' \
             + '/touchpad/[dev_id]/in/[value]<br>' \
             + '/regisit/[dev_id]/[ip]/[port]<br>' 
        return output

@route('/clean/<name>')
def clean(name = 'no'):
    if name == 'no':
        return 'need a name <br>'
    elif name == 'all':
        os.system('rm /home/cmlab/REST/data*.csv')
        return 'clean all data'

@route('/pir/<dev_id>/in/<value>')
def pir_in(dev_id = 'needID' , value = 0):
    f = open('data_pir_in_'+dev_id+'.csv','ab')
    w = csv.writer(f)
    timestamp=int(time.time())
    w.writerows([[value,timestamp]])
    f.close()
    return '['+value+', '+str(timestamp)+']'

@route('/lightsensor/<dev_id>/in/<value>')
def lightsensor_in(dev_id = 'needID' , value = 0):
    f = open('data_lightsensor_in_'+dev_id+'.csv','ab')
    w = csv.writer(f)
    timestamp=int(time.time())
    w.writerows([[value,timestamp]])
    f.close()
    return '['+value+', '+str(timestamp)+']'

@route('/touchpad/<dev_id>/in/<value>')
def touchpad_in(dev_id = 'needID' , value = 0):
    f = open('data_touchpad_in_'+dev_id+'.csv','ab')
    w = csv.writer(f)
    timestamp=int(time.time())
    w.writerows([[value,timestamp]])
    f.close()
    return '['+value+', '+str(timestamp)+']'

@route('/regisit/<dev_id/<ip>/<port>')
def regisit(dev_id , ip):
    f = open('data_dev_ip.csv','ab')
    w = csv.writer(f)
    w.writerows([[dev_id, ip, port]])
    f.close()

    db = dataset.connect('sqlite:///DB/iot_db.db')
    table = db['wukong_id_ip']
    try:
        table.insert(dict(deviceid = dev_id, deviceip = ip, deviceport = port))
        db.commit()
    except:
        print "Error at regist %s %s %s" %(dev_id,ip,port)
        db.rollback()

    return '['+dev_id+', '+ip+', '+port+']'


@route('/forum')
#/forum?devicetype=1&deviceid=22&value=333&timestamp=112233445
def getvar():
    devicetype_in = request.query.devicetype
    deviceid_in = request.query.deviceid
    value_in = request.query.value
    timestamp_in = int(time.time())
    db = dataset.connect('sqlite:///DB/iot_db.db')

    table = db['wukonginput']
    try:
        table.insert(dict(devicetype = devicetype_in,
                          deviceid = deviceid_in,
                          value = value_in,
                          timestamp = timestamp_in ))    
        
        db.commit()
    except:
        print "error at insert %d %d %d %d" %(devicetype,
                                              deviceid,
                                              value,
                                              timestamp)
        db.rollback()


    f = open('total.csv','ab')
    w = csv.writer(f)
    w.writerows([[devicetype_in,deviceid_in,value_in,timestamp_in]])
    f.close()

run(host='10.5.6.248', port=23456, debug=True)
