import webapp2


class PingHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('OK.')


class CreateInstanceHandler(webapp2.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('OK. Instance created.')


class DeleteInstanceHandler(webapp2.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('OK. Instance DELETED.')


APPLICATION = webapp2.WSGIApplication([
    ('/api/ping', PingHandler),
    ('/api/create-instance', CreateInstanceHandler),
    ('/api/delete-instance', DeleteInstanceHandler),
], debug=True)
