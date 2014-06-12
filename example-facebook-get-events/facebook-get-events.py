#!/usr/bin/env python

import logging
from pdb import set_trace

import requests
import simplejson
from time import time
import os
import datetime
from datetime import date
from dateutil import parser

import facebook

MY_API_URL = 'http://jazzcal.com/api1/events.json'
MY_SITE_MSG = "This week's jazz gigs on Jazzcal.com"
MY_GROUP_NAME = 'The Jazz List - Scotland'

GROUP_NAMES = [
    'The Jazz List - Scotland'
]

token = os.environ['FACEBOOK_ACCESS_TOKEN']
GRAPH = facebook.GraphAPI(token)


def run():

    for name in GROUP_NAMES:
        _import_from_group(name)


def _import_from_group(name):
    group = _get_group_from_name(name)
    events = _get_group_events(group)
    sync_events_to_db(events)


def sync_events_to_db(events):
    print ("TODO: sync_events_to_db")
    # print(events)
    for x in events:
        print (x['name'], x['start_date'], x['location'])



def _get_group_from_name(name):
    # need user_groups permission

    # Why doesn't Facebook provide an API for getting the
    #    group id from the name?
    my_groups = GRAPH.get_connections('me', 'groups')['data']

    for x in my_groups:
        if x['name'] == name:
            return x
    return None


def _get_group_events(group):
    # set_trace()
    print (group)

    today  = date.today()

    events = GRAPH.get_connections(group['id'], 'events')
    # set_trace()

    my_events = []
    for x in events['data']:
        if 'timezone' in x.keys():
            assert x['timezone'] == 'Europe/London'

        start_str = x['start_time']

        try:
            start_date = datetime.datetime.strptime(start_str, '%Y-%m-%d').date()
            start = start_date
        except ValueError:
            start_time = parser.parse(start_str)
            start_date = start_time.date()
            start = start_time

        if start_date < today:
            continue

        name = x['name']

        if name == 'Martin Waugh' and start == date(2014, 11, 4):
            continue

        try:
            location = x['location']
        except KeyError:
            set_trace()
            print (x)

        x['start_date'] = start_date
        my_events.append(x)
    return my_events



if __name__ == '__main__':

    # try:
    #     MY_API_URL
    # except:
    #     print ("Set your MY_API_URL e.g. 'http://jazzcal.com/api1/events.json'")
    #     exit (-1)

    # try:
    #     MY_SITE_MSG
    # except:
    #     print ("Set your MY_SITE_MSG e.g. 'This week's jazz gigs on Jazzcal.com'")
    #     exit (-1)

    # try:
    #     MY_GROUP_NAME
    # except:
    #     print ("Set your MY_GROUP_NAME")
    #     exit (-1)

    try:
        token = os.environ['FACEBOOK_ACCESS_TOKEN']
    except:
        print ("Set the env var FACEBOOK_ACCESS_TOKEN")
        exit (-1)

    run()

# eof
