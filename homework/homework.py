import webapp2
import cgi
import re

form = """
<b>Enter some text to ROT13:<b>
<br>
<form method="post">
    <textarea name="text" rows="8" cols="100">%s</textarea>
    <br>
    <input type="submit">
</form>
"""

class HomeWork1(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello, Udacity!")

class HomeWork2(webapp2.RequestHandler):
    def write_form(self, s=""):
        self.response.write(form % s)

    def get(self):
        self.write_form()

    def rot13(self, text):
        return "".join([c if not c.isalpha() else chr(ord(c) + 13) if (c >= 'a' and c < 'n')or(c >= 'A' and c < 'N') else chr(ord(c)-13) for c in text])

    def post(self):
        text = self.rot13(self.request.get("text"))
        text = cgi.escape(text, quote = True)
        self.write_form(text)

signup_form = """
<b>Sign up:<b><br>
<form method=post>
  <label>
    Username
    <input type="text" name="username" value="%(username)"><div style="color: red">%(username_error)</div>
  </label>
  <label>
    Password
    <input type="password" name="password" value="%(password)"><div style="color: red">%(password_error)</div>
  </label>
  <label>
    Verify Password
    <input type="password" name="verify" value="%(verify)"><div style="color: red">%(verify_error)</div>
  </label>
  <label>
    Email(optinal)
    <input type="text" name="email" value="%(email)"><div style="color: red">%(email_error)</div>
  </label>
  <br>
  <input type="submit">
</form>
"""

validates = {
    "username": re.compile(r"^[a-zA-Z0-9_-]{3,20}$"),
    "email": re.compile(r"^[\S]+@[\S]+\.[\S]+$"),
    "password": re.compile(r"^.{3,20}$")
}

errors = {
    "username": "That's not a valid username.",
    "email": "That's not a valid email.",
    "password": "That wasn't a valid password.",
    "verify": "Your password didn't match."
}

error_names = {
    "username": "username_error",
    "password": "password_error",
    "verify": "verify_error",
    "email": "email_error"
}

def valid_username(username):
    return USER_RE.match(username)

class UserSignup(webapp2.RequestHandler):
    def write_form(self, kv = {}):
        self.response.write(signup_form % kv)

    def get(self):
        self.write_form()

    def post(self):
        has_errors = {}
        values = {}
        for k in validates:
            values[k] = cgi.escape(self.request.get(k))
            if not (validates[k].match(values.get(k))):
                has_errors[error_names[k]] = errors[k]

        values["verify"] = cgi.escape(self.request.get("verify"))
        if values.get("password") != values.get("verify"):
            has_errors[error_names["verify"]] = errors["verify"]

        if has_errors:
            self.write_form(has_errors)
        else:
            self.redirect("/success")

class UserSignupSuccess(webapp2.RequestHandler):
    def get(self):
        self.response.write("success")


application = webapp2.WSGIApplication([
    ('/', HomeWork1),
    ('/unit2', HomeWork2),
    ('/signup', UserSignup),
    ('/success', UserSignupSuccess),
], debug=True)
