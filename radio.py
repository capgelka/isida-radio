#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import requests
import re
from xmltodict import parse

def save_root(root):
    with open('UGLY_STORAGE', 'w') as f:
        f.write(root)


def get_root():
    with open('UGLY_STORAGE') as f:
        return f.read()


def current_track(root_url, stream_name):
    xml = requests.get('{}/{}.xspf'.format(root_url, stream_name)).text
    return parse(xml)['playlist']['trackList']['track']['title']


def get_streams(root_url):
    html = requests.get(root_url).text
    pattern = re.compile('<h3 class="mount">Mount Point /(.*?)</h3>')
    return pattern.findall(html)


def radio(message_type, jid, nick, text):
    try:
        root = get_root()
    except IOError:
        root = ''
    try:
        streams = get_streams(root)
    except requests.RequestException:
        streams = []
    comm_args = text.split()
    buff_answer = []
    if not comm_args or len(comm_args) > 2:
        msg = '\n'.join('{name}: {track}'.format(name=s, 
                                                 track=current_track(root, s))
                        for s in streams)

    elif comm_args[0] == 'set':
        new_root = comm_args[1]
        save_root(new_root)
        msg = 'icecast root url had been set to {}'.format(new_root)
    else:
        stream = comm_args[0]
        if stream not in streams:
            msg = 'wrong stream name!'
        else:
            msg = current_track(root, stream)
    send_msg(message_type, jid, nick, msg)


execute = [(0, 'radio', radio, 2, 'command to work with radio'),]

if __name__ == '__main__':
    if 'send_msg' not in globals():
        def send_msg(a, b, c, d):
            print(d)
        import sys
        radio(None, None, None, " ".join(sys.argv[1:]))
