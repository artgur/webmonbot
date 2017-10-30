from argparse import ArgumentParser
from webmonbot.workers import TelegramWorker, CheckerWorker
from threading import Thread
import queue
import logging
import json
import signal
import sys

def main(args):
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', required=True)
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO'
    )
    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(threadName)s-%(name)s-%(funcName)s %(message)s",
        level=getattr(logging, args.log_level)
    )

    logger = logging.getLogger(__name__)
    out_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(out_handler)


    try:
        with open(args.file) as f:
            config_file = f.read()

    except FileNotFoundError as e:
        logger.critical('config file not found', e)
        logging.shutdown()
        exit(1)
    else:
        try:
            config = json.loads(config_file)
        except json.JSONDecodeError as e:
            logger.critical('parser error', e)
            logging.shutdown()
            exit(1)

    mqueue = queue.Queue()

    telegram_worker = TelegramWorker(config["telegram"], mqueue)
    telegram_thread = Thread(name="bot_thread", target=telegram_worker.run)
    telegram_thread.start()

    checker_worker = CheckerWorker(config["urlchecker"], mqueue)
    checker_thread = Thread(name="checker_thread", target=checker_worker.run)
    checker_thread.start()

    def stopper(*args):
        logging.info("Stopping application")
        telegram_worker.stop()
        checker_worker.stop()
        telegram_thread.join()
        checker_thread.join()
        logging.shutdown()

    signal.signal(signal.SIGTERM, stopper)
    signal.signal(signal.SIGINT, stopper)


if __name__ == "__main__":
    main()