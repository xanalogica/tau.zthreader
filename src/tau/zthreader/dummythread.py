import time

from signal import SIGINT
from Signals.Signals import SignalHandler

import logging
log = logging.getLogger("BackgroundThread")

class DummyThread(object):
    """  """

    running = True

    def __init__(self):
        pass # set up any static resources it needs

    def __call__(self, cfg_args):

        interval = float(cfg_args['ping-interval-secs'])
        ping_url = cfg_args['keepalive-host']

        while self.running:
            log.info("(pinging host %r)" % ping_url)
            time.sleep(interval)
        log.info("_shutdown_phase told me to stop")

    def stopme(self):
        log.info("exiting process, stopping thread")
        print "exiting process, stopping thread"
        self.running = False

dummythreadfunc = DummyThread()
SignalHandler.registerHandler(SIGINT, dummythreadfunc.stopme)
