#!/usr/bin/env python

import logging
from pdb import set_trace

import requests
import simplejson
from time import time
import os

import facebook

# MY_API_URL
# MY_SITE_MSG
# MY_GROUP_NAME


def run():

    data = get_from_cal_json()
    msg = create_msg(data)
    post(msg)


def get_from_cal_json():


    r = requests.get(MY_API_URL)
    if r.status_code != requests.codes.ok:
        r.raise_for_status()

    j = simplejson.loads(r.text)

    now = time()
    inaweek = now + 60 * 60 * 24 * 7

    data = [
        x for x in j['data']
        if x['start']['timestamp'] > now
        and x['start']['timestamp'] < inaweek
    ]

    return data


def create_msg(data):

    for x in data:
        x['displaystart'] = x['start']['displaytimezone']

    msgbits = []
    msgbits.append(MY_SITE_MSG + ':')
    msgbits.append('')

    for x in data:
        msgbits.append(x['displaystart'])
        msgbits.append(x['summary'])
        msgbits.append(x['url'])
        msgbits.append('')

    msg = '\n'.join(msgbits)

    return msg


def get_group_ids(graph):
    # need user_groups permission

    # Why doesn't Facebook provide an API for getting the
    #    group id from the name?
    my_groups = graph.get_connections('me', 'groups')['data']

    # Add your group names here
    group_names = [
        MY_GROUP_NAME,
        # 'The Jazz List - Scotland',
    ]
    assert group_names, "Need to add some groups to post to"
    group_ids = [x['id'] for x in my_groups if x['name'] in group_names]


def post(msg):
    token = os.environ['FACEBOOK_ACCESS_TOKEN']
    graph = facebook.GraphAPI(token)
    profile = graph.get_object("me")

    group_ids = get_group_ids(graph)

    print msg
    return

    for group_id in group_ids:
        graph.put_object(group_id, "feed", message=msg)


if __name__ == '__main__':

    try:
        MY_API_URL
    except:
        print "Set your MY_API_URL e.g. 'http://jazzcal.com/api1/events.json'"
        exit (-1)

    try:
        MY_SITE_MSG
    except:
        print "Set your MY_SITE_MSG e.g. 'This week's jazz gigs on Jazzcal.com'"
        exit (-1)

    try:
        MY_GROUP_NAME
    except:
        print "Set your MY_GROUP_NAME"
        exit (-1)

    try:
        token = os.environ['FACEBOOK_ACCESS_TOKEN']
    except:
        print "Set the env var FACEBOOK_ACCESS_TOKEN"
        exit (-1)

    run()

# eof
