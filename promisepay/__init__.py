
import requests
import base64
import json


import os
from distutils.util import strtobool

def auth(username,secret,is_production=False):
	os.environ['PROMISE_PAY_SECRET'] = secret
	os.environ['PROMISE_PAY_KEY'] = username 
	os.environ['is_production'] = str(is_production)
	



class PromisePay(object):


	
	def __init__(self):

		try:
			from django.conf import settings

			self.password = settings.PROMISE_PAY_SECRET
			self.username = settings.PROMISE_PAY_KEY

			self.is_production = getattr(settings, "PROMISE_PAY_IS_PROD", False)


			if self.is_production:
				self.MASTER_URL = 'https://api.promisepay.com/'
			else:
				self.MASTER_URL = 'https://test.api.promisepay.com/'


			self.AUTH = 'Basic '+base64.b64encode(settings.PROMISE_PAY_KEY+':'+settings.PROMISE_PAY_SECRET)
			self.HEADERS = {'Authorization': self.AUTH,"Content-Type": "application/json"}


		except:

			if not os.environ.has_key('PROMISE_PAY_SECRET') or not os.environ.has_key('PROMISE_PAY_KEY'):
				raise Exception('Make sure you have imported auth from promisepay import auth , And set username and password secret ')

			self.username = os.environ.get('PROMISE_PAY_KEY')  
			self.password = os.environ.get('PROMISE_PAY_SECRET')  
			self.is_production =  bool(strtobool(str(os.environ.get('is_production'))))
			
			if self.is_production:
				self.MASTER_URL = 'https://api.promisepay.com/'
			else:
				self.MASTER_URL = 'https://test.api.promisepay.com/'


			self.AUTH = 'Basic '+base64.b64encode(self.username+':'+self.password)
			self.HEADERS = {'Authorization': self.AUTH,"Content-Type": "application/json"}

		
			

	def get_list(self,path,limit=10,offset=0):

		self.limit = limit
		self.path=path
		self.offset=offset

		payload = {'limit': self.limit, 'offset': self.offset}

		r = requests.get(self.MASTER_URL+self.path, headers=self.HEADERS,params=payload)
		
		if r.json().has_key('meta'):
			return r.json()
		
		else:
			try:
				
				if r.status_code == 503:
					return {'errors':'Service is down'}
				else:
					return r.json()
			except:
				raise Exception(r.json())


	def get_one(self,path,id=None):
		

		if id:
			r = requests.get(self.MASTER_URL+path+'/'+id, headers=self.HEADERS)

		else:
			r = requests.get(self.MASTER_URL+path+'/', headers=self.HEADERS)
		
		if r.status_code == 503:
			return {'errors':'Service is down'}
		
		else:
			print r.json()
			return r.json()



	def delete_one(self,path,id=None):
		
		
		if id:
			r = requests.delete(self.MASTER_URL+path+'/'+id, headers=self.HEADERS)

		else:
			r = requests.delete(self.MASTER_URL+path+'/', headers=self.HEADERS)
		

		print "SCODE",r.status_code

		if r.status_code == 200:
			return r.json()

	
		if r.status_code == 503:
			return {'errors':'Service is down'}
		
		else:
			return {'errors':'Something went wrong with service provider'}
		



	def add_one(self,path,data=None):
	
		r = requests.post(self.MASTER_URL+path, headers=self.HEADERS,data=json.dumps(data))


		if r.status_code == 201:
			return r.json()

		elif r.status_code ==  401:
			raise Exception('Authorization error')


		if r.status_code == 503:
			return {'errors':'Service is down'}
		else:
			return r.json()


	def edit_one(self,path,id,data):

		r = requests.patch(self.MASTER_URL+path+'/'+id, data=json.dumps(data),headers=self.HEADERS)

		return r
