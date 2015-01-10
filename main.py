from google.appengine.api import urlfetch

import webapp2


COMPUTE_SCOPE = 'https://www.googleapis.com/auth/compute'
STORAGE_SCOPE = 'https://www.googleapis.com/auth/devstorage.full_control'

PROJECT = 'sauer-cloud'
ZONE = 'us-central1-a'
DISK = 'mc'
STARTUP_SCRIPT_URL='gs://sauer-cloud/mc-startup-script.sh'
NETWORK = 'mc'

API_V1_URL = 'https://www.googleapis.com/compute/v1'
PROJECT_URL = API_V1_URL + '/projects/' + PROJECT
PROJECT_ZONE_URL = PROJECT_URL + '/zones/' + ZONE
DISK_URL = PROJECT_ZONE_URL + '/disks/' + DISK
INSTANCES_URL = PROJECT_ZONE_URL + '/instances'


class PingHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('OK.')


class CreateInstanceHandler(webapp2.RequestHandler):
  def post(self):
    payload = {
      'name': 'mc',
      'machineType': 'g1-small',
      'disks': [{
        'deviceName': DISK,
        'source': DISK_URL,
        'mode': 'READ_WRITE',
        'boot': True,
      }],
      'metadata': {
        'items': [{
          'key': 'startup-script-url',
          'value': STARTUP_SCRIPT_URL,
        }],
      },
      'scheduling': {
        'automaticRestart': True,
        'onHostMaintenance': 'MIGRATE',
      },
      'serviceAccounts': [{
        'scopes': [STORAGE_SCOPE],
      }],
      'networkInterfaces': [{
        'network': NETWORK,
      }],
    };


    url =INSTANCES_URL + '/create'
    result = urlfetch.fetch(url,
      payload=payload,
      method='POST',
      headers={},
      follow_redirects=False,
      deadline=60,
      validate_certificate=True)

    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('URL:\n{}\n\n'.format(url))
    self.response.write('PAYLOAD:\n{}\n\n\n'.format(payload))
    if result.status_code == 200:
      self.response.write('OK. Instance created.')
    else:
      self.response.status_int = result.status_code
      self.response.write('ERROR CODE:\n{}\n\n'.format(result.status_code))
      self.response.write('RESPONSE BODY:\n{}\n\n'.format(result.content))


class DeleteInstanceHandler(webapp2.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('OK. Instance DELETED.')


APPLICATION = webapp2.WSGIApplication([
    ('/api/ping', PingHandler),
    ('/api/create-instance', CreateInstanceHandler),
    ('/api/delete-instance', DeleteInstanceHandler),
], debug=True)
