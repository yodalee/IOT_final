from bottle import route, run

@route('/hello')
def hello():
	return "Hello World!"

run(host='10.5.6.248', port=8080, debug=True)
