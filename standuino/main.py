from standuino.threads import ArduinoThread, ScreenThread
from standuino.state import State
from standuino.sqlite import save_state
import Queue
import logging
import sqlite3
import rjmetrics


ONE_YEAR = 60 * 60 * 24 * 365

logging.basicConfig(level=logging.DEBUG)


def create_initial_state(message):
    event_type, event_value = message
    assert(event_type == "standing")

    state = State(standing=event_value, at_desk=True)
    state.start()

    return state


def handle_message(message, old_state):
    logging.debug("Received message " + str(message))

    event_type, event_value = message

    if event_type == "at_desk" and event_value == old_state.at_desk:
        logging.info("Message did not change state")
        return old_state

    old_state.end()
    save_state(old_state)
    rjmetrics.send_state(old_state)

    if event_type == "at_desk":
        new_state = State(standing=old_state.standing, at_desk=event_value)
    else:
        new_state = State(standing=event_value, at_desk=old_state.at_desk)

    logging.info("State was: " + old_state.description + " now it's " +
                 new_state.description)

    new_state.start()
    return new_state


def main(args):
    queue = Queue.Queue()

    ArduinoThread(queue, threshold_cm=15).start()

    # the screen thread is not as important as the sitting/standing thread
    # if we never get something from the screen thread, we'll just assume
    # the user is at their desk. so wait for an initial message from the
    # arduino thread before starting to listen for screen messages
    logging.info("Reading initial sitting/standing state")
    initial_arduino_message = queue.get(timeout=ONE_YEAR)
    current_state = create_initial_state(initial_arduino_message)

    ScreenThread(queue).start()

    logging.info("Beginning main loop")

    try:
        while True:
            message = queue.get(timeout=ONE_YEAR)
            current_state = handle_message(message, current_state)
    finally:
        logging.info("Shutting down")
