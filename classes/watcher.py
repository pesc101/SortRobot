import os
import time
from watchdog.observers import Observer
import logging


class Watcher:

    def __init__(self, directory, handler):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self, go_recursively):
        self.observer.schedule(self.handler, self.directory, recursive=go_recursively)
        self.observer.start()
        logging.info(f'Watcher Running in {self.directory}')
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
        logging.warning("Watcher Terminated\n\n")
