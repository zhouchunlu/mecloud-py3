#-*- coding: utf-8 -*- 
import urllib
from urllib import request

def post(url, headers, data):
	req = request.Request(url)
	for header in headers:
		req.add_header(header, headers[header])
	if data!=None:
		print(url)
		print(data)
		return request.urlopen(req, data).read()
	else:
		return request.urlopen(req).read()

def get(url):
	pass