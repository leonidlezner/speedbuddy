import logging
import threading
import time
import signal


class MainRunner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.kill_me = False
        signal.signal(signal.SIGTERM, self.sigterm_handler)

    def sigterm_handler(self, signal, frame):
        logging.debug('SIGTERM')
        self.stop(sigterm=True)

    def loop(self):
        pass

    def cleanup(self):
        pass

    def run(self):
        self.kill_me = False

        logging.debug('Starting application!')

        while not self.kill_me:
            self.loop()

        logging.debug('Stopping application!')

        self.cleanup()

    def stop(self, sigterm=False):
        self.kill_me = True

    def lock(self):
        while self.isAlive():
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
                break


def main():
    logging.basicConfig(level=logging.DEBUG)
    app = MainRunner()
    app.start()
    app.lock()


if __name__ == '__main__':
    main()
