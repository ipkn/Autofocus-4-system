from Models import *
from Page import *

class AddPage(Page):
	def render(self):
		if self.request.get('text'):
			todo = Todo()
			todo.user = self.user
			todo.text = self.request.get('text')
			todo.put()

			self.redirect('/current')
		else:
			self.response.out.write(template.render('add.html',{}))

