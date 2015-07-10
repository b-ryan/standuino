from standuino.track import ArduinoThread, ScreenThread
import Queue
import logging

ONE_YEAR = 60 * 60 * 24 * 365


def print_cbk(message):
    print message


def main(args):
    queue = Queue.Queue()

    ArduinoThread(queue, threshold_cm=15).start()
    ScreenThread(queue).start()

    logging.info("Reading from queue")

    try:
        while True:
            message = queue.get(timeout=ONE_YEAR)
            logging.debug("Received message " + str(message))
    finally:
        logging.info("Shutting down")


if __name__ == "__main__":
    main()
