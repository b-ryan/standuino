#!/usr/bin/env python
import logging
import serial
from json import loads
import argparse
import time

OLD_MESSAGE_THRESHOLD_MS = 100

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read(arduino):
    return arduino.readline().replace("\r\n", "").replace("\0", "")


def parse(line):
    logger.debug("received {} HEX:({})"
                 .format(line, ':'.join(x.encode("hex") for x in line)))

    try:
        message = loads(line)
    except ValueError as e:
        logger.exception("invalid JSON received".format(line))
        return None

    return message


def now_ms():
    return int(round(time.time() * 1000))


def clear_old_messages(arduino):
    """The serial connection may have buffered lines that are too old (because
    the Arduino doesn't record the time the distance was recorded). This
    function reads and ignores all but the current line. It does so by seeing
    how long it takes to read each line. Once it reads a line that takes longer
    than OLD_MESSAGE_THRESHOLD_MS milliseconds to read, it knows this is the
    current line and returns the line."""
    while True:
        then_ms = now_ms()
        line = read(arduino)
        if (now_ms() - then_ms) > OLD_MESSAGE_THRESHOLD_MS:
            return line
        logger.debug("ignoring {}".format(line))


def handle_line(line):
    json = parse(line)
    if not json:
        return

    if "distance_cm" not in json:
        logger.warn("key 'distance_cm' not in JSON; moving on...")
        return

    distance_cm = json["distance_cm"]
    logging.info("Current distance (CM): {}".format(distance_cm))


def main_loop(arduino):
    handle_line(clear_old_messages(arduino))
    while True:
        handle_line(read(arduino))


def connect(port, baud):
    try:
        arduino = serial.Serial(port, baud)
    except Exception as e:
        logger.exception("connection failed".format(args.device))
        raise e
    return arduino


def main():
    parser = argparse.ArgumentParser(description="Lister for standuino.ino")
    parser.add_argument("--device", help="Device/port to listen to",
                        default="/dev/ttyACM0")
    parser.add_argument("--baud-rate", default=9600, type=int)
    args = parser.parse_args()

    logger.info("connecting to arduino on {} with baud {}"
                .format(args.device, args.baud_rate))

    arduino = connect(args.device, args.baud_rate)
    logger.info("connected")
    main_loop(arduino)

if __name__ == "__main__":
    main()
