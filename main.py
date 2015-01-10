from google.appengine.api import app_identity
from google.appengine.api import urlfetch

import json
import webapp2


COMPUTE_SCOPE = 'https://www.googleapis.com/auth/compute'
STORAGE_SCOPE = 'https://www.googleapis.com/auth/devstorage.full_control'

PROJECT = 'sauer-cloud'
ZONE = 'us-central1-a'
DISK = 'mc'
STARTUP_SCRIPT_URL='gs://sauer-cloud/mc-startup-script.sh'
SERVICE_ACCOUNT_EMAIL = app_identity.get_service_account_name()

API_V1_URL = 'https://www.googleapis.com/compute/v1'
PROJECT_URL = API_V1_URL + '/projects/' + PROJECT
PROJECT_ZONE_URL = PROJECT_URL + '/zones/' + ZONE
PROJECT_GLOBAL_URL = PROJECT_URL + '/global'
DISK_URL = PROJECT_ZONE_URL + '/disks/' + DISK
INSTANCES_URL = PROJECT_ZONE_URL + '/instances'
MACHINE_TYPE = PROJECT_ZONE_URL + '/machineTypes/g1-small'
NETWORK = PROJECT_GLOBAL_URL + '/networks/mc'

class PingHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('OK.')


class CreateInstanceHandler(webapp2.RequestHandler):
  def post(self):
    payload = {
      'name': 'mc',
      'machineType': MACHINE_TYPE,
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
        'email': SERVICE_ACCOUNT_EMAIL,
        'scopes': [STORAGE_SCOPE],
      }],
      'networkInterfaces': [{
        'network': NETWORK,
      }],
    }

    authorization_token, _ = app_identity.get_access_token(COMPUTE_SCOPE)
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'OAuth ' + authorization_token,
    }

    url = INSTANCES_URL
    result = urlfetch.fetch(url,
      payload=json.dumps(payload),
      method='POST',
      headers=headers,
      follow_redirects=False,
      deadline=60,
      validate_certificate=True)

    pretty_payload=json.dumps(payload, indent=2)
    pretty_headers=json.dumps(headers, indent=2)

    self.response.headers['Content-Type'] = 'text/plain'
    if result.status_code == 200:
      self.response.write('OK. Instance created.\n\n')
    else:
      self.response.status_int = result.status_code
      self.response.write('RESPONSE ERROR CODE:\n{}\n\n'.format(result.status_code))
      self.response.write('RESPONSE BODY:\n{}\n\n'.format(result.content))
    self.response.write('-' * 80 + '\n\n')
    self.response.write('REQUEST URL:\n{}\n\n'.format(url))
    self.response.write('REQUEST HEADERS:\n{}\n\n'.format(pretty_headers))
    self.response.write('REQUEST PAYLOAD:\n{}\n\n\n'.format(pretty_payload))


class DeleteInstanceHandler(webapp2.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('OK. Instance DELETED.')


APPLICATION = webapp2.WSGIApplication([
    ('/api/ping', PingHandler),
    ('/api/create-instance', CreateInstanceHandler),
    ('/api/delete-instance', DeleteInstanceHandler),
], debug=True)
