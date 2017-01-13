from bottle import route, run, template
import csv
import time
#from subprocess import call
import os



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
#	elif name == 'pir'

@route('/clean/<name>')
def clean(name = 'no'):
	if name == 'no':
		return 'need a name <br>'
	elif name == 'all':
		#call('rm /home/cmlab/REST/data*')
		os.system('rm /home/cmlab/REST/data*.csv')
		
		return 'clean all data'

@route('/pir/<dev_id>/in/<value>')
def pir_in(dev_id = 'needID' , value = 0):
	f = open('data_pir_in_'+dev_id+'.csv','ab')
        w = csv.writer(f)
	timestamp=int(time.time())
	#print timestamp
	w.writerows([[value,timestamp]])
	f.close()
	return '['+value+', '+str(timestamp)+']'

@route('/lightsensor/<dev_id>/in/<value>')
def lightsensor_in(dev_id = 'needID' , value = 0):
	f = open('data_lightsensor_in_'+dev_id+'.csv','ab')
        w = csv.writer(f)
	timestamp=int(time.time())
	#print timestamp
	w.writerows([[value,timestamp]])
	f.close()
	return '['+value+', '+str(timestamp)+']'


@route('/touchpad/<dev_id>/in/<value>')
def touchpad_in(dev_id = 'needID' , value = 0):
	f = open('data_touchpad_in_'+dev_id+'.csv','ab')
        w = csv.writer(f)
	timestamp=int(time.time())
	#print timestamp
	w.writerows([[value,timestamp]])
	f.close()
	return '['+value+', '+str(timestamp)+']'

@route('/regisit/<dev_id/<ip>/<port>')
def regisit(dev_id , ip):
	f = open('data_dev_ip.csv','ab')
	w = csv.writer(f)
	w.writerows([[dev_id, ip, port]])
	f.close()
	return '['+dev_id+', '+ip+', '+port+']'

run(host='10.5.3.92', port=23456, debug=True)
