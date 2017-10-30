from webmonbot.telegram import TelegramBot
from webmonbot.urlchecker import URLChecker

import queue
import logging
import time

logger = logging.getLogger(__name__)

class GenericWorker:
    def __init__(self, config, mqueue):
        self.exit_flag = False
        self.message_queue = mqueue
        self.config = config

    def run(self):
        pass

    def _put_msg(self, msg):
        self.message_queue.put(msg)

    def _get_msg(self):
        try:
            msg = self.message_queue.get(timeout=1)
        except queue.Empty:
            return None
        else:
            return msg

    def stop(self):
        self.exit_flag = True


class TelegramWorker(GenericWorker):
    def __init__(self, config, mqueue):
        super(TelegramWorker, self).__init__(config, mqueue)
        try:
            self.bot = TelegramBot(**config)
        except Exception as e:
            logger.exception(e)
        self.last_sended = 0
        self.send_timeout = 60

    def run(self):
        while not self.exit_flag:
            msg = self._get_msg()
            current_time = time.time()
            timeout = self.last_sended + self.send_timeout
            if msg and current_time >= timeout:
                self.bot.send_message(msg)
                self.last_sended = current_time


class CheckerWorker(GenericWorker):
    def __init__(self, config, mqueue):
        super(CheckerWorker, self).__init__(config, mqueue)
        try:
            self.checker = URLChecker(**config)
        except Exception as e:
            logger.exception(e)

    def run(self):
        logging.info("starting monitoring")
        self._put_msg("Monitoring up")
        while not self.exit_flag:
            if not self.checker.check():
                msg = "{0} is broken {1} not found".format(self.config['url'], self.config['substring'])
                self._put_msg(msg)
                time.sleep(1)




