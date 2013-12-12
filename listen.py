#!/usr/bin/env python
import time
import serial
import threading
import Queue
import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop
import logging
import psycopg2

ONE_YEAR = 60 * 60 * 24 * 365

class Tracker:

    def __init__(self):
        self.times = []
        self.position = 'sitting'
        self.lock_status = 'tracking_shutdown'

    def receive_event(self, event, time):
        last_row = self.times[-1] if len(self.times) else None

        if last_row and not last_row[2]:
            ## there is a sitting/standing event waiting to be closed
            # no matter what the event, we need to close that one out
            last_row[2] = time
            self.times[-1] = last_row

        if event in ('sitting', 'standing',):
            if self.lock_status != 'locked':
                self.times.append([event, time, None])
            self.position = event

        elif event == 'unlocked':
            assert(last_row)
            self.times.append([self.position, time, None])
            self.lock_status = event

        elif event in ('locked', 'tracking_shutdown',):
            self.lock_status = event

def dt():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def msg(event):
    return (event, dt(),)

class _Worker(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue

    def send_event(self, event):
        message = msg(event)
        logging.debug('Queuing ' + str(message))
        self.queue.put(message)

class ArduinoThread(_Worker):

    def run(self):
        logging.info('Starting arduino thread')
        arduino = serial.Serial('/dev/ttyACM0', 9600)
        while True:
            line = arduino.readline().replace("\r\n", "\n")[:-1]
            pre = "event: " 
            if pre in line:
                start = line.find(pre) + len(pre)
                sitting_standing = line[start:]
                assert(sitting_standing in ('sitting', 'standing',))
                self.send_event(sitting_standing)

class LockThread(_Worker):

    def run(self):
        logging.info('Starting lock thread')
        def cbk(message):
            unlocked = 0
            locked = 1
            assert(message in (unlocked, locked,))
            self.send_event(
                'locked' if message == locked else 'unlocked'
            )

        DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        bus.add_signal_receiver(
            cbk,
            dbus_interface='org.gnome.ScreenSaver',
            signal_name='ActiveChanged'
        )
        loop = gobject.MainLoop()
        gobject.threads_init()
        loop.run()

def get_connection():
    return psycopg2.connect(
        host='127.0.0.1',
        database='stand',
        user='stand',
        password='password',
    )

def save(event):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT into events (event, time)
        VALUES (%s, %s)
        ''',
        event
    )
    connection.commit()
    connection.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    queue = Queue.Queue()
    ArduinoThread(queue).start()
    LockThread(queue).start()

    logging.info('Reading from queue')

    try:
        while True:
            # queue.get blocks Ctrl-C signal unless a timeout is
            # specified, even if the timeout will never be reached.
            message = queue.get(timeout=ONE_YEAR)
            logging.debug('Received message ' + str(message))
            save(message)
    finally:
        save(msg('tracking_shutdown'))
