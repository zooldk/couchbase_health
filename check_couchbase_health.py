#!/usr/bin/python
#
# python check_couchbase_health.py -H [SERVER] -p 8091 --url /pools/default -u [USER] -P [PASSWORD]

import urllib,urllib2, base64, sys, os

try:
  import json
  json  # workaround for pyflakes issue #13
except ImportError:
  import simplejson as json
from optparse import OptionParser

UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2

parser = OptionParser()
parser.add_option('-H', '--hostname', dest='hostname')
parser.add_option('-r', '--url', dest='url')
parser.add_option('-u', '--user', dest='user')
parser.add_option('-P', '--password', dest='password')
parser.add_option('-p', '--port', dest='port', help="""ex: 8080""")
parser.add_option('-w', '--warning', dest='warning', help="""ex: 5""")
parser.add_option('-c', '--critical', dest='critical', help="""ex: 10""")

options, args = parser.parse_args()
test_url = 'http://%s:%s%s' % (options.hostname, options.port, options.url)

request = urllib2.Request(url=test_url) 
if options.user:
    #base64string = base64.encodestring('%s:%s' % (options.user, options.password)).replace('\n', '')
    #request.add_header("Authorization", "Basic %s" % base64string)
    request.add_header("Content-Type",'application/json')
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, "api.foursquare.com", options.user, options.password)
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))

try:
  f = urllib2.urlopen(request)
except urllib2.HTTPError, err:
  print("%s: %s", options.url, err)
  raise SystemExit, WARNING

data = json.loads(f.read())
nodes = data["nodes"]
for node in nodes:
  #print("node: " + node["status"])
  if node["status"] == "healthy":
    print 'Check Ok'
    raise SystemExit, OK
  else:
    raise SystemExit, CRITICAL
