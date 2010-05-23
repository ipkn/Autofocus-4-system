from Models import *
from Page import *

class CurrentPage(Page):
	def CompleteBacklog(self):
		'Insert new backlog at the end of the list.'
		query = Todo.gql('WHERE user = :1 AND backlog = TRUE', self.user)
		for x in query:
			x.delete()
		Todo(
			user = self.user,
			backlog = True
			).put()
		self.ResetBacklogInfo()


	def SelectFirstWork(self, first = True, ignore_review = False):
		if ignore_review:
			query = Todo.gql('WHERE user = :1 AND review = FALSE ORDER BY date LIMIT 1', self.user)
		else:
			query = Todo.gql('WHERE user = :1 ORDER BY date LIMIT 1', self.user)

		firstWork = query.get()

		if firstWork is None:
			# nothing to do now !
			#self.redirect('/add&msg=Add+anything+to+do+first!')
			self.ResetBacklogInfo()
			self.redirect('/add')
			return

		if firstWork.backlog:
			if not first:
				self.redirect('/add')
				return
			self.CompleteBacklog()
			return self.SelectFirstWork(False)

		self.ResetBacklogInfo()
		return firstWork

	def SelectNextWork(self, date):
		query = Todo.gql('WHERE user = :1 AND date > :2 ORDER BY date LIMIT 2', self.user, date)
		result = query.fetch(2)
		nextWork = None
		if len(result) >= 1:
			nextWork = result[0]
		nextnextWork = None
		if len(result) >= 2:
			nextnextWork = result[1]

		if nextWork is None:
			return self.SelectFirstWork(self)
		elif nextWork.backlog:
			# TODO
			info = BacklogInfo.gql('WHERE user = :1', self.user).get()
			if info is None:
				info = BacklogInfo(
					user = self.user,
					didBacklog = True,
					firstBacklog = False)
			if info.didBacklog:
				# go first of backlog
				self.UpdateBacklogNotFirst()
				return self.SelectFirstWork()
			elif info.firstBacklog:
				# make all list of backlog into review
				for todo in Todo.gql("WHERE user = :1 AND date < :2", self.user, nextWork.date):
					if not todo.review:
						todo.review = True
						todo.put()
				self.CompleteBacklog()
				self.ResetBacklogInfo()
				return nextnextWork or self.SelectFirstWork(ignore_review = True)
			else:
				# go first of active list
				self.ResetBacklogInfo()
				return nextnextWork or self.SelectFirstWork()
		else:
			return nextWork

	def render(self):
		query = db.GqlQuery("SELECT * FROM Todo WHERE user = :1 AND current = TRUE ORDER BY date", self.user)
		currentWork = query.get()

		if currentWork is None:
			currentWork = self.SelectFirstWork()
			if not currentWork:
				return

		# now currentWork is current 
		detail = currentWork.detail or ''
		action = self.request.get('action')
		if action == 'complete' or action == 'reenter':
			# delete currentWork
			CompletedTodo(
				user = currentWork.user,
				date_added = currentWork.date,
				text = currentWork.text,
				detail = currentWork.detail,
				).put()

			if action == 'reenter':
				Todo(
					user = currentWork.user,
					text = currentWork.text,
					detail = currentWork.detail,
					).put()

			# select next work as current
			date = currentWork.date
			currentWork.delete()
			currentWork = self.SelectNextWork(date)
			self.UpdateBacklogDid()
		elif action == 'skip':
			currentWork.current = False
			currentWork.put()
			currentWork = self.SelectNextWork(currentWork.date)
		if currentWork:
			if currentWork.current != True:
				currentWork.current = True
				currentWork.put()
			page = 'current.html'
			if currentWork.review:
				page = 'review.html'

			self.response.out.write(template.render(page,
				dict(
					work = currentWork,
					detail = detail
					)))
