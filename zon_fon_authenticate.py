import urllib, urllib2
from urlparse import urlparse, parse_qs
from urllib import urlencode
from os import getenv
import sys

FON_USERNAME = getenv('FON_USERNAME')
FON_PASSWORD = getenv('FON_PASSWORD')

START_URL = 'http://www.speedtest.net'

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
urllib2.install_opener(opener)
data = urllib2.urlopen(START_URL)
auth_url = data.geturl()
if not auth_url.startswith('https://zon.portal.fon.com/'):
	print "Zon fon authentication was not requested. Already authenticated?"
	sys.exit(1)

url_data = parse_qs(urlparse(auth_url).query, keep_blank_values=True)
fields = [ 'nasid', 'uamip', 'uamport', 'mac', 'challenge' ]
str_data = 'res=login'
for f in fields:
	str_data += '&%s=%s' % (f, url_data[f][0])
str_data += '&tab=2'
url = "%s://%s%s?%s" % (urlparse(auth_url).scheme, urlparse(auth_url).netloc, urlparse(auth_url).path, str_data)
html = urllib2.urlopen(url,
 data=urllib.urlencode({'USERNAME': FON_USERNAME, 'PASSWORD': FON_PASSWORD}))
html_data = html.read()
if 'Incorrect username or password' in html_data:
	print "Login failed, check username/password!"
elif "'You're connected!":
	print "You are now connected"
else:
	print "Something failed"
