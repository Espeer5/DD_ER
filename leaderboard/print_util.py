################################################################################
#                                                                              #
#  print_util.py                                                               #
#                                                                              #
#  This file defines printing utilities needed to do non-blocking asyncio      #
#  compliant printing to the console cross-platform. It is used in both the    #
# daemon and the client applications to print the leaderboard and log.         #
#                                                                              #
#  Author: Edward Speer                                                        #
#  Date:   05/15/2025                                                          #
#                                                                              #
################################################################################

################################################################################
#  IMPORTS                                                                     #
################################################################################

import asyncio
import sys
import threading
import queue

class PrintQ:
    def __init__(self):
        self.queue = queue.Queue()
        self.QThread = threading.Thread(target=self._print_thread, daemon=True)
        self.run = True
        self.QThread.start()

    def put(self, msg):
        self.queue.put(msg)

    def shutdown(self):
        self.run = False

    def _print_thread(self):
        while self.run:
            msg = self.queue.get()
            if msg is None:  # signal to exit
                break
            sys.__stdout__.write(msg + "\n")
            sys.__stdout__.flush()
