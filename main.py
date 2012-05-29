#!/usr/bin/env python
import webapp2	# web application framework
import jinja2	# template engine
import os		# access file system
import datetime
import calendar
import urllib
import cgi
from google.appengine.api import users	# Google account authentication
from google.appengine.ext import db		# datastore

# initialize template
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Contact(db.Expando):
	''' User data model '''
	pid = db.StringProperty(required=True)
	name = db.StringProperty(required=True)
	email = db.EmailProperty(required=True)
	datefrom1 = db.DateTimeProperty(required=False)
	dateto1 = db.DateTimeProperty(required=False)
	country1 = db.StringProperty(required=False)
	transit1 = db.StringProperty()
	datefrom2 = db.DateTimeProperty(required=False)
	dateto2 = db.DateTimeProperty(required=False)
	country2 = db.StringProperty(required=False)
	transit2 = db.StringProperty()
	datefrom3 = db.DateTimeProperty(required=False)
	dateto3 = db.DateTimeProperty(required=False)
	country3 = db.StringProperty(required=False)
	transit3 = db.StringProperty()

class MainHandler(webapp2.RequestHandler):
	''' Home page handler '''
	def get(self):
		''' Show home page '''
        # check if valid Google account
		user = users.get_current_user()

		if user:	# if valid logged in user
			# logout link
			url = users.create_logout_url(self.request.uri)
			# logout text
			url_linktext = 'logout'
			# retrieve user record
			query = Contact.gql('WHERE pid = :1', user.nickname())
			# get 1 record
			result = query.fetch(1)
			if result:	# if user record found
				contact = result[0]
				greeting = ("Hello %s!" % (contact.name,))
			else:		# not found
				contact = "Invalid dhs.sg user"
				greeting = ""

		else: 		# not logged in
			# login link
			url = users.create_login_url(self.request.uri)
			# login text
			url_linktext = 'login'	
			contact = "Not authorized"
			greeting = "You need to"

		template_values = {
			'contact': contact,
			'greeting': greeting,
			'url': url,
			'url_linktext': url_linktext
		}
		
		# create index.html template
		template = jinja_environment.get_template('index.html')
		# associate template values with template
		self.response.out.write(template.render(template_values))

class UpdateHandler(webapp2.RequestHandler):
	''' Update contact '''
	def post(self):
		if self.request.get('update'):
			# get data from form controls
			updated_datefrom1 = self.request.get('datefrom1')
			updated_dateto1 = self.request.get('dateto1')
			updated_country1 = self.request.get('country1')
			updated_transit1 = self.request.get('transit1')
			updated_datefrom2 = self.request.get('datefrom12')
			updated_dateto2 = self.request.get('dateto2')
			updated_country2 = self.request.get('country2')
			updated_transit2 = self.request.get('transit2')
			updated_datefrom3 = self.request.get('datefrom3')
			updated_dateto3 = self.request.get('dateto3')
			updated_country3 = self.request.get('country3')
			updated_transit3 = self.request.get('transit3')
			# get user to update
			user = users.get_current_user()
			if user:
				url = users.create_logout_url(self.request.uri)
				url_linktext = 'Logout'
				query = Contact.gql('WHERE pid = :1', user.nickname())
				result = query.fetch(1)
				if result: #user found, update
					contact = result[0]
					contact.datefrom1 = updated_datefrom1
					contact.dateto1 = updated_dateto1
					contact.country1 = updated_country1
					contact.transit1 = updated_transit1
					contact.datefrom2 = updated_datefrom2
					contact.dateto2 = updated_dateto2
					contact.country2 = updated_country2
					contact.transit2 = updated_transit2
					contact.datefrom3 = updated_datefrom3
					contact.dateto3 = updated_dateto3
					contact.country3 = updated_country3
					contact.transit3 = updated_transit3
					contact.put()
				else:	#user not found, error
					self.response.write('Update failed :( ')
		
		
		template_values = {
			'contact':contact,
			'greeting':greeting,
			'url':url_linktext,
			'url_linktext':url_linktext,
			'contact.datefrom1' : updated_datefrom1,
			'contact.dateto1' : updated_dateto1,
			'contact.country1' : updated_country1,
			'contact.transit1' : updated_transit1,
			'contact.datefrom2' : updated_datefrom2,
			'contact.dateto2' : updated_dateto2,
			'contact.country2' : updated_country2,
	 		'contact.transit2' : updated_transit2,
			'contact.datefrom3' : updated_datefrom3,
			'contact.dateto3' : updated_dateto3,
			'contact.country3' : updated_country3,
			'contact.transit3' : updated_transit3,
			}
		
		template = jinja_environment.get_template('index.html/#view')                
		self.response.out.write(template.render(template_values))
		

#main
app = webapp2.WSGIApplication([('/', MainHandler),
								('/update',UpdateHandler),
								]
								,debug=True)
contact1 = Contact(pid='liu.yunzhu',name='LIU YUNZHU', email='liu.yunzhu@dhs.sg', datefrom1='', dateto1='', country1='hi', transit1='nil')
contact1.put()
