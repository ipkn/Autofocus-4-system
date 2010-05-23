from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

from Page import Page
from AddPage import AddPage
from ListPage import ListPage
from CurrentPage import CurrentPage

class MainPage(Page):
	def render(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('Hello, webapp World!')

application = webapp.WSGIApplication(
                                     [('/', ListPage),
                                     ('/add', AddPage),
                                     ('/list', ListPage),
                                     ('/review', MainPage),
                                     ('/current', CurrentPage),
									 ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
