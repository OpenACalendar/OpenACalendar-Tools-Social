
# @link http://ican.openacalendar.org/ OpenACalendar Open Source Software
# @license http://ican.openacalendar.org/license.html 3-clause BSD
# @copyright (c) 2013-2014, JMB Technology Limited, http://jmbtechnology.co.uk/

import sys
import ConfigParser
import json
import urllib2
import time

print "Post Upcoming OpenACalendar Events To Facebook\n\n"

#### Sanity check input
if len(sys.argv) < 2:
	print "No ini file passed!"
	exit()


#### Load config
config = ConfigParser.ConfigParser()
config.read(sys.argv[1])


#### Get Events
#### Build URL for Events
url = "http://" + config.get('events','site')+'/api1'

feedUrl = url + '/events.json'

# TODO add other filters

#### Get raw data
print "Getting events ..."
req = urllib2.Request(feedUrl)
response = urllib2.urlopen(req)
json_object = json.load(response)
print "Got " + str(len(json_object['data'])) +  " events in total!"

#### Filter events down to what we want
days = int(config.get('events','days'))
eventsBeforeThisTimeStampOnly = time.time() + (days * 24*60*60)

events = [event for event in json_object['data'] if eventsBeforeThisTimeStampOnly > event['start']['timestamp'] ]


print "Got " + str(len(events)) +  " events in next "+ str(days) +" days!"


#### Make event Text

eventText = "\n".join([event['summaryDisplay'] + " "+ event['start']['displaylocal'] + " "+event['siteurl'] for event in events])

print eventText


#### Post to facebook ???




