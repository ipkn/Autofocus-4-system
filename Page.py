from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from Models import *

class Page(webapp.RequestHandler):
	def UpdateBacklogDid(self):
		q = BacklogInfo.gql("WHERE user = :1", self.user)
		info = q.get()
		if info:
			info.didBacklog = True
			info.put()
		else:
			BacklogInfo(
				user = user,
				didBacklog = True,
				firstBacklog = False,
				).put()

	def UpdateBacklogNotFirst(self):
		q = BacklogInfo.gql("WHERE user = :1", self.user)
		info = q.get()
		if info:
			info.firstBacklog = False
			info.put()
		else:
			BacklogInfo(
				user = user,
				didBacklog = False,
				firstBacklog = False,
				).put()
		
	def ResetBacklogInfo(self, did=False, first=True):
		user = users.get_current_user()
		# init backlog information to first loop
		q = BacklogInfo.gql("WHERE user = :1", user)
		info = q.get()
		if info:
			info.didBacklog = did
			info.firstBacklog = first
			info.put()
		else:
			BacklogInfo(
				user = user,
				didBacklog = did,
				firstBacklog = first,
				).put()

		q = Todo.gql("WHERE user = :1 AND backlog = TRUE", user)
		backlog = q.get()
		if backlog is None:
			Todo(
				user = user,
				backlog = True
				).put()

	def get(self):
		self.user = user = users.get_current_user()

		if user:
			self.response.out.write(template.render('header.html',{}))
			self.render()
			self.response.out.write(template.render('footer.html',{}))
		else:
			self.redirect(users.create_login_url(self.request.uri)) 
