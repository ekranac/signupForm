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

    def verify_username(self, username):
        count_error = 0
        username_args = {}
        if username=="":
            username_args["username_error"]="Empty field"
            count_error += 1
        else:
            listed_username = list(username)
            for letter in listed_username:
                if (letter.isalpha()==False) and (letter.isdigit()==False):
                    username_args["username_error"] = "Invalid username"
                    count_error += 1

        if count_error==0:
            return False
        else:
            return username_args



    def verify_passwords(self, password, vpassword):
        count_error = 0
        password_args = {}
        if password=="" or vpassword=="":
            password_args["pass_error"]="Empty"
            password_args["vpass_error"]="Empty"
            count_error += 1

        else:
            listed_pass = list(password)
            listed_vpass = list(vpassword)

            if password!=vpassword:
                password_args["pass_error"]="Passwords don't match"
                password_args["vpass_error"] = "Passwords don't match"
                count_error += 1

        if count_error==0:
            return False
        else:
            return password_args

    def verify_email(self, email):
        count_error = 0
        email_args={}
        if email=="":
            email_args["email_error"]="Empy field"
            count_error += 1

        else:
            listed_email = list(email)
            if "@" not in listed_email:
                email_args["email_error"]="Not a valid email"
                count_error += 1

        if count_error==0:
            return False
        else:
            return email_args



    def get(self):
        self.render_template("index.html")


    def post(self):
        username = self.request.get("username")
        password = self.request.get("pass")
        vpassword = self.request.get("vpass")
        email = self.request.get("email")

        valid_username = self.verify_username(username)
        valid_password = self.verify_passwords(password, vpassword)
        valid_email = self.verify_email(email)

        if valid_username==False and valid_password==False and valid_email==False:
            self.redirect("/hello?username=" + username)
        else:
            #args = dict(valid_username.items() + valid_password.items() + valid_email.items())
            args = {}
            errors = [valid_username, valid_password, valid_email]
            for element in errors:
                if element!=False:
                    args.update(element)
            self.render_template("index.html", args)




class HelloPage(BaseHandler):
    def get(self):
        username = self.request.get("username")
        args = {"name":username}
        self.render_template("hello.html", args)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ("/hello", HelloPage)
], debug=True)