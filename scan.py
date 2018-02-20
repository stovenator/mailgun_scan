"""View a message using its Mailgun storage key."""
import os
import sys
import json

import requests
import datetime
from email.Utils import formatdate

now = datetime.datetime.now()
beginTime = now - datetime.timedelta(minutes=10)
begin = formatdate(float(beginTime.strftime('%s')), localtime   = False, usegmt = True)


if len(sys.argv) != 1:
  print "Usage: scan.py"
  sys.exit(1)

def getJson(url):
  headers = {"Accept": "message/rfc2822"}
  # Look in ~/Downloads/mailgun_api_key
  api_key = os.environ['MAILGUN_API_KEY']
  r = requests.get(url, auth=("api", api_key), headers=headers, params={"begin": begin, "ascending": "yes"})

  if r.status_code == 200:
    response = r.json()
  else:
    print "Oops! Something went wrong: %s" % r.content
    sys.exit(1)

  return response


# url for retrieval
domain = "glgroup.com"
url = "https://api.mailgun.net/v3/%s/events"
url = url % (domain)



response = getJson(url)
i=0
while (i < 200):
  i+=1
  if len(response['items']):
    for item in response['items']:
      if 'url' in item and '#' in item['url']:
        print "Url: %s" % item['url']
    if 'paging' in response:
      #print "Retrieval %d" % i
      response = getJson(response['paging']['next'])
  else:
    print "Finished"
    sys.exit(1)