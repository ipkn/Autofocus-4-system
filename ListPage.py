from Models import *
from Page import *

class ListPage(Page):
	def render(self):
		clist = []
		query = Todo.gql("WHERE user = :1 ORDER BY date DESC", self.user)
		todolist = []

		def action(todo, completed,can_become_current = False):
				d = dict(
					text = todo.text,
					can_become_current = can_become_current,
					current = (not completed) and todo.current,
					backlog = (not completed) and todo.backlog,
					completed = completed,
					review = (not completed) and todo.review,
				)
				todolist.append(d)

		if self.request.get('all') == '1':
			query2 = CompletedTodo.gql("WHERE user = :1 ORDER BY date DESC", self.user)
			#merge_with_action(query, lambda x: action(x, 0), query2, lambda x: action(x, 1))
			i1 = iter(query)
			i2 = iter(query2)
			try:
				todo1 = None
				todo1 = i1.next()
				todo2 = None
				todo2 = i2.next()
				while 1:
					if todo1.date > todo2.date:
						action(todo1, 0)
						todo1 = i1.next()
					else:
						action(todo2, 1)
						todo2 = i2.next()
			except StopIteration:
				try:
					if todo1:
						action(todo1, 0)
					while 1:
						todo = i1.next()
						action(todo, 0)
				except StopIteration:
					pass
				try:
					while 1:
						todo = i2.next()
						action(todo, 1)
				except StopIteration:
					pass
		else:
			for todo in query:
				action(todo, 0)

		todolist.reverse()

		self.response.out.write(template.render('list.html',{'todolist':todolist}))

