import standuino.arduino as arduino
import screen_events
from ino.environment import Environment
import threading
import logging
import time
import copy

logging.basicConfig(level=logging.DEBUG)


def dt():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def msg(state_type, state_value):
    assert(state_type in ("standing", "at_desk"))
    return (state_type, state_value, dt(),)


class State:
    def __init__(self):
        self.at_desk = False
        self.standing = False


    def __str__(self):
        if not self.at_desk:
            return "Away from desk"
        return ("Standing" if self.standing else "Sitting") + " at desk"


class BaseThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue


    def queue_state(self, state_type, state_value):
        message = msg(state_type, state_value)
        logging.debug("Queuing new message: " + str(message))
        self.queue.put(message)


class ArduinoThread(BaseThread):
    def __init__(self, queue, threshold_cm):
        BaseThread.__init__(self, queue)
        self.current_state = None
        self.threshold_cm = threshold_cm

    def arduino_cbk(self, arduino_message):
        distance_cm = arduino_message["distance_cm"]
        standing = (distance_cm > self.threshold_cm)
        if standing != self.current_state:
            self.queue_state("standing", standing)
            self.current_state = standing

    def run(self):
        logging.info("Starting arduino thread")
        port = Environment().guess_serial_port()
        arduino.main_loop(arduino.connect(port), self.arduino_cbk)


class ScreenThread(BaseThread):
    def __init__(self, queue):
        BaseThread.__init__(self, queue)
        self.current_state = None

    def screen_cbk(self, screen_state):
        screen_on = (screen_state == screen_events.ScreenState.ON)
        if screen_on != self.current_state:
            self.queue_state("at_desk", screen_on)
            self.current_state = screen_on

    def run(self):
        logging.info("Starting screen thread")
        screen_events.event_loop(self.screen_cbk)
