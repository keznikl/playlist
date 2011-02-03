import os
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models import *

from youtube import *
from gdata.youtube import YouTubeVideoEntry

def template_path(name):
	return os.path.join(os.path.dirname(__file__), 'templates/' + name)

class MainPage(webapp.RequestHandler):
	def get(self):
		greetings_query = Greeting.all().order('-date')
		greetings = greetings_query.fetch(10)
	
		for g in greetings:
			link = g.content[g.content.find("http://www.youtube.com"):]
			link = link[:link.find(" ")]
			if link == "":
				continue
			id = YoutubeIdFromURL(link)
			p = """<iframe title="YouTube video player"
width="480" height="390" src="http://www.youtube.com/embed/%s" frameborder="0"
allowfullscreen></iframe>""" % id
			g.content = p



		
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		
		user = users.get_current_user()
		template_values = {
			'greetings': greetings,
			'url': url,
			'url_linktext': url_linktext,
			'user': user,
		}		
		self.response.out.write(template.render(template_path('index.html'), template_values))
		

class Guestbook(webapp.RequestHandler):
	def post(self):
		greeting = Greeting()		
		if users.get_current_user():
			greeting.author = users.get_current_user()
		
		content = self.request.get('content')		
		greeting.content = content
		greeting.put()
		self.redirect('/')