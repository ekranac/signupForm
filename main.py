import webapp2
import os
from google.appengine.ext.webapp import template


class BaseHandler(webapp2.RequestHandler):
    def render_template(self, view_filename, params=None):
		if not params:
			params = {}
		path = os.path.join(os.path.dirname(__file__), 'templates', view_filename)
		self.response.out.write(template.render(path, params))




class MainPage(BaseHandler):
    def get(self):
        self.render_template("index.html")





application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)