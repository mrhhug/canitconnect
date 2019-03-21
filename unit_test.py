#!/usr/bin/python

import unittest
from main import app
 
class Test(unittest.TestCase):
 
	def setUp(self):
		self.app = app.test_client()
 
	def test_index(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)

	def test_traceroute(self):
		response = self.app.get('/api/traceroute/localhost')
		self.assertEqual(response.status_code, 200)
 
	def test_telnet(self):
		response = self.app.get('/api/telnet/localhost/22')
		self.assertEqual(response.status_code, 200)
 
	def test_curl(self):
		data = '{"url":"https://www.fiserv.com", "method":"GET"}'
		headers = dict([("Content-Type","application/json")])
		response = self.app.post('/api/curl', data=data,  headers=headers)
		self.assertEqual(response.status_code, 200)

	def test_envVars(self):
		response = self.app.get('/api/getenv')
		self.assertEqual(response.status_code, 200)

	def test_set_http_proxy(self):
		data = '{"data":""}'
		headers = dict([("Content-Type","application/json")])
		response = self.app.post('/api/setenv/http_proxy', data=data,  headers=headers)
		self.assertEqual(response.status_code, 200)

	def test_set_https_proxy(self):
		data = '{"data":""}'
		headers = dict([("Content-Type","application/json")])
		response = self.app.post('/api/setenv/https_proxy', data=data,  headers=headers)
		self.assertEqual(response.status_code, 200)
		
	def test_set_no_proxy(self):
		data = '{"data":""}'
		headers = dict([("Content-Type","application/json")])
		response = self.app.post('/api/setenv/no_proxy', data=data,  headers=headers)
		self.assertEqual(response.status_code, 200)

	def test_unset_proxy_vars(self):
		response = self.app.put('/api/unsetproxyvars')
		self.assertEqual(response.status_code, 200)

	def test_get_datetime(self):
		response = self.app.get('/api/datetime')
		self.assertEqual(response.status_code, 200)
if __name__ == '__main__':
    unittest.main()
