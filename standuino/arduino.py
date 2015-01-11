"""
A library for connecting to the standuino Arduino program for reading
distances.

TODO:
 - rename? other ideas: ardu-sonic, ardu-distance
 - maybe have this script write to the arduino to initialize the current
   session. This would make the clear_old_messages function less hacky. It
   would also allow for accurate timing
"""

import logging
import serial
from json import loads
import argparse
import time
import datetime

OLD_MESSAGE_THRESHOLD_MS = 100

logger = logging.getLogger(__name__)


class ValidationException(Exception):
    pass


def read(arduino):
    return arduino.readline().replace("\r\n", "").replace("\0", "")


def parse_and_validate(line):
    try:
        message = loads(line)
    except ValueError as e:
        raise ValidationException("{} is not valid JSON".format(line))

    if "distance_cm" not in message:
        raise ValidationException("key 'distance_cm' not in {}".format(line))

    message["datetime"] = datetime.datetime.now()
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


def handle_line(line, cbk):
    try:
        message = parse_and_validate(line)
    except ValidationException as e:
        logger.error(e.message)
        return
    else:
        cbk(message)


def main_loop(arduino, cbk):
    handle_line(clear_old_messages(arduino), cbk)
    while True:
        line = read(arduino)
        handle_line(line, cbk)


def connect(port, baud):
    logger.info("connecting to arduino on {} with baud {}".format(port, baud))
    try:
        arduino = serial.Serial(port, baud)
    except Exception as e:
        logger.exception("connection failed".format(args.device))
        raise e
    else:
        logger.info("connected")
        return arduino
