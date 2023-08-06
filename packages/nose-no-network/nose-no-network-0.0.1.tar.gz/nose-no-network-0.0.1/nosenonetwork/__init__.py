#
#
#

__version__ = '0.0.1'

import logging
import os

from nose.plugins import Plugin
import socket


def _disabled(*args, **kwargs):
    raise Exception('No network access allowed during tests')


class NoNetworkPlugin(Plugin):
    name = 'no-network'

    def begin(self):
        socket.socket = _disabled
