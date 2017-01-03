import pycurl

class GetPage:
	def __init__ (self, url):
		self.contents = ''
		self.url = url

	def read_page (self, buf):
		self.contents = self.contents + buf

	def show_page (self):
		print self.contents
		return self.contents

name = 'test2'
target = GetPage("http://10.5.6.248:23456/pir/123123/in/1")

testcurl = pycurl.Curl()
testcurl.setopt(testcurl.URL, target.url)
testcurl.setopt(testcurl.WRITEFUNCTION, target.read_page)
testcurl.perform()
testcurl.close()

content = target.show_page()

print content[2]







