import os
import chmura.log as log
from lo3.settings import DEFAULT_USER_AGENT, ENABLE_TOR, ENABLE_AGGRESSIVE_IP_CHANGE


if ENABLE_TOR:
    # Thanks to /u/gaten
    import socks
    import socket


    def create_connection(address, timeout=None, source_address=None):
        sock = socks.socksocket()
        sock.connect(address)
        return sock


    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
    socket.socket = socks.socksocket

    # patch the socket module
    socket.socket = socks.socksocket
    socket.create_connection = create_connection
    log.info('TOR forwarding enabled')
else:
    log.warning('TOR not enabled!!!')

if ENABLE_AGGRESSIVE_IP_CHANGE:
    from stem import Signal
    from stem.control import Controller

    log.warning('Aggressive IP changing is active!')

import urllib.request
import urllib.parse


def get_cur_path():
    return os.path.dirname(os.path.abspath(__file__))


def getReversedDict(dictionary, key):
    for d in dictionary:
        if dictionary[d] == key:
            return d
    return "null"


def getReversedStudent(dictionary, key):
    for d in dictionary:
        for k in dictionary[d]:
            if k['id'] == key:
                return k['firstname'] + ' ' + k['lastname']
    return "null"


def create_new_session():
    if ENABLE_AGGRESSIVE_IP_CHANGE:
        with Controller.from_port(port=14356) as controller:
            controller.authenticate(password='tojestbardzozlaszkola')
            controller.signal(Signal.NEWNYM)
        log.info('New TOR session created')


def url_request(address, header=None, params=None):
    if header is None:
        header = {}
    if params is None:
        params = {}

    header['User-Agent'] = DEFAULT_USER_AGENT

    options = urllib.parse.urlencode(params).encode('UTF-8')
    url = urllib.request.Request(address, options, headers=header)
    serverResponse = urllib.request.urlopen(url)
    return serverResponse
