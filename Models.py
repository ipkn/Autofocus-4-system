from google.appengine.ext import db

class BacklogInfo(db.Model):
	user = db.UserProperty()
	didBacklog = db.BooleanProperty()
	firstBacklog = db.BooleanProperty()

class CompletedTodo(db.Model):
	user = db.UserProperty()
	date_added = db.DateTimeProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	text = db.StringProperty()
	detail = db.StringProperty(multiline=True)

class Todo(db.Model):
	user = db.UserProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	text = db.StringProperty()
	detail = db.StringProperty(multiline=True)
	current = db.BooleanProperty(default=False)
	review = db.BooleanProperty(default=False)
	backlog = db.BooleanProperty(default=False)

