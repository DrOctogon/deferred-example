import jinja2
import logging
import os
import webapp2
from google.appengine.api import mail
from google.appengine.ext import deferred

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# Details for sending the deferred email
SENDER = "Test Sender <test@sender.com>"
SUBJECT = "Hello World"
BODY = "This message was sent 10 minutes after the user entered his/her email address"

# Time deferred before sending the email in seconds
EMAIL_DELAY = 600

class IndexPage(webapp2.RequestHandler):
  """ GET method that serves the index page
  """
  def get(self):
    template_values = {}
    template = jinja_environment.get_template("index.html")
    self.response.out.write(template.render(template_values))
  def post(self):
    """
    POST method for accepting email sign ups
    """
    email = self.request.get("email")
    email_delay(email=email)

def email_delay(email):
  """ Sends a delayed email to the user provided address
  """
  deferred.defer(send_email, email, _countdown=EMAIL_DELAY)

def send_email(email):
  """ Sends a delayed email to a person who has signed up.

  Args:
    email: The email to send to.
  """
  if not mail.is_email_valid(email): # only checks if non-empty
    return False
  try:
    mail.send_mail(SENDER, email, SUBJECT, BODY)
  except Exception, e:
    logging.error("Unable to send email to {0}: {1}".format(
      email, str(e)))
    return False

app = webapp2.WSGIApplication(
  [('/', IndexPage),])

